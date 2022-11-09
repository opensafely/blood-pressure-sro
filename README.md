# Blood pressure (BP) indicators in the Quality and Outcomes Framework (QOF)

[View on OpenSAFELY](https://jobs.opensafely.org/datalab/blood-pressure-quality-and-outcomes-framework-qof/qof-blood-pressure/)

Details of the purpose and any published outputs from this project can be found at the link above.

The contents of this repository MUST NOT be considered an accurate or valid representation of the study or its purpose. 
This repository may reflect an incomplete or incorrect analysis with no further ongoing work.
The content has ONLY been made public to support the OpenSAFELY [open science and transparency principles](https://www.opensafely.org/about/#contributing-to-best-practice-around-open-science) and to support the sharing of re-usable code for other subsequent users.
No clinical, policy or safety conclusions must be drawn from the contents of this repository.

## Overview
 
The study in this repository aims to
(1) implement the QOF blood pressure indicators in OpenSAFELY and
(2) provide resources and coding guidelines that help with the implementation of future QOF studies in OpnSAFELY.
New QOF studies should follow the workflow and repository strcuture described in the [qof-utilities](https://github.com/opensafely/qof-utilities) GitHub repository and the general structure of this repo (for more details see [this](#repository-structure) of the readme below.

General practice has been disrupted by the pandemic in many clinical areas (e.g., Curtis et al., [2021](https://bjgp.org/content/72/714/e63); Williams et al., [2020](https://www.thelancet.com/journals/lanpub/article/PIIS2468-2667(20)30201-2/fulltext)). 
This project aims to assess the impact of the pandemic on the routine management of blood pressure as measured by the QOF blood pressure indicator. 
High blood pressure is one of the leading risk factors for several diseases (e.g., cardiovascular disease, stroke) worldwide. 
Research suggests that delays in the management of high blood pressure are associated with worse clinical outcomes, for example acute cardiovascular events, or death (Xu et al., [2015](https://www.bmj.com/content/350/bmj.h158)). 

## QOF Blood pressure business rules

[The Quality and Outcomes Framework (QOF)](https://digital.nhs.uk/data-and-information/data-tools-and-services/data-services/general-practice-data-hub/quality-outcomes-framework-qof) outlines several indicators that focus blood pressure (BP) targets. 
This project aims to use OpenSAFELY to quantify the extent to which any of the relevant blood pressure QOF indicators ([v46](https://digital.nhs.uk/data-and-information/data-collections-and-data-sets/data-collections/quality-and-outcomes-framework-qof/quality-and-outcome-framework-qof-business-rules/qof-business-rules-v46.0-2021-2022-baseline-release)) were disrupted during the pandemic but wont link our results to clinical outcomes.
A short description of the QOF blood pressure ([v46](https://digital.nhs.uk/data-and-information/data-collections-and-data-sets/data-collections/quality-and-outcomes-framework-qof/quality-and-outcome-framework-qof-business-rules/qof-business-rules-v46.0-2021-2022-baseline-release)) indicator BP002 is shown below:

- **BP002**: The percentage of **patients aged 45** or over who have a **record of blood pressure in the preceding 5 years**.

## Repository structure 

The following list outlines the the general steps for implementing QOF indicators in OpenSAFELY:

1. Add all codelists specified in the QOF busieness rules to [codelists/codelists.txt](codelists/codelists.txt). 
   The codelists can be found on OpenCodelists under [NHSD Primary Care Domain Refsets](https://www.opencodelists.org/codelist/nhsd-primary-care-domain-refsets/).
2. Define the variables specified in the business rules in shared variable dictionaries or individyal study definitions
3. Implement QOF numerator and denominator rules in study definition (see [here](#study-definitions))
4. Specify measures (e.g., percentage achievement, exclusions, and breakdowns) for each indicator (see [here](#measures))

**More details and reusable code for implementing QOF registers in OpenSAFELY are available in the [qof-utilities](https://github.com/opensafely/qof-utilities) GitHub repository.**

### Codelists

- All codelists used in this project are available in the [codelists](codelists) folder.

### Variable dictionaries

Variables that are shared by multiple QOF indicators are specified in dictionaries (see [OpenSAFELY programming tricks](https://docs.opensafely.org/study-def-tricks/#sharing-common-study-definition-variables)):
- **Demographic variables**: [analysis/dict_demo_variables.py](analysis/dict_demo_variables.py)
- Variables to define the blood pressure **indicator** (`bp002_variables`): [analysis/dict_bp_variables.py](analysis/dict_bp_variables.py)

    Almost all denominator and numerator rules can be broken down into individual variables that follow this strucutre: (1) a clinical codelist and a (2) timeframe, so variable names are following this  structure: `<name_of_codelist>_<time_frame>`.
    For example, consider the following description of denominator rule 2 for indicator BP002:

    |Rule number | Rule | Rule description or comments |
    |---| ---- | ---------------------------- |
    | 2 | If `BP_DAT` > (`PPED` – 5 years) | Select patients passed to this rule who had their blood pressure recorded in the 5 year period leading up to and including the payment period end date. Pass all remaining patients to the next rule. |

    This rule could be implemented like shown below, where the codelist *ht_max_codes* is defined in [analysis/codelists.py](analysis/codelists.py).
    
    ```
    bp002_denominator_r2=patients.satisfying(
        """
        bp_rec_5y
        """,
        bp_rec_5y=patients.with_these_clinical_events(
            codelist=bp_codes,
            between=[
                "first_day_of_month(index_date) - 5 years",
                "last_day_of_month(index_date)",
            ],
            returning="binary_flag",
            return_expectations={"incidence": 0.5},
        ),
    ),
    ```

  - Where the date of the variable will also be needed, we can make use of the `include_date_*` argument. 
  This includes the date associated with each event to the data (see [OpenSAFELY variable reference](https://docs.opensafely.org/study-def-variables/)).
  - The variables defined in these dictionaries can then be loaded as needed in individual study defintions using `** name_of_variable_dictionary,`.
### Study definitions

- The blood pressure indicator (BP002) is specified here: [analysis/study_definition_bp002.py](analysis/study_definition_bp002.py).
  The denominator and numerator rules are composed using variables from the dictionaries using the `patients.satisfying()` function to:
  1. Create a variable for each numerator and denominator rule (e.g., `bp002_denominator_r1`), where variables for each rule number are named following this structure: `<indicator>_<numerator/denominator>_<rule_number>`.
  2. These rule variables can then again be composed to create the numerator and denominator variables (e.g., `bp002_denominator`).

- Commonly used dates (e.g., '*Payment Period Start Date*') and variables used for breakdowns of results are defined in [analysis/config.py](analysis/config.py)

### Measures

The main results (montly percentage achievement per incicator) are calculated using the `Measure()` framework (see [OpenSAFELY documentation](https://docs.opensafely.org/measures/)).
The following results are calculated for each measure:
- Percentage achievement of:
  - the total target population: `measure_<condition_tag>_achievem_population_rate.csv`
  - different demographic and clinical breakdowns (see demographic_breakdowns list in [analysis/config.py](analysis/config.py)): `measure_<condition_tag>_achievem_<breakdown_tag>_breakdown_rate.csv`
  - individual GP practices; this data is only used to generate deciles using the reusable action [deciles-charts](https://github.com/opensafely-actions/deciles-charts)

### Actions

All scripted and reusable actions are defined in the [project.yaml](project.yaml).

* Each indicator has the following actions:
  * `generate_study_population_<condition_tag>`: Extracts study population
  * `generate_measures_<condition_tag>`: Generates measures using the `Measure()` framework (see [OpenSAFELY documentation](https://docs.opensafely.org/measures/))

# About the OpenSAFELY framework

Developers and epidemiologists interested in the framework should review [the OpenSAFELY documentation](https://docs.opensafely.org)
The OpenSAFELY framework is a Trusted Research Environment (TRE) for electronic
health records research in the NHS, with a focus on public accountability and
research quality.
Read more at [OpenSAFELY.org](https://opensafely.org).

# Licences
As standard, research projects have a MIT license. 
