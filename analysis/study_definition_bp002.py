from cohortextractor import StudyDefinition, patients, Measure

import json
import pandas as pd

# Import dates and codelists
from config import start_date, end_date, demopgraphic_breakdowns
from codelists_bp import bp_codes, bp_dec_codes

# Import shared variable dictionaries
from dict_bp_variables import bp002_variables
from dict_demographic_variables import demographic_variables

study = StudyDefinition(
    index_date=start_date,
    default_expectations={
        "date": {"earliest": start_date, "latest": end_date},
        "rate": "uniform",
        "incidence": 0.5,
    },
    population=patients.satisfying(
        """
        # Define general population parameters
        (NOT died) AND
        (sex = 'F' OR sex = 'M') AND
        (age_band != 'missing') AND

        # Define GMS registration status
        gms_reg_status AND

        # Define list size type:
        age >= 45
        """,
    ),
    # Include blood pressure and demographic variable dictionaries
    **demographic_variables,
    **bp002_variables,
)

measures = [
    Measure(
        id="bp002_population_rate",
        numerator="bp002_numerator",
        denominator="population",
        group_by=["practice"],
        small_number_suppression=True,
    ),
    Measure(
        id="bp002_population_rate",
        numerator="bp002_denominator_r2",
        denominator="population",
        group_by=["practice"],
        small_number_suppression=True,
    ),
    Measure(
        id="bp002_population_rate",
        numerator="bp002_denominator_r3",
        denominator="population",
        group_by=["practice"],
        small_number_suppression=True,
    ),
    Measure(
        id="bp002_population_rate",
        numerator="bp002_denominator_r4",
        denominator="population",
        group_by=["practice"],
        small_number_suppression=True,
    ),
]

# Create blood pressure indicator BP002 measures
for breakdown in demopgraphic_breakdowns:
    m = Measure(
        id=f"bp002_{breakdown}_breakdown_rate",
        numerator="bp002_numerator",
        denominator="bp002_denominator",
        group_by=[breakdown],
        small_number_suppression=True,
    )
    measures.append(m)

# Create blood pressure exclusion measures
for breakdown in demopgraphic_breakdowns:
    m = Measure(
        id=f"bp002_{breakdown}_breakdown_rate",
        numerator="bp002_numerator",
        denominator="bp002_denominator",
        group_by=[breakdown],
        small_number_suppression=True,
    )
    measures.append(m)
