# Join measures
# This scrip loads all measure files and 
# (1) joins them together
# (2) rounds counts to the nearest 10

# Note that the ungrouped measure (population) and grouped measures
# differ in the number of their variables

# Load packages ----
library(magrittr)
library(dplyr)
library(tidyr)
library(here)
library(readr)
library(fs)
library(purrr)
library(stringr)

# Get file names and path ----
dir_bp_002_measures <- fs::dir_ls(path = "output/",
                                   glob = "*rate_table*.csv$")
dir_bp_002_measures
# Split dir paths because file structure differes
## Grouped measures (excluding practice)
dir_bp_002_measures_groups <- dir_bp_002_measures[!stringr::str_detect(dir_bp_002_measures, "total")]
dir_bp_002_measures_groups <- dir_bp_002_measures_groups[!stringr::str_detect(dir_bp_002_measures_groups, "practice")]
dir_bp_002_measures_groups <- dir_bp_002_measures_groups[!stringr::str_detect(dir_bp_002_measures_groups, "event_code")]

## Population measure
dir_bp_002_measures_pop <- dir_bp_002_measures[stringr::str_detect(dir_bp_002_measures, "total")]

# Load files ----
## Load grouped measures
## Pivot longer so variable names are identical across measure files
df_bp_002_measures_groups <- dir_bp_002_measures_groups %>%
  purrr::map(readr::read_csv) %>%
  purrr::map_dfr(tidyr::pivot_longer,
                 cols = 1,
                 names_to = "group",
                 values_to = "category",
                 values_transform = list(category = as.character))

# Load population measure ---
# Add variables that are missing compared to grouped measures
df_bp_002_measures_pop <- readr::read_csv(here::here(dir_bp_002_measures_pop)) %>%
  dplyr::mutate(group = "population",
                category = "population")

# Join all measures into one object ---
df_bp_002_measures <- df_bp_002_measures_groups %>%
  dplyr::bind_rows(df_bp_002_measures_pop)

# Write hyp001 csv file
## First create subdirectory (if it doesn't exist)
fs::dir_create(here::here("output", "measures"))

# Round counts to the nearest 10
df_bp_002_measures <- df_bp_002_measures %>%
   dplyr::mutate(dplyr::across(c("event", "population"), round, -1))

## Next, write csv file
readr::write_csv(df_bp_002_measures,
                 here::here("output", "measures", "measures_bp002.csv"))
