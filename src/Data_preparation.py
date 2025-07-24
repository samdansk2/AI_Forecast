
# file: ai_data_preprocessor.py

import pandas as pd

class AIDataPreprocessor:
    def __init__(self, paths: dict):
        """
        paths: dict with dataset file paths
        Example:
        {
          'jobs': 'AI_JOB_TRENDS.csv',
          'popularity': 'AI_ML_POPULARITY.csv',
          'rise_ai': 'THE_RISE_OF_AI.csv',
          'economy': 'economy.csv',
          'public_opinion': 'public_opinion.csv',
          'rnd': 'rnd.csv'
        }
        """
        self.paths = paths
        self.dataframes = {}
        self.master_df = None

    @staticmethod
    def _clean_numeric(series):
        """Remove non-numeric characters and convert to float."""
        return pd.to_numeric(series.astype(str).str.replace('[^0-9.\-]', '', regex=True), errors='coerce')

    def load_data(self):
        """Load all datasets into a dictionary."""
        for name, path in self.paths.items():
            try:
             self.dataframes[name] = pd.read_csv(path)
            except UnicodeDecodeError:
                # Try to read with a different encoding if the default fails
                self.dataframes[name] = pd.read_csv(path,encoding='latin1')

    def clean_data(self, dataset_name: str):
        """Clean and aggregate data by Year for a given dataset."""
        df = self.dataframes[dataset_name]

        # Normalize Year if exists
        if 'Year' in df.columns:
            df['Year'] = pd.to_numeric(df['Year'], errors='coerce')

        if dataset_name == 'jobs':
            df['posting_date'] = pd.to_datetime(df['posting_date'], errors='coerce')
            df['Year'] = df['posting_date'].dt.year
            df = df.groupby('Year', as_index=False)['salary_usd'].mean()
            df.rename(columns={'salary_usd': 'Avg Salary USD'}, inplace=True)

        elif dataset_name == 'popularity':
            if 'Year' not in df.columns:
                df['Year'] = pd.to_datetime('today').year
            if 'Popularity' in df.columns:
                df['Popularity'] = self._clean_numeric(df['Popularity'])
            df = df.groupby('Year', as_index=False)['Popularity'].mean()

        elif dataset_name == 'rise_ai':
            keep_cols = ['Year', 'Global AI Market Value(in Billions)', 'AI Adoption (%)']
            df = df[keep_cols]
            df['Global AI Market Value(in Billions)'] = self._clean_numeric(df['Global AI Market Value(in Billions)'])
            df['AI Adoption (%)'] = self._clean_numeric(df['AI Adoption (%)'])
            df.rename(columns={
                'Global AI Market Value(in Billions)': 'AI Market Value (Billions)',
                'AI Adoption (%)': 'AI Adoption %'
            }, inplace=True)
            df = df.groupby('Year', as_index=False).mean()

        elif dataset_name == 'economy':
            keep_cols = ['Year', 'Number of AI Job Postings', 'Total investment (in billions of US dollars)']
            df = df[keep_cols]
            df['Number of AI Job Postings'] = self._clean_numeric(df['Number of AI Job Postings'])
            df['Total investment (in billions of US dollars)'] = self._clean_numeric(df['Total investment (in billions of US dollars)'])
            df.rename(columns={
                'Number of AI Job Postings': 'AI Job Postings',
                'Total investment (in billions of US dollars)': 'AI Investment (Billions)'
            }, inplace=True)
            df = df.groupby('Year', as_index=False).sum()

        elif dataset_name == 'public_opinion':
            keep_cols = ['Year', '% of respondents that “agree”']
            df = df[keep_cols]
            df['% of respondents that “agree”'] = self._clean_numeric(df['% of respondents that “agree”'])
            df.rename(columns={'% of respondents that “agree”': 'Public Opinion %'}, inplace=True)
            df = df.groupby('Year', as_index=False).mean()

        elif dataset_name == 'rnd':
            keep_cols = ['Year', 'Number of AI publications (in thousands)', 'Number of AI patents granted (in thousands)']
            df = df[keep_cols]
            df['Number of AI publications (in thousands)'] = self._clean_numeric(df['Number of AI publications (in thousands)'])
            df['Number of AI patents granted (in thousands)'] = self._clean_numeric(df['Number of AI patents granted (in thousands)'])
            df.rename(columns={
                'Number of AI publications (in thousands)': 'AI Publications (K)',
                'Number of AI patents granted (in thousands)': 'AI Patents (K)'
            }, inplace=True)
            df = df.groupby('Year', as_index=False).sum()

        df['Year'] = df['Year'].astype('Int64')
        self.dataframes[dataset_name] = df

    def merge_all(self):
        """Merge all cleaned datasets on Year."""
        dfs = list(self.dataframes.values())
        df = dfs[0]
        for next_df in dfs[1:]:
            df = df.merge(next_df, on='Year', how='outer')

        df.sort_values('Year', inplace=True)
        df.reset_index(drop=True, inplace=True)
        df.fillna(method='ffill', inplace=True)
        self.master_df = df

    def feature_engineering(self):
        """Add YoY growth rate features for numeric columns."""
        if self.master_df is None:
            raise ValueError("Run merge_all() before feature_engineering()")

        for col in ['AI Market Value (Billions)', 'AI Job Postings', 'AI Investment (Billions)']:
            if col in self.master_df.columns:
                self.master_df[f'{col} YoY Growth'] = self.master_df[col].pct_change()

        self.master_df.fillna(0, inplace=True)

    def get_cleaned_data(self):
        """Return the final merged and processed dataframe."""
        return self.master_df
    
if __name__ == "__main__":
    paths = {
        'jobs': 'data/raw/AI_JOB_TRENDS.csv',
        'popularity': 'data/raw/AI_ML_popularity.csv',
        'rise_ai': 'data/raw/The_Rise_of_AI.csv',
        'economy': 'data/raw/2025_OXFORD_AI_REPORT/Economy_combined.csv',
        'public_opinion': 'data/raw/2025_OXFORD_AI_REPORT/Public_Opinion_combined.csv',
        'rnd': 'data/raw/2025_OXFORD_AI_REPORT/Research_and_Development_combined.csv'
    }

    processor = AIDataPreprocessor(paths)
    processor.load_data()

    for name in paths.keys():
        processor.clean_data(name)

    processor.merge_all()
    processor.feature_engineering()
    final_df = processor.get_cleaned_data()
    final_df.to_csv('AI_data_prepared.csv', index=False)