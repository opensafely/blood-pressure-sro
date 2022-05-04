library(magrittr)

# Create dir if needed
fs::dir_create(here::here("output", "joined", "measures"))

# Get file paths
dir_bp002_deciles_tables <- fs::dir_ls(
    path = "output",
    glob = "*deciles_table_bp002_*.csv$"
)

# Read all data
df_deciles_tables <- purrr::map_dfr(dir_bp002_deciles_tables,
               readr::read_csv,
               .id = "file_name")

# Change file name string
df_deciles_tables <- df_deciles_tables %>% 
  dplyr::mutate(file_name = stringr::str_replace(file_name, "output/deciles_table_", ""),
                file_name = stringr::str_replace(file_name, "_rate.csv", "")) %>% 
  dplyr::rename(measure = file_name)

readr::write_csv(df_deciles_tables,
                 here::here("output", "joined", "measures", "measures_bp002_deciles_tables.csv"))
