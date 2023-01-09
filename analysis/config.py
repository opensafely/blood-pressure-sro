# Study start date
# Note: This should match the start dates in project.yaml
# In QOF also: Payment Period Start Date (PPSD)
start_date = "2019-03-01"

# Study end date
# Note: This should match the end dates in project.yaml
# In QOF also: Payment Period End Date (PPED)
end_date = "2022-03-01"

# demographic variables by which code use is broken down
demographic_breakdowns = [
    "age_band",
    "sex",
    "region",
    "care_home",
    "learning_disability",
    "imd_q5",
    "ethnicity6",
    "ethnicity16",
]

bp002_exclusions = [
    "bp002_excl_denominator_r3",
    "bp002_excl_denominator_r4",
]

bp002_flowchart = [
    "denominator_r1_reject",
    "denominator_r2_select",
    "denominator_r3_reject",
    "denominator_r4_reject",
]
