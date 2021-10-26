#study start date.  should match date in project.yaml
start_date = "2021-06-01"

#study end date.  should match date in project.yaml
end_date = "2021-12-01"

#demographic variables by which code use is broken down
#select from ["sex", "age_band", "region", "imd", "ethnicity", "learning_disability"]
demographics = ["sex", "age_band", "region", "imd", "ethnicity", "learning_disability", "care_home_status"]

#name of measure
marker="Systolic blood pressure"

#codelist path
codelist_path = "codelists/opensafely-systolic-blood-pressure-qof.csv"

