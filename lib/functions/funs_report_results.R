#' Report count and percentage of measures
#'
#' @param df Data frame. Requires the variables named "date", "group", "category" used for filtering
#' @param var_value Name of variable with count or percent values
#' @param date String, specifying value for filtering date
#' @param group String, specifying value for filtering date
#' @param category String, specifying value for filtering date
#' @param convert_percent Logical, whether to convert percent (0.1) to 10.00%
#'
#' @return
#' @export
#'
#' @examples
report_measures <- function(df, 
                            var_value, 
                            filter_date, filter_group, filter_category, 
                            convert_percent = TRUE) {
  
  report_value <- df %>% 
    filter(date == filter_date) %>% 
    filter(group == filter_group) %>% 
    filter(category == filter_category) %>% 
    pull({{ var_value }})
  
  if (convert_percent) {
    
    if (report_value <= 1) {
      report_value <-  scales::percent(report_value, accuracy = 0.01)
    } else {
        warning(paste0("value is greater than 1 (", report_value, ") and not converted to %."), 
                call. = FALSE)
      }
    }
  
  return(report_value)
  
  }