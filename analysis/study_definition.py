# Import functions
import json
import pandas as pd

from cohortextractor import (
    StudyDefinition,
    patients,
    codelist,
    Measure
)

# Import codelists
from codelists import codelist, ld_codes, nhse_care_homes_codes, bp_dec_codes

from config import start_date, end_date, start_date_minus_5y, end_date_minus_3m, codelist_path, demographics

codelist_df = pd.read_csv(codelist_path)
codelist_expectation_codes = codelist_df['code'].unique()

# Specifiy study definition
study = StudyDefinition(
    index_date=start_date,
    # Configure the expectations framework
    default_expectations={
        "date": {"earliest": start_date, "latest": end_date},
        "rate": "exponential_increase",
        "incidence": 0.1,
    },
    # Define population parameters and denominator rules
    population=patients.satisfying(
        """
        # Define general population parameters
        registered AND
        (NOT died) AND
        (sex = 'F' OR sex = 'M') AND

        # Denominator Rule Number 1
        (age >= 45) AND
        
        # Denominator Rule Number 2
        # This rule doesnt exlude any patients
        
        # Denominator Rule Number 3
        (bp_declined = 0) AND
        
        # Denominator Rule Number 4
        (registered_include)
        """,

        registered=patients.registered_as_of(
            "index_date",
            return_expectations={"incidence": 0.9},
        ),

        died=patients.died_from_any_cause(
            on_or_before="index_date",
            returning="binary_flag",
            return_expectations={"incidence": 0.1}
        ),

        # Define variable for denominator rule number 3
        bp_declined=patients.with_these_clinical_events(
            codelist=bp_dec_codes,
            returning="binary_flag"
        ),
        # Define variable for denominator rule number 4
        # Reject patients passed to this rule who registered with the GP practice in the 3 month period 
        # leading up to and including the payment period end date. 
        # Select the remaining patients.
        registered_include=patients.registered_with_one_practice_between(
            start_date=end_date_minus_3m,
            end_date=end_date,
            return_expectations={"incidence": 0.1}
        )

    ),

    age=patients.age_as_of(
        "index_date",
        return_expectations={
            "rate": "universal",
            "int": {"distribution": "population_ages"},
        },
    ),

    age_band=patients.categorised_as(
        {
            "missing": "DEFAULT",
            "0-19": """ age >= 0 AND age < 20""",
            "20-29": """ age >=  20 AND age < 30""",
            "30-39": """ age >=  30 AND age < 40""",
            "40-49": """ age >=  40 AND age < 50""",
            "50-59": """ age >=  50 AND age < 60""",
            "60-69": """ age >=  60 AND age < 70""",
            "70-79": """ age >=  70 AND age < 80""",
            "80+": """ age >=  80 AND age < 120""",
        },
        return_expectations={
            "rate": "universal",
            "category": {
                "ratios": {
                    "0-19": 0.125,
                    "20-29": 0.125,
                    "30-39": 0.125,
                    "40-49": 0.125,
                    "50-59": 0.125,
                    "60-69": 0.125,
                    "70-79": 0.125,
                    "80+": 0.125,
                }
            },
        },
    ),

    sex=patients.sex(
        return_expectations={
            "rate": "universal",
            "category": {"ratios": {"M": 0.5, "F": 0.5}},
        }
    ),

    practice=patients.registered_practice_as_of(
        "index_date",
        returning="pseudo_id",
        return_expectations={
            "int": {"distribution": "normal", "mean": 25, "stddev": 5}, "incidence": 0.5}
    ),

    region=patients.registered_practice_as_of(
        "index_date",
        returning="nuts1_region_name",
        return_expectations={"category": {"ratios": {
            "North East": 0.1,
            "North West": 0.1,
            "Yorkshire and the Humber": 0.1,
            "East Midlands": 0.1,
            "West Midlands": 0.1,
            "East of England": 0.1,
            "London": 0.2,
            "South East": 0.2, }}}
    ),

    imd=patients.address_as_of(
        "index_date",
        returning="index_of_multiple_deprivation",
        round_to_nearest=100,
        return_expectations={
            "rate": "universal",
            "category": {"ratios": {"100": 0.2, "200": 0.2, "300": 0.2, "400": 0.2, "500": 0.2}},
        },
    ),

    learning_disability=patients.with_these_clinical_events(
        ld_codes,
        on_or_before="index_date",
        returning="binary_flag",
        return_expectations={"incidence": 0.01, },
    ),

    care_home_status=patients.with_these_clinical_events(
        nhse_care_homes_codes,
        returning="binary_flag",
        on_or_before="index_date",
        return_expectations={"incidence": 0.2}
    ),
    
    # Numerator Rule Number 1
    # Select patients from the denominator who had their blood pressure recorded in the 5 year period 
    # leading up to and including the payment period end date. 
    # Reject the remaining patients.
    event=patients.with_these_clinical_events(
        codelist=codelist,     
        between=[start_date_minus_5y, end_date],
        returning="binary_flag",
        return_expectations={"incidence": 0.5}
    ),

    event_code=patients.with_these_clinical_events(
        codelist=codelist,
        between=[start_date_minus_5y, end_date],
        returning="code",
        return_expectations={"category": {
            "ratios": {x: 1/len(codelist_expectation_codes) for x in codelist_expectation_codes}}, }
    ),
)

# # Create default measures
measures = [

    Measure(
        id="event_code_rate",
        numerator="event",
        denominator="population",
        group_by=["event_code"],
        small_number_suppression=True
    ),

    Measure(
        id="practice_rate",
        numerator="event",
        denominator="population",
        group_by=["practice"],
        small_number_suppression=False
    ),

]

# Add demographics measures

for d in demographics:

    if d == 'imd':
        apply_suppression = False

    else:
        apply_suppression = True

    m = Measure(
        id=f'{d}_rate',
        numerator="event",
        denominator="population",
        group_by=[d],
        small_number_suppression=apply_suppression
    )

    measures.append(m)
