import os
from dotenv import load_dotenv

from acquire_data import main as acquire_data
from data_cleaning import load_data
from model_training import train_models

import subprocess

def main():

    print("\n🚀 Running full pipeline...\n")

    load_dotenv()
    api_key = os.getenv("FRED_API_KEY")

    # ----------------------------
    # 1. DATA ACQUISITION
    # ----------------------------
    print("📥 Step 1: Acquiring raw data...")
    acquire_data()   # saves raw data + checksum

    # ----------------------------
    # 2. LOAD + CLEAN + INTEGRATE
    # ----------------------------
    print("🧹 Step 2: Cleaning + integrating data...")
    df = load_data()
    
    os.makedirs("data/processed", exist_ok=True)
    os.makedirs("outputs", exist_ok=True)

    df.to_csv("data/processed/cleaned_data.csv", index=False)
    print("✅ cleaned_data.csv saved in data/processed/")

    # ----------------------------
    # 3. MODEL TRAINING
    # ----------------------------
    print("🤖 Step 3: Training models...")
    results = train_models(df)

    print("\n📊 Model Performance Summary:")
    print(results)

    # ----------------------------
    # 4. LAUNCH STREAMLIT APP
    # ----------------------------
    print("\n📡 Step 4: Launching dashboard...")
    subprocess.run(["streamlit", "run", "app.py"])


if __name__ == "__main__":
    main() 