# Import functions
import json
import pandas as pd

from cohortextractor import StudyDefinition, patients, codelist, Measure

# Import codelists
from codelists import codelist, ld_codes, nhse_care_homes_codes, bp_dec_codes

from config import (
    start_date,
    end_date,
    start_date_minus_5y,
    end_date_minus_3m,
    codelist_path,
    demographics,
)

codelist_df = pd.read_csv(codelist_path)
codelist_expectation_codes = codelist_df["code"].unique()

# Specifiy study definition
study = StudyDefinition(
    index_date=end_date,
    # Configure the expectations framework
    default_expectations={
        "date": {"earliest": start_date, "latest": end_date},
        "rate": "exponential_increase",
        "incidence": 0.1,
    },
    # Define population parameters and denominator rules for:
    # Business Rules for Quality and Outcomes Framework (QOF) 2021/22 - Blood pressure
    # Resources
    # Web: https://digital.nhs.uk/data-and-information/data-collections-and-data-sets/data-collections/quality-and-outcomes-framework-qof/quality-and-outcome-framework-qof-business-rules/qof-business-rules-v46.0-2021-2022-baseline-release
    # Zip file: https://nhs-prod.global.ssl.fastly.net/binaries/content/assets/website-assets/data-and-information/data-collections/qof/qof_v46_tracked_changes_accepted.zip
    # Reference document: Blood_Pressure_v46.0.docx
    # Indicator ID: BP002
    # Description: The percentage of patients aged 45 or over who have a record of blood pressure in the preceding 5 years.
    population=patients.satisfying(
        """
        # Define general population parameters
        registered AND
        (NOT died) AND
        (sex = 'F' OR sex = 'M') AND

        # Denominator Rule Number 1
        # Description: Reject patients from the specified population who are aged less than 45 years old. 
        (age >= 45) AND
        
        # Denominator Rule Number 2
        # Description: Select patients passed to this rule who had their blood pressure recorded in the 5 year period leading up to and including the payment period end date. 
        # Note: This rule doesnt exlude any patients
        
        # Denominator Rule Number 3
        # Description: Reject patients passed to this rule chose not to have their blood pressure recorded in the 5 year period leading up to and including the payment period end date. 
        (bp_declined = 0) AND
        
        # Denominator Rule Number 4
        # Description: Reject patients passed to this rule who registered with the GP practice in the 3 month period leading up to and including the payment period end date. 
        (registered_include)
        """,
        registered=patients.registered_as_of(
            "index_date",
            return_expectations={"incidence": 0.9},
        ),
        died=patients.died_from_any_cause(
            on_or_before="index_date",
            returning="binary_flag",
            return_expectations={"incidence": 0.1},
        ),
        # Define variable for denominator rule number 3
        bp_declined=patients.with_these_clinical_events(
            between=[
                "first_day_of_month(index_date) - 5 years",
                "last_day_of_month(index_date)",
            ],
            codelist=bp_dec_codes,
            returning="binary_flag",
        ),
        # Define variable for denominator rule number 4
        # Reject patients passed to this rule who registered with the GP practice in the 3 month period
        # leading up to and including the payment period end date.
        # Select the remaining patients.
        registered_include=patients.registered_with_one_practice_between(
            start_date=end_date_minus_3m,
            end_date=end_date,
            return_expectations={"incidence": 0.1},
        ),
    ),
    # Currently this is not possible, here we are calculating age as of March 1st YYYY
    # because age_as_of uses the first day of the given month to calculate the age
    age=patients.age_as_of(
        "last_day_of_nhs_financial_year(index_date) + 1 day",
        return_expectations={
            "rate": "universal",
            "int": {"distribution": "population_ages"},
        },
    ),
    age_band=patients.categorised_as(
        {
            "missing": "DEFAULT",
            "45-49": """ age >= 45 AND age < 50""",
            "50-59": """ age >= 50 AND age < 60""",
            "60-69": """ age >= 60 AND age < 70""",
            "70-79": """ age >= 70 AND age < 80""",
            "80+": """ age >=  80 AND age < 120""",
        },
        return_expectations={
            "rate": "universal",
            "category": {
                "ratios": {
                    "45-49": 0.349,
                    "50-59": 0.30,
                    "60-69": 0.20,
                    "70-79": 0.10,
                    "80+": 0.05,
                    "missing": 0.001,
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
            "int": {"distribution": "normal", "mean": 25, "stddev": 5},
            "incidence": 0.5,
        },
    ),
    region=patients.registered_practice_as_of(
        "index_date",
        returning="nuts1_region_name",
        return_expectations={
            "category": {
                "ratios": {
                    "North East": 0.1,
                    "North West": 0.1,
                    "Yorkshire and the Humber": 0.1,
                    "East Midlands": 0.1,
                    "West Midlands": 0.1,
                    "East of England": 0.1,
                    "London": 0.2,
                    "South East": 0.2,
                }
            }
        },
    ),
    imd=patients.address_as_of(
        "index_date",
        returning="index_of_multiple_deprivation",
        round_to_nearest=100,
        return_expectations={
            "rate": "universal",
            "category": {
                "ratios": {"100": 0.2, "200": 0.2, "300": 0.2, "400": 0.2, "500": 0.2}
            },
        },
    ),
    learning_disability=patients.with_these_clinical_events(
        ld_codes,
        on_or_before="index_date",
        returning="binary_flag",
        return_expectations={
            "incidence": 0.01,
        },
    ),
    care_home_status=patients.with_these_clinical_events(
        nhse_care_homes_codes,
        returning="binary_flag",
        on_or_before="index_date",
        return_expectations={"incidence": 0.2},
    ),
    # Numerator Rule Number 1
    # Description: Select patients from the denominator who had their blood pressure recorded in the 5 year period
    # leading up to and including the payment period end date.
    # NOTE: Binary because we want to know who had a reading of bp
    event=patients.with_these_clinical_events(
        codelist=codelist,
        between=[
            "first_day_of_month(index_date) - 5 years",
            "last_day_of_month(index_date)",
        ],
        returning="binary_flag",
        return_expectations={"incidence": 0.5},
    ),
    # NOTE: This gives us information about which code from the codelist a px had
    event_code=patients.with_these_clinical_events(
        codelist=codelist,
        between=[
            "first_day_of_month(index_date) - 5 years",
            "last_day_of_month(index_date)",
        ],
        returning="code",
        return_expectations={
            "category": {
                "ratios": {
                    x: 1 / len(codelist_expectation_codes)
                    for x in codelist_expectation_codes
                }
            },
        },
    ),
)

# Create default measures
measures = [
    Measure(
        id="event_code_rate",
        numerator="event",
        denominator="population",
        group_by=["event_code"],
        small_number_suppression=True,
    ),
    Measure(
        id="practice_rate",
        numerator="event",
        denominator="population",
        group_by=["practice"],
        small_number_suppression=False,
    ),
]

# Add demographic measures
for d in demographics:

    if d in ["imd", "age_band"]:
        apply_suppression = False

    else:
        apply_suppression = True

    m = Measure(
        id=f"{d}_rate",
        numerator="event",
        denominator="population",
        group_by=[d],
        small_number_suppression=apply_suppression,
    )

    measures.append(m)
