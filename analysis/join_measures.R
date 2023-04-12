# This scrip loads all measure files and
# (1) joins them together
# (2) rounds counts to the nearest 10
# (3) recalculate value after rounding

# Note that the ungrouped measure (population) and grouped measures
# differ in the number of their variables

# Load packages ----
library(magrittr)
source(here::here("lib", "funs.R"))
fs::dir_create(here::here("output", "joined", "measures"))

# Get file names and path ----
bp002_1y_achievem_breakdown_measures <- fs::dir_ls(
  path = "output/joined",
  glob = "*measure_bp002_1y_achievem_*_breakdown_rate.csv$"
)

bp002_5y_achievem_breakdown_measures <- fs::dir_ls(
  path = "output/joined",
  glob = "*measure_bp002_5y_achievem_*_breakdown_rate.csv$"
)

# Remove practice level data from achievement measures
bp002_1y_achievem_breakdown_measures <- bp002_1y_achievem_breakdown_measures[!stringr::str_detect(bp002_1y_achievem_breakdown_measures, "practice")]
bp002_5y_achievem_breakdown_measures <- bp002_5y_achievem_breakdown_measures[!stringr::str_detect(bp002_5y_achievem_breakdown_measures, "practice")]

bp002_1y_achievem_population_measures <- fs::dir_ls(
  path = "output/joined",
  glob = "*measure_bp002_1y_achievem_population_rate.csv$"
)

bp002_5y_achievem_population_measures <- fs::dir_ls(
  path = "output/joined",
  glob = "*measure_bp002_5y_achievem_population_rate.csv$"
)

# read bp002 1y lookback data
df_bp002_1y_achievem_population <- read_population_measures(bp002_1y_achievem_population_measures)
df_bp002_1y_achievem_breakdown <- read_breakdown_measures(bp002_1y_achievem_breakdown_measures)
df_bp002_1y_achievem <- dplyr::bind_rows(df_bp002_1y_achievem_population, df_bp002_1y_achievem_breakdown) %>%
  dplyr::mutate(lookback = "1y")

df_bp002_5y_achievem_population <- read_population_measures(bp002_5y_achievem_population_measures)
df_bp002_5y_achievem_breakdown <- read_breakdown_measures(bp002_5y_achievem_breakdown_measures)
df_bp002_5y_achievem <- dplyr::bind_rows(df_bp002_5y_achievem_population, df_bp002_5y_achievem_breakdown) %>%
  dplyr::mutate(lookback = "5y")

df_bp002_achievem <- dplyr::bind_rows(df_bp002_1y_achievem, df_bp002_5y_achievem)

df_bp002_achievem <- df_bp002_achievem %>%
  round_variables(c("bp002_numerator", "bp002_denominator", "population")) %>%
  dplyr::mutate(value = bp002_numerator / bp002_denominator)

readr::write_csv(
  df_bp002_achievem,
  here::here("output", "joined", "measures", "measures_bp002_achievem.csv")
)
