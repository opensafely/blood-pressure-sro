read_breakdown_measures <- function(measures_dir) {
  
  df_breakdown_measures <- measures_dir %>%
    purrr::map(readr::read_csv) %>%
    purrr::map_dfr(tidyr::pivot_longer,
                   cols = 1,
                   names_to = "group",
                   values_to = "category",
                   values_transform = list(category = as.character))
  
  if(length(names(df_breakdown_measures)) > 6) {
    stop("Unexpected number of returned variables. Check that all measures have the same variable names.", call. = FALSE)
  }
  
  df_breakdown_measures
  
}

read_population_measures <- function(measures_dir) {
  
  readr::read_csv(here::here(measures_dir)) %>%
    dplyr::mutate(group = "population",
                  category = "population")
  
}


round_variables <- function(df, var_list, digits = -1) {

    dplyr::mutate(df, dplyr::across(!!var_list, round, digits))

}
