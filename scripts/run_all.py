import os
import pandas as pd
from dotenv import load_dotenv

from acquire_data import main as acquire_data
from data_cleaning import load_data
from model_training import train_models

import subprocess

def main():

    print("\n🚀 Running full pipeline...\n")

    load_dotenv()
    api_key = os.getenv("FRED_API_KEY")

    # 1. DATA ACQUISITION
    print("📥 Step 1: Acquiring raw data...")
    acquire_data()   # saves raw data + checksum

    # 2. DATA CLEANING + INTEGRATION
    print("🧹 Step 2: Cleaning + integrating data...")
    df = load_data()
    
    os.makedirs("data/processed", exist_ok=True)
    os.makedirs("outputs", exist_ok=True)

    df.to_csv("data/processed/cleaned_data.csv", index=False)
    print("✅ cleaned_data.csv saved in data/processed/")

    # 3. MERGE STATISTICS
    print("\n📊 Step 3: Computing post-merge statistics...")

    raw_sizes = {
        "DXY": len(pd.read_csv("data/raw/DXY.csv")),
        "VIX": len(pd.read_csv("data/raw/VIX.csv")),
        "FEDFUNDS": len(pd.read_csv("data/raw/FEDFUNDS.csv")),
        "ECB_RATE": len(pd.read_csv("data/raw/ECB_RATE.csv")),
        "TRADE_BAL": len(pd.read_csv("data/raw/TRADE_BAL.csv")),
    }

    cleaned_size = len(df)
    min_raw = min(raw_sizes.values())
    merge_rate = cleaned_size / min_raw

    print("\nMERGE STATISTICS")
    print("----------------------")

    for name, size in raw_sizes.items():
        print(f"{name}: {size}")

    print(f"\nFinal merged dataset: {cleaned_size} rows")
    print(f"Merge rate (vs smallest dataset): {merge_rate:.2%}")

    # Save report
    with open("outputs/post_merge_report.txt", "w") as f:
        f.write("MERGE STATISTICS\n")
        f.write("----------------------\n\n")

        for name, size in raw_sizes.items():
            f.write(f"{name}: {size}\n")

        f.write(f"\nFinal merged dataset: {cleaned_size}\n")
        f.write(f"Merge rate: {merge_rate:.2%}\n")

    print("✅ Merge report saved to outputs/post_merge_report.txt")

    
    # 4. MODEL TRAINING
    print("🤖 Step 3: Training models...")
    results = train_models(df)

    print("\n📊 Model Performance Summary:")
    print(results)


    # 5. LAUNCH STREAMLIT APP
    print("\n📡 Step 4: Launching dashboard...")
    subprocess.run(["streamlit", "run", "app.py"])


if __name__ == "__main__":
    main() 