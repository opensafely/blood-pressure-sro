from cohortextractor import (
    StudyDefinition,
    patients,
    codelist,
    codelist_from_csv,
    Measure,
)

from config import end_date
from codelists_demographic import ethnicity6_codes, ethnicity16_codes

study = StudyDefinition(
    default_expectations={
        "date": {"earliest": "1900-01-01", "latest": "today"},
        "rate": "uniform",
    },
    index_date=end_date,
    population=patients.all(),
    eth=patients.with_these_clinical_events(
        ethnicity16_codes,
        returning="category",
        find_last_match_in_period=True,
        include_date_of_match=False,
        return_expectations={
            "category": {
                "ratios": {
                    "1": 0.1,
                    "2": 0.1,
                    "3": 0.1,
                    "4": 0.1,
                    "5": 0.1,
                    "6": 0.025,
                    "7": 0.025,
                    "8": 0.05,
                    "9": 0.05,
                    "10": 0.05,
                    "11": 0.05,
                    "12": 0.05,
                    "13": 0.05,
                    "14": 0.05,
                    "15": 0.05,
                    "16": 0.05,
                }
            },
            "incidence": 0.75,
        },
    ),
    ethnicity16=patients.categorised_as(
        {
            "Unknown": "DEFAULT",
            "White - British": "eth='1'",
            "White - Irish": "eth='2'",
            "White - Any other White background": "eth='3'",
            "Mixed - White and Black Caribbean": "eth='4'",
            "Mixed - White and Black African": "eth='5'",
            "Mixed - White and Asian": "eth='6'",
            "Mixed - Any other mixed background": "eth='7'",
            "Asian or Asian British - Indian": "eth='8'",
            "Asian or Asian British - Pakistani": "eth='9'",
            "Asian or Asian British - Bangladeshi": "eth='10'",
            "Asian or Asian British - Any other Asian background": "eth='11'",
            "Black or Black British - Caribbean": "eth='12'",
            "Black or Black British - African": "eth='13'",
            "Black or Black British - Any other Black background": "eth='14'",
            "Other Ethnic Groups - Chinese": "eth='15'",
            "Other Ethnic Groups - Any other ethnic group": "eth='16'",
        },
        return_expectations={
            "category": {
                "ratios": {
                    "White - British": 0.1,
                    "White - Irish": 0.1,
                    "White - Any other White background": 0.1,
                    "Mixed - White and Black Caribbean": 0.1,
                    "Mixed - White and Black African": 0.1,
                    "Mixed - White and Asian": 0.025,
                    "Mixed - Any other mixed background": 0.025,
                    "Asian or Asian British - Indian": 0.05,
                    "Asian or Asian British - Pakistani": 0.05,
                    "Asian or Asian British - Bangladeshi": 0.05,
                    "Asian or Asian British - Any other Asian background": 0.05,
                    "Black or Black British - Caribbean": 0.05,
                    "Black or Black British - African": 0.05,
                    "Black or Black British - Any other Black background": 0.05,
                    "Other Ethnic Groups - Chinese": 0.05,
                    "Other Ethnic Groups - Any other ethnic group": 0.05,
                }
            },
            "incidence": 0.8,
        },
    ),
    ethnicity6=patients.categorised_as(
        {
            "Unknown": "DEFAULT",
            "White": "eth='1'",
            "Mixed": "eth='2'",
            "Asian or Asian British": "eth='3'",
            "Black or Black British": "eth='4'",
            "Chinese or Other Ethnic Groups": "eth='5'",
        },
        return_expectations={
            "category": {
                "ratios": {
                    "White": 0.2,
                    "Mixed": 0.2,
                    "Asian or Asian British": 0.2,
                    "Black or Black British": 0.2,
                    "Chinese or Other Ethnic Groups": 0.2,
                }
            },
            "incidence": 0.8,
        },
    ),
)
