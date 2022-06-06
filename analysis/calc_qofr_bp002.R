library(arrow)
library(here)
library(dplyr)
library(tidyr)
library(lubridate)
library(ggplot2)
library(magrittr)
library(readr)
library(skimr)


# Get file names and path for all input files ----
dir_input_bp002 <- fs::dir_ls(
    path = "output/joined",
    glob = "*input_bp002_*.csv$"
)

# Define select / reject logic for BP002 indicator
calc_bp002 <- function(df) {
    df %>%
        mutate(bp_002_denominator_r = case_when((bp002_denominator_r1 == TRUE &
                                                bp002_denominator_r2 == TRUE) |

                                                (bp002_denominator_r1 == TRUE &
                                                bp002_denominator_r3 == TRUE &
                                                bp002_denominator_r4 == TRUE)
                                                ~ TRUE,
                                                TRUE ~ FALSE),
                bp_002_numerator_r = case_when(bp_002_denominator_r == TRUE &
                                               bp002_denominator_r2 == TRUE
                                               ~ TRUE,
                                               TRUE ~ FALSE))
}

# 1. Read all input files
# 2. Valculate composite denominator (bp_002_denominator_r) and numerator (bp_002_numerator_r)
# 3. Write files
dir_input_bp002 %>%
    purrr::map(readr::read_csv) %>%
    purrr::map(calc_bp002) %>%
    purrr::walk2(dir_input_bp002, readr::write_csv)