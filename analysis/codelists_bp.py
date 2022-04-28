from cohortextractor import codelist_from_csv

# Cluster name: BP_COD
# Description: Blood pressure (BP) recording codes
# SNOMED CT: ^999012731000230108
bp_codes = codelist_from_csv(
    "codelists/nhsd-primary-care-domain-refsets-bp_cod.csv",
    system="snomed",
    column="code",
)

# Cluster name: BPDEC_COD
# Description: Codes indicating the patient has chosen not to have blood
# pressure procedure
# SNOMED CT: ^999012611000230106
bp_dec_codes = codelist_from_csv(
    "codelists/nhsd-primary-care-domain-refsets-bpdec_cod.csv",
    system="snomed",
    column="code",
)
