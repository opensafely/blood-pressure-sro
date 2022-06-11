# Define common demographic variables needed across indicators here
# See https://docs.opensafely.org/study-def-tricks/

from cohortextractor import patients
from codelists_demographic import (
    nhse_care_homes_codes,
    learning_disability_codes,
)

demographic_variables = dict(
    # GMS registration status
    gms_reg_status=patients.registered_as_of(
        "last_day_of_month(index_date)",
        return_expectations={"incidence": 0.9},
    ),
    died=patients.died_from_any_cause(
        on_or_before="last_day_of_month(index_date)",
        returning="binary_flag",
        return_expectations={"incidence": 0.1},
    ),
    # Age as of end of NHS financial year (March 31st)
    # NOTE: This project extracts QOF montly. Therefore
    # only the March estimates is matching the buisiness
    # rule definition for age.
    age=patients.age_as_of(
        "last_day_of_month(index_date) + 1 day",
        return_expectations={
            "rate": "universal",
            "int": {"distribution": "population_ages"},
        },
    ),
    age_band=patients.categorised_as(
        {
            "missing": "DEFAULT",
            "45-49": """ age >=  45 AND age < 50""",
            "50-59": """ age >=  50 AND age < 60""",
            "60-69": """ age >=  60 AND age < 70""",
            "70-79": """ age >=  70 AND age < 80""",
            "80+": """ age >=  80 AND age <= 120""",
        },
        return_expectations={
            "rate": "universal",
            "category": {
                "ratios": {
                    "missing": 0.005,
                    "45-49": 0.25,
                    "50-59": 0.2,
                    "60-69": 0.2,
                    "70-79": 0.2,
                    "80+": 0.145,
                }
            },
        },
    ),
    # Sex
    sex=patients.sex(
        return_expectations={
            "rate": "universal",
            "category": {"ratios": {"M": 0.49, "F": 0.51}},
        }
    ),
    # Index of Multiple Deprivation (IMD)
    imd_q5=patients.categorised_as(
        {
            "Unknown": "DEFAULT",
            "1": "imd >= 0 AND imd < 32800*1/5",
            "2": "imd >= 32800*1/5 AND imd < 32800*2/5",
            "3": "imd >= 32800*2/5 AND imd < 32800*3/5",
            "4": "imd >= 32800*3/5 AND imd < 32800*4/5",
            "5": "imd >= 32800*4/5 AND imd <= 32800",
        },
        imd=patients.address_as_of(
            "index_date",
            returning="index_of_multiple_deprivation",
            round_to_nearest=100,
        ),
        return_expectations={
            "rate": "universal",
            "category": {
                "ratios": {
                    "Unknown": 0.05,
                    "1": 0.20,
                    "2": 0.20,
                    "3": 0.20,
                    "4": 0.20,
                    "5": 0.15,
                }
            },
        },
    ),
    # Region
    region=patients.registered_practice_as_of(
        "last_day_of_month(index_date)",
        returning="nuts1_region_name",
        return_expectations={
            "rate": "universal",
            "category": {
                "ratios": {
                    "North East": 0.1,
                    "North West": 0.1,
                    "Yorkshire and The Humber": 0.1,
                    "East Midlands": 0.1,
                    "West Midlands": 0.1,
                    "East": 0.1,
                    "London": 0.2,
                    "South East": 0.1,
                    "South West": 0.1,
                },
            },
        },
    ),
    # Practice
    practice=patients.registered_practice_as_of(
        "last_day_of_month(index_date)",
        returning="pseudo_id",
        return_expectations={
            "int": {"distribution": "normal", "mean": 25, "stddev": 5},
            "incidence": 0.5,
        },
    ),
    learning_disability=patients.with_these_clinical_events(
        learning_disability_codes,
        on_or_before="last_day_of_month(index_date)",
        returning="binary_flag",
        return_expectations={"incidence": 0.01},
    ),
    care_home=patients.with_these_clinical_events(
        nhse_care_homes_codes,
        returning="binary_flag",
        on_or_before="last_day_of_month(index_date)",
        return_expectations={"incidence": 0.2},
    ),
)
