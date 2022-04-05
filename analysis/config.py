from dateutil.relativedelta import relativedelta
from datetime import date, datetime

# study start date. should match date in project.yaml
start_date = "2019-09-01"

# study end date. should match date in project.yaml
end_date = "2022-03-31"

# Vertical plot lines for financial year
# Leave an empty list if no lines needed
# If a date is out of range of the graph, it will not be visible
vertical_lines = ["2020-04-01", "2021-04-01"]

# demographic variables by which code use is broken down
demographics = [
    "sex",
    "age_band",
    "region",
    "imd",
    "ethnicity",
    "learning_disability",
    "care_home_status",
]

# name of measure
marker = "QOF Blood Pressure targets"
qof_measure_marker = "BP002"

# Codelist path
codelist_path = "codelists/nhsd-primary-care-domain-refsets-bp_cod.csv"
