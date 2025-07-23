import pandas as pd
import os
import numpy as np
from pathlib import Path

# Configuration
CORRELATION_THRESHOLD = 0.5  # Minimum correlation to include a column
TOP_N_COLUMNS = 15  # Maximum number of top correlation columns to keep
INCLUDE_IDENTIFIERS = True  # Whether to include identifier columns (Year, Date, etc.)

# Change to the project root directory to ensure relative paths work
project_root = Path(__file__).parent.parent
os.chdir(project_root)
print(f"Working directory: {os.getcwd()}")

INPUT_DIR = Path("data/raw/2025_OXFORD_AI_REPORT")
OUTPUT_DIR = Path("data/processed")
OUTPUT_DIR.mkdir(exist_ok=True)

print(f"Looking for files in: {INPUT_DIR.absolute()}")
print(f"Input directory exists: {INPUT_DIR.exists()}")
print(f"Output directory: {OUTPUT_DIR.absolute()}")
print(f"Configuration: correlation_threshold={CORRELATION_THRESHOLD}, top_n={TOP_N_COLUMNS}")

# List all CSV files in the directory
if INPUT_DIR.exists():
    csv_files = list(INPUT_DIR.glob("*_combined.csv"))
    print(f"Found {len(csv_files)} combined CSV files: {[f.name for f in csv_files]}")
else:
    print("Input directory does not exist!")
    exit(1)

def filter_top_correlation_columns(combined_file_path: Path, correlation_threshold: float = None, top_n: int = None):
    """
    Filter CSV file to include only columns with high correlations.
    
    Args:
        combined_file_path: Path to the input CSV file
        correlation_threshold: Minimum correlation threshold to include columns (uses global config if None)
        top_n: Maximum number of top correlation columns to keep (uses global config if None)
    
    Returns:
        Path to the filtered output file
    """
    if correlation_threshold is None:
        correlation_threshold = CORRELATION_THRESHOLD
    if top_n is None:
        top_n = TOP_N_COLUMNS
        
    try:
        df = pd.read_csv(combined_file_path, low_memory=False)
        print(f"\nProcessing file: {combined_file_path.name}")
        print(f"Original shape: {df.shape}")
        
        # Convert numeric string columns to float where possible
        for col in df.columns:
            if df[col].dtype == 'object':
                # Try to convert to numeric, keep as string if it fails
                numeric_series = pd.to_numeric(df[col], errors='coerce')
                if not numeric_series.isna().all():  # If at least some values can be converted
                    df[col] = numeric_series
        
        # Get numeric columns for correlation analysis
        numeric_cols = df.select_dtypes(include=['float64', 'int64']).columns.tolist()
        
        if len(numeric_cols) < 2:
            print(f"Not enough numeric columns ({len(numeric_cols)}) for correlation analysis. Keeping original file.")
            # Copy original file to processed directory
            output_path = OUTPUT_DIR / f"filtered_{combined_file_path.name}"
            df.to_csv(output_path, index=False)
            return output_path
        
        print(f"Found {len(numeric_cols)} numeric columns for correlation analysis")
        
        # Calculate correlation matrix and get mean absolute correlations
        corr_matrix = df[numeric_cols].corr()
        
        # Remove self-correlations (diagonal) by setting them to NaN
        np.fill_diagonal(corr_matrix.values, np.nan)
        
        # Calculate mean absolute correlation for each column (excluding NaN)
        mean_abs_corr = corr_matrix.abs().mean(skipna=True).sort_values(ascending=False)
        
        # Filter out columns with NaN correlations (usually single-value columns)
        mean_abs_corr = mean_abs_corr.dropna()
        
        print("\nTop correlations (mean absolute correlation with other columns):")
        print(mean_abs_corr.head(min(20, len(mean_abs_corr))))
        
        # Select top correlation columns
        top_corr_cols = mean_abs_corr[mean_abs_corr >= correlation_threshold].head(top_n).index.tolist()
        
        if not top_corr_cols:
            print(f"No columns meet correlation threshold {correlation_threshold}. Using top {min(top_n, len(mean_abs_corr))} columns.")
            top_corr_cols = mean_abs_corr.head(min(top_n, len(mean_abs_corr))).index.tolist()
        
        # Include any important identifier columns (like Year, Date, etc.) that aren't numeric
        identifier_cols = []
        if INCLUDE_IDENTIFIERS:
            potential_identifiers = ['year', 'date', 'time', 'period', 'country', 'region', 'state', 'id']
            for col in df.columns:
                if any(identifier in col.lower() for identifier in potential_identifiers):
                    if col not in top_corr_cols:
                        identifier_cols.append(col)
        
        # Combine identifier columns with top correlation columns
        selected_columns = identifier_cols + top_corr_cols
        
        print(f"\nSelected columns ({len(selected_columns)}):")
        print("Identifier columns:", identifier_cols)
        print("Top correlation columns:", top_corr_cols)
        
        # Create filtered dataframe
        filtered_df = df[selected_columns].copy()
        
        # Save filtered file
        output_path = OUTPUT_DIR / f"filtered_{combined_file_path.name}"
        filtered_df.to_csv(output_path, index=False)
        
        print(f"Filtered shape: {filtered_df.shape}")
        print(f"Saved to: {output_path}")
        print(f"Reduction: {df.shape[1] - filtered_df.shape[1]} columns removed")
        
        return output_path
        
    except Exception as e:
        print(f"Error processing {combined_file_path.name}: {e}")
        return None

def main():
    """Main function to process all combined CSV files."""
    print("\n" + "="*60)
    print("FILTERING CSV FILES TO TOP CORRELATION COLUMNS")
    print("="*60)
    
    processed_files = []
    
    for file_path in INPUT_DIR.glob("*_combined.csv"):
        output_path = filter_top_correlation_columns(file_path)
        if output_path:
            processed_files.append(output_path)
        print("-" * 60)
    
    print("\nProcessing complete!")
    print(f"Processed {len(processed_files)} files:")
    for file_path in processed_files:
        print(f"  - {file_path.name}")
    
    print(f"\nAll filtered files saved to: {OUTPUT_DIR.absolute()}")

def analyze_filtered_files():
    """Analyze the filtered CSV files to show the results of filtering."""
    print("\n" + "="*60)
    print("ANALYSIS OF FILTERED FILES")
    print("="*60)
    
    if not OUTPUT_DIR.exists():
        print("No processed files found. Run main() first.")
        return
    
    filtered_files = list(OUTPUT_DIR.glob("filtered_*.csv"))
    
    for file_path in filtered_files:
        try:
            df = pd.read_csv(file_path)
            print(f"\nFile: {file_path.name}")
            print(f"Shape: {df.shape}")
            print(f"Columns: {df.columns.tolist()}")
            
            # Show basic statistics for numeric columns
            numeric_cols = df.select_dtypes(include=['float64', 'int64']).columns
            if len(numeric_cols) > 0:
                print(f"Numeric columns ({len(numeric_cols)}): {numeric_cols.tolist()}")
                print("Basic statistics:")
                print(df[numeric_cols].describe())
            print("-" * 60)
            
        except Exception as e:
            print(f"Error analyzing {file_path.name}: {e}")

if __name__ == "__main__":
    main()
    
    # Optionally analyze the filtered files
    print("\nWould you like to see detailed analysis of filtered files? (y/n)")
    # For automated execution, we'll just run the analysis
    analyze_filtered_files()