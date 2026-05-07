import os
import pandas as pd
import numpy as np
from dotenv import load_dotenv

from acquire_data import main as acquire_data
from data_cleaning import load_data
from model_training import train_models

from sklearn.metrics import mean_squared_error, mean_absolute_error, r2_score

import subprocess


def main():

    print("\n🚀 Running full pipeline...\n")

    load_dotenv()

    # 1. DATA ACQUISITION
    print("📥 Step 1: Acquiring raw data...")
    acquire_data()

    # 2. DATA CLEANING + INTEGRATION
    print("\n🧹 Step 2: Cleaning + integrating data...")
    df = load_data()

    os.makedirs("data/processed", exist_ok=True)
    os.makedirs("outputs/models", exist_ok=True)

    df.to_csv("data/processed/cleaned_data.csv", index=False)
    print("✅ cleaned_data.csv saved in data/processed/")

    # 3. MERGE STATISTICS
    print("\n📊 Step 3: Computing merge statistics...")

    raw_sizes = {
        "DXY": len(pd.read_csv("data/raw/DXY.csv")),
        "VIX": len(pd.read_csv("data/raw/VIX.csv")),
        "FEDFUNDS": len(pd.read_csv("data/raw/FEDFUNDS.csv")),
        "ECB_RATE": len(pd.read_csv("data/raw/ECB_RATE.csv")),
        "TRADE_BAL": len(pd.read_csv("data/raw/TRADE_BAL.csv")),
        "USDJPY": len(pd.read_csv("data/raw/USDJPY.csv")),
        "AUDUSD": len(pd.read_csv("data/raw/AUDUSD.csv")),
    }

    cleaned_size = len(df)
    min_raw = min(raw_sizes.values())
    merge_rate = cleaned_size / min_raw

    print("\nMERGE STATISTICS")
    print("─" * 30)

    for name, size in raw_sizes.items():
        print(f"  {name}: {size}")

    print(f"\n  Final merged dataset: {cleaned_size} rows")
    print(f"  Merge rate (vs smallest dataset): {merge_rate:.2%}")

    with open("data/processed/merge_report.txt", "w") as f:
        f.write("MERGE STATISTICS\n")
        f.write("─" * 30 + "\n\n")
        for name, size in raw_sizes.items():
            f.write(f"{name}: {size}\n")
        f.write(f"\nFinal merged dataset: {cleaned_size}\n")
        f.write(f"Merge rate: {merge_rate:.2%}\n")

    print("✅ Merge report saved to data/processed/merge_report.txt")

    # 4. MODEL TRAINING
    print("\n🤖 Step 4: Training models...")
    best_HistGB, best_sarimax, best_linear_model, best_svr = train_models(TRAIN_AGAIN=False)

    # 5. MODEL PERFORMANCE
    print("\n📊 Step 5: Model performance summary...\n")

    X = df[['DXY', 'VIX', 'ECB_RATE', 'TRADE_DEFICIT', 'INT_DIFF', 'YEAR', 'MONTH', 'QUARTER', 'AUDJPY_LOG']]
    y = df['DXY_Diff']

    split = int(len(df) * 0.75)
    X_test = X.iloc[split:]
    y_test = y.iloc[split:]

    result_df = df.iloc[split:].copy()

    preds = {
        "Linear": np.exp(best_linear_model.predict(X_test)) * result_df["DXY"].values,
        "SVR": np.exp(best_svr.predict(X_test)) * result_df["DXY"].values,
        "HistGBR": np.exp(best_HistGB.predict(X_test)) * result_df["DXY"].values,
        "SARIMAX": np.exp(best_sarimax.forecast(steps=len(y_test), exog=X_test.values)) * result_df["DXY"].values,
    }

    actual = result_df["DXY_next"].values

    rows = []
    for name, y_pred in preds.items():
        rmse = np.sqrt(mean_squared_error(actual, y_pred))
        mae = mean_absolute_error(actual, y_pred)
        r2 = r2_score(actual, y_pred)
        print(f"  {name}")
        print(f"    RMSE: {rmse:.4f}")
        print(f"    MAE:  {mae:.4f}")
        print(f"    R²:   {r2:.4f}")
        print()
        rows.append({"model": name, "rmse": rmse, "mae": mae, "r2": r2})

    perf_df = pd.DataFrame(rows)
    perf_df.to_csv("outputs/model_performance.csv", index=False)
    print("✅ Model performance saved to outputs/model_performance.csv")

    # 6. SAVE PREDICTIONS FOR STREAMLIT
    for name, y_pred in preds.items():
        pred_df = pd.DataFrame({
            "date": result_df["DATE"].values,
            "actual": actual,
            "predicted": y_pred,
        })
        pred_df.to_csv(f"outputs/{name}_predictions.csv", index=False)

    print("✅ Predictions saved to outputs/")

    # 7. LAUNCH STREAMLIT APP
    print("\n📡 Step 7: Launching dashboard...")
    subprocess.run(["streamlit", "run", "scripts/app.py"])


if __name__ == "__main__":
    main()