from cohortextractor import codelist_from_csv
from config import codelist_path

# Change the path of the codelist to your chosen codelist
codelist = codelist_from_csv(codelist_path, system='snomed')

bp_dec_codes = codelist_from_csv(
    "codelists/nhsd-primary-care-domain-refsets-bpdec_cod.csv",
    system="snomed",
    column="code",
)

bp_codes = codelist_from_csv(
    "codelists/nhsd-primary-care-domain-refsets-bp_cod.csv",
    system="snomed",
    column="code",
)

bp_home_codes = codelist_from_csv(
    "codelists/nhsd-primary-care-domain-refsets-homebp_cod.csv",
    system="snomed",
    column="code",
)

ethnicity_codes = codelist_from_csv(
        "codelists/opensafely-ethnicity.csv",
        system="ctv3",
        column="Code",
        category_column="Grouping_6",
    )

nhse_care_homes_codes = codelist_from_csv("codelists/opensafely-nhs-england-care-homes-residential-status.csv",
    system="snomed",
    column="code",
)

ld_codes = codelist_from_csv(
    "codelists/opensafely-learning-disabilities.csv",
    system="ctv3",
    column="CTV3Code",
)
