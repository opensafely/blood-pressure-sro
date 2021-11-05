from dateutil.relativedelta import relativedelta
from datetime import date, datetime

# study start date. should match date in project.yaml
start_date = "2019-09-01"

# study end date. should match date in project.yaml
end_date = "2022-03-31"

# Define a function for fun, I'm not really happy with this but it works
# Definitely need some help improving this, need to learn how to write robust funs in py
def calculate_date(date, months):
    """Add or substract months to a date in "YYYY-MM-DD" format.
    
    Args:
        date: date as string in YYYY-MM-DD format.
        month: Number of month to add (+) or substract (-)

    Returns:
        Date as string in YYYY-MM-DD format
    """

    date_calc = datetime.strptime(date, "%Y-%m-%d").date() + relativedelta(months=months)
    return date_calc.strftime("%Y-%m-%d")

# Define more date variables needed for this project
start_date_minus_5y = calculate_date(date = end_date, months = -(5 * 12))
end_date_minus_3m = calculate_date(date = end_date, months = -3)

# demographic variables by which code use is broken down
demographics = ["sex", "age_band", "region", "imd", "ethnicity", "learning_disability", "care_home_status"]

#name of measure
marker = "Blood Pressure"

# Codelist path
codelist_path = "codelists/nhsd-primary-care-domain-refsets-bp_cod.csv"

