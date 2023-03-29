# Can run from command line with Rscript ranksum.r (assume R/bin in PATH)
# data.csv has column headers, first column is "Groups" as 1 and 0, and others are variables
# can tolerate zeros but will return some errors if whole class is zero and NaN if whole variable is zero

# Load required library, use install.packages("dplyr") if not present
library(dplyr)

# Read in the csv file
data <- read.csv("data.csv")

# Split the data into two groups based on the first column
group_0 <- data %>% filter(Groups == 0) %>% select(-Groups)
group_1 <- data %>% filter(Groups == 1) %>% select(-Groups)

# Get the column names for the data frames
col_names <- colnames(group_0)

# Perform Wilcoxon rank sum test for each column
p_values <- sapply(col_names, function(col) {
  # Skip columns with only missing values
  if (sum(is.na(group_0[[col]])) == nrow(group_0) || sum(is.na(group_1[[col]])) == nrow(group_1)) {
    return(NA)
  }
  
  result <- wilcox.test(group_1[[col]], group_0[[col]], paired = FALSE)
  return(result$p.value)
})

# Correct p-values using Benjamini-Hochberg procedure
corrected_p_values <- p.adjust(p_values, method = "BH")

# Combine the p-values and corrected p-values into a data frame
results <- data.frame(col_names, p_values, corrected_p_values)

# Write the results to a csv file
write.csv(results, file = "results.csv", row.names = FALSE)
