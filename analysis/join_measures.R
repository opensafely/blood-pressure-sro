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
bp002_excl_breakdown_dr3_measures <- fs::dir_ls(
  path = "output/joined",
  glob = "*measure_bp002_excl_denominator_r3_*_breakdown_rate.csv$"
)

bp002_excl_population_dr3_measures <- fs::dir_ls(
  path = "output/joined",
  glob = "*measure_bp002_excl_denominator_r3_population_rate.csv$"
)

bp002_excl_breakdown_dr4_measures <- fs::dir_ls(
  path = "output/joined",
  glob = "*measure_bp002_excl_denominator_r4_*_breakdown_rate.csv$"
)

bp002_excl_population_dr4_measures <- fs::dir_ls(
  path = "output/joined",
  glob = "*measure_bp002_excl_denominator_r4_population_rate.csv$"
)

bp002_achievem_breakdown_measures <- fs::dir_ls(
  path = "output/joined",
  glob = "*measure_bp002_achievem_*_breakdown_rate.csv$"
)

# Remove practice level data from achievement measures
bp002_achievem_breakdown_measures <- bp002_achievem_breakdown_measures[!stringr::str_detect(bp002_achievem_breakdown_measures, "practice")]

bp002_achievem_population_measures <- fs::dir_ls(
  path = "output/joined",
  glob = "*measure_bp002_achievem_population_rate.csv$"
)

df_bp002_achievem_population <- read_population_measures(bp002_achievem_population_measures)
df_bp002_achievem_breakdown <- read_breakdown_measures(bp002_achievem_breakdown_measures)

df_bp002_achievem <- dplyr::bind_rows(df_bp002_achievem_population, df_bp002_achievem_breakdown)

df_bp002_achievem <- df_bp002_achievem %>%
  round_variables(c("bp002_numerator", "bp002_denominator", "population")) %>%
  dplyr::mutate(value = bp002_numerator / bp002_denominator)

readr::write_csv(
  df_bp002_achievem,
  here::here("output", "joined", "measures", "measures_bp002_achievem.csv")
)

df_bp002_excl_dr3_population <- read_population_measures(bp002_excl_population_dr3_measures) %>%
  dplyr::mutate(excl_rule = "bp002_denom_r3") %>%
  dplyr::rename(excl_denominator = bp002_excl_denominator_r3)

df_bp002_excl_dr4_population <- read_population_measures(bp002_excl_population_dr4_measures) %>%
  dplyr::mutate(excl_rule = "bp002_denom_r4") %>%
  dplyr::rename(excl_denominator = bp002_excl_denominator_r4)

df_bp002_excl_dr3_breakdown <- read_breakdown_measures(bp002_excl_breakdown_dr3_measures) %>%
  dplyr::mutate(excl_rule = "bp002_denom_r3") %>%
  dplyr::rename(excl_denominator = bp002_excl_denominator_r3)

df_bp002_excl_dr4_breakdown <- read_breakdown_measures(bp002_excl_breakdown_dr4_measures) %>%
  dplyr::mutate(excl_rule = "bp002_denom_r4") %>%
  dplyr::rename(excl_denominator = bp002_excl_denominator_r4)

df_bp002_excl <- dplyr::bind_rows(
  df_bp002_excl_dr3_population,
  df_bp002_excl_dr3_breakdown,
  df_bp002_excl_dr4_population,
  df_bp002_excl_dr4_breakdown
)

df_bp002_excl <- df_bp002_excl %>%
  round_variables(c("excl_denominator", "population")) %>%
  dplyr::mutate(value = excl_denominator / population)

readr::write_csv(
  df_bp002_excl,
  here::here("output", "joined", "measures", "measures_bp002_excl.csv")
)
