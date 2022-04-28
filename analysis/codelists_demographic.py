from cohortextractor import codelist_from_csv

ethnicity6_codes = codelist_from_csv(
    "codelists/opensafely-ethnicity.csv",
    system="ctv3",
    column="Code",
    category_column="Grouping_6",
)

learning_disability_codes = codelist_from_csv(
    "codelists/nhsd-primary-care-domain-refsets-ld_cod.csv",
    system="snomed",
    column="code",
)

nhse_care_homes_codes = codelist_from_csv(
    "codelists/nhsd-primary-care-domain-refsets-carehome_cod.csv",
    system="snomed",
    column="code",
)
