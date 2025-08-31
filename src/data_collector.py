# Merge The_Rise_of_AI and AI_ML_popularity datasets

import pandas as pd
import numpy as np

# Load cleaned datasets
df_rise = pd.read_csv(r'data\processed\cleaned_The_Rise_of_AI.csv')
df_popularity = pd.read_csv(r'data\processed\cleaned_AI_ML_popularity.csv')

# 1. Compute Popularity Trend
# =========================
# If AI_ML_popularity has no year column, create synthetic yearly trend based on rows count
years = pd.to_datetime(df_rise['Year']).dt.year.tolist()

# Calculate overall mean popularity for baseline
pop_cols = ['CountryPopularity', 'CityPopularity', 'Popularity', 'Popularity.1']
popularity_values = []
for col in pop_cols:
    if col in df_popularity.columns:
        popularity_values.append(df_popularity[col].dropna().mean())

# Compute average popularity
avg_popularity = np.mean(popularity_values) if popularity_values else 50.0

# Create synthetic trend: increasing popularity over years
trend_step = 5  # assume popularity grows by 5 units per year
popularity_trend = [avg_popularity + i*trend_step for i in range(len(years))]

# =========================
# 2. Build merged DataFrame
# =========================
df_merged = pd.DataFrame({
    'Year': years,
    'Market_Value': df_rise['Global AI Market Value(in Billions)'],
    'AI_Adoption': df_rise['AI Adoption (%)'],
    'Popularity_Score': popularity_trend
})

# =========================
# 3. Save merged dataset
# =========================
df_merged.to_csv('merged_AI_trend_popularity.csv', index=False)
print("Merged DataFrame created with temporal popularity trend:")
print(df_merged)
print("\nFile saved as merged_AI_trend_popularity.csv")
