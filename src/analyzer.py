# File: merge_ai_datasets.py
import pandas as pd
from pathlib import Path
from sklearn.preprocessing import MinMaxScaler

# Paths
DATA_DIR = Path(r"data/raw")
AI_INDEX_DIR = DATA_DIR / "2025_OXFORD_AI_REPORT" / "legacy"

# Load primary datasets
df_rise = pd.read_csv(DATA_DIR / "The_Rise_of_AI.csv")
df_jobs = pd.read_csv(DATA_DIR / "AI_JOB_TRENDS.csv")
df_popularity = pd.read_csv(DATA_DIR / "AI_ML_popularity.csv",encoding='latin1')

# Load AI Index CSVs
df_technical = pd.read_csv(AI_INDEX_DIR / "Technical_Performance_combined.csv")
df_technical['Year'] = pd.to_datetime(df_technical['Year'], errors='coerce').dt.year
df_technical = df_technical.fillna(0)

df_economy = pd.read_csv(AI_INDEX_DIR / "Economy_combined.csv",low_memory=False)
df_economy['Year'] = pd.to_datetime(df_economy['Year'], errors='coerce').dt.year
df_economy = df_economy.fillna(method='bfill')  # Fill NaNs with 0 for economy data

df_opinion = pd.read_csv(AI_INDEX_DIR / "Public_opinion_combined.csv")
df_opinion['Year'] = pd.to_datetime(df_opinion['Year'], errors='coerce').dt.year
df_opinion = df_opinion.fillna(0)

df_research = pd.read_csv(AI_INDEX_DIR / "Research_and_Development_combined.csv")
df_research = df_research.fillna(method='bfill')  # Fill NaNs with 0 for research output

# --- Step 1: Standardize columns and keep relevant features ---
def clean_yearly_df(df, year_col, rename_map):
    """
    Standardize Year column and rename selected columns.
    """
    df = df.copy()
    df[year_col] = df[year_col].astype(int)
    df.rename(columns=rename_map, inplace=True)
    return df

df_rise_filtered = clean_yearly_df(df_rise, "Year", {"AI Papers": "papers"})

df_research_filtered = clean_yearly_df(df_research, "Year", {"Research Output": "papers_ai_index"})
df_technical_filtered = clean_yearly_df(df_technical, "Year", {"Benchmark Score": "technical_score"})
df_economy_filtered = clean_yearly_df(df_economy, "Year", {"Investment (B$)": "investment"})
df_opinion_filtered = clean_yearly_df(df_opinion, "Year", {"Public Sentiment Score": "sentiment"})

# --- STEP 2: Process JOBS dataset (extract year & aggregate) ---
df_jobs['posting_date'] = pd.to_datetime(df_jobs['posting_date'], errors='coerce')
df_jobs['Year'] = df_jobs['posting_date'].dt.year
df_jobs_yearly = (
    df_jobs.groupby('Year')
    .agg({
        'salary_usd': 'mean',   # Avg salary
        'job_id': 'count'       # Job postings
    })
    .rename(columns={'job_id': 'jobs', 'salary_usd': 'avg_salary'})
    .reset_index()
)

# --- STEP 3: Process POPULARITY dataset (static feature) ---
# Compute mean popularity across all rows as a single feature
popularity_score = df_popularity['Ai and ML(Popularity)'].mean() if 'Ai and ML(Popularity)' in df_popularity.columns else None

# --- STEP 4: Merge datasets on Year ---
dfs = [df_rise, df_jobs_yearly, df_research, df_technical, df_economy, df_opinion]
merged_df = dfs[0]
for df in dfs[1:]:
    merged_df = pd.merge(merged_df, df, on="Year", how="outer")

# --- Step 5: Handle missing values ---
merged_df.sort_values("Year", inplace=True)
merged_df.fillna(method="ffill", inplace=True)  # Forward fill
merged_df.fillna(method="bfill", inplace=True)  # Backward fill if needed

# --- STEP 6: Add static popularity feature ---
if popularity_score is not None:
    merged_df['popularity_static'] = popularity_score

# --- Step 7: Normalize numeric features ---
scaler = MinMaxScaler()
numeric_cols = [col for col in merged_df.columns if col != "Year"]
merged_df[numeric_cols] = scaler.fit_transform(merged_df[numeric_cols])

# --- Step 8: Save cleaned dataset ---
merged_df.to_csv(DATA_DIR / "ai_future_merged.csv", index=False)
print("✅ Final merged dataset saved at: data/ai_future_merged.csv")