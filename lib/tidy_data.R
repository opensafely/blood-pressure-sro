#' Tidy categories in joint measures file
#'
#' @param df 
#' @param group 
#' @param category 
#' @param care_home 
#' @param learning_disability 
#' @param imd 
#' @param imd_explicit_na 
#' @param sex 
#' @param population 
#' @param long_labels 
#'
#' @return
#' @export
#'
#' @examples
tidy_category_names <- function(df,
                                group = NULL,
                                category = NULL,
                                care_home = NULL, 
                                learning_disability = NULL,
                                imd = NULL,
                                imd_explicit_na = TRUE,
                                sex = NULL,
                                population = NULL,
                                long_labels = FALSE) {
  
  # Convert to string 
  df <- df %>% 
    mutate({{ category }} := as.character({{ category }}))
  
  if (!is.null(population)) {
    df <- df %>% 
      mutate({{ category }} := case_when({{ group }} == {{ population }} ~ 
                                           as.character("Total"),
                                         TRUE ~ {{ category }}))
  }
  
  if (long_labels) {
    
    if (!is.null(care_home)) {
      
      df <- df %>%
        mutate({{ category }} := case_when({{ group }} == {{ care_home }} ~ 
                                             as.character(factor({{ category }},
                                                                 levels = c(TRUE, FALSE),
                                                                 labels = c("Record of positive care home status",
                                                                            "No record of positive care home status"))),
                                           TRUE ~ {{ category }}))
    }
    
    if (!is.null(learning_disability)) {
      df <- df %>%
        mutate({{ category }} := case_when({{ group }} == {{ learning_disability }} ~ 
                                             as.character(factor({{ category }},
                                                                 levels = c(TRUE, FALSE),
                                                                 labels = c("Record of learning disability",
                                                                            "No record of learning disability"))),
                                           TRUE ~ {{ category }}))
    }
    
  } else {
    
    if (!is.null(care_home)) {
      
      df <- df %>%
        mutate({{ category }} := case_when({{ group }} == {{ care_home }} ~ 
                                             as.character(factor({{ category }},
                                                                 levels = c(TRUE, FALSE),
                                                                 labels = c("Yes",
                                                                            "No"))),
                                           TRUE ~ {{ category }}))
    }
    
    if (!is.null(learning_disability)) {
      df <- df %>%
        mutate({{ category }} := case_when({{ group }} == {{ learning_disability }} ~ 
                                             as.character(factor({{ category }},
                                                                 levels = c(TRUE, FALSE),
                                                                 labels = c("Yes",
                                                                            "No"))),
                                           TRUE ~ {{ category }}))
    }
    
  }
  
  
  if (!is.null(imd)) {
    
    if (imd_explicit_na) {
      imd_levels <- c(0:5)
      imd_labels <- c("(Missing)",
                      "1 - Most deprived",
                      "2", "3", "4",
                      "5 - Least deprived")
    } else {
      imd_levels <- c(1:5)
      imd_labels <- c("1 - Most deprived",
                      "2", "3", "4",
                      "5 - Least deprived")
    }
    
    df <- df %>%
      mutate({{ category }} := case_when({{ group }} == {{ imd }} ~ 
                                           as.character(factor({{ category }},
                                                               levels = imd_levels,
                                                               labels = imd_labels)),
                                         TRUE ~ {{ category }}))
  }
  
  if (!is.null(sex)) {
    df <- df %>%
      mutate({{ category }} := case_when({{ group }} == {{ sex }} ~ 
                                           as.character(factor({{ category }},
                                                               levels = c("F", "M"),
                                                               labels = c("Female", "Male"))),
                                         TRUE ~ {{ category }}))
  }
  
  return(df)
  
}