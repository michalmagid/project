# Install and load necessary packages

library(readxl)
library(afex)

library(ez)
# Read the Excel file
file_path2 <-"C:/Users/USER/Documents/annova_test/80_transformed_data.xlsx"
data2 <- read_excel(file_path2)
# Display the original data to verify structure
print(head(data2))

# Convert columns to factors
data2$Photo_Type <- as.factor(data2$Photo_Type)
data2$Color <- as.factor(data2$Color)
data2$Photo_ID <- as.factor(data2$Photo_ID)

# Conduct the two-way mixed ANOVA
anova_result <- ezANOVA(
  data = data2,
  dv = .(Score),             # Dependent variable
  wid = .(Photo_ID),         # Subject identifier
  within = .(Color),         # Within-subject factor
  between = .(Photo_Type),   # Between-subject factor
  type = 3                   # Type III sum of squares
)

# Check the results
print(anova_result)

library(ggplot2)
library(dplyr)  # Ensure dplyr is loaded for data manipulation
summary_data <- data2 %>%
  group_by(Photo_Type, Color) %>%
  summarise(mean_score = mean(Score), .groups = 'drop')
# Create the interaction plot
interaction_plot <-ggplot(summary_data, aes(x = Photo_Type, y = mean_score, color = Color, group = Color)) +
  geom_line(linewidth = 1) +
  geom_point(size = 3) +
  labs(
    title = "Interaction Plot",
    x = "Photo Type",
    y = "Mean Score"
  ) +
  theme_minimal() +
  scale_color_manual(values = c("blue", "red"))


# Display the plot
print(interaction_plot)

# Create the violin plot
violin_plot <- ggplot(data2, aes(x = interaction(Photo_Type, Color), y = Score, fill = Color)) +
  geom_violin(trim = FALSE) +
  geom_boxplot(width = 0.1, position = position_dodge(0.9)) +
  labs(
    title = "Score Distribution by foodness & colorness",
    x = "Photo Type and Color",
    y = "Score"
  ) +
  theme_minimal() +
  scale_fill_manual(values = c("blue", "red")) +
  theme(axis.text.x = element_text(angle = 45, hjust = 1))

# Display the plot
print(violin_plot)

