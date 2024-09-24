library(binomialtrend)
library(tidyverse)



df <- read.csv("Scripts/Vegetation/TYC_data.csv")

# Run the trend analysis
#sort the data by year

#df <- df[order(df$Year)]
df<-df %>% arrange(Year)
df<-df %>% select(Attainment_Status)
attainment <- as.numeric(df$Attainment_Status)
print(attainment)
trend <- binomialtrend(attainment)

trend_df <- data.frame(trend_attainment = trend$parameter, p_value = trend$p.value)
print(trend_df)
write.csv(trend_df, "Scripts/Vegetation/Trend_Analysis.csv")
