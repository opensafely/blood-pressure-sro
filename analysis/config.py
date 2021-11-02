#study start date.  should match date in project.yaml
start_date = "2021-04-01"

#study end date.  should match date in project.yaml
end_date = "2022-03-31"

#demographic variables by which code use is broken down
#select from ["sex", "age_band", "region", "imd", "ethnicity", "learning_disability"]
demographics = ["sex", "age_band", "region", "imd", "ethnicity", "learning_disability", "care_home_status"]

#name of measure
marker="Blood Pressure"

# Codelist path
# MILAN TODO ADD THE CODELIST I NEED HERE, NOT SURE ABOUT THIS ...
codelist_path = "codelists/nhsd-primary-care-domain-refsets-bp_cod.csv"

