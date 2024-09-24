library(binomialtrend)
library(tidyverse)



df <- read.csv("Scripts/Vegetation/TYC_data.csv")

# Run the trend analysis
#sort the data by year

#df <- df[order(df$Year)]
df<-df %>% arrange(Year)
df<-df %>% select(Attainment_Status, Relation_to_Threshold)
attainment <- as.numeric(df$Attainment_Status)
trend <- binomialtrend(attainment)
trend_df <- data.frame(trend_attainment = trend$parameter, p_value = trend$p.value)
write.csv(trend_df, "Scripts/Vegetation/Trend_Analysis_Binary.csv")

site_proportion <- df$Relation_to_Threshold
trend_site_proportion <- binomialtrend(site_proportion)
trend_site_proportion_df <- data.frame(trend_attainment = trend_site_proportion$parameter,
p_value = trend_site_proportion$p.value)
write.csv(trend_site_proportion_df, "Scripts/Vegetation/Trend_Analysis_Site_Proportion.csv")
