import os
import pandas as pd
import hashlib
from fredapi import Fred
from dotenv import load_dotenv

load_dotenv()

def save_checksum(df, path):
    checksum = hashlib.sha256(
        pd.util.hash_pandas_object(df, index=True).values
    ).hexdigest()

    with open(path, "w") as f:
        f.write(checksum)

    return checksum


def save_series(series, name):
    df = series.to_frame(name)
    df.index.name = "DATE"
    df.index = pd.to_datetime(df.index)
    df = df.sort_index()
    # Filter from 2006 onward
    df = df[df.index >= "2006-01-01"]

    os.makedirs("data/raw", exist_ok=True)

    csv_path = f"data/raw/{name}.csv"
    df.to_csv(csv_path)

    checksum = save_checksum(df, f"data/raw/{name}_checksum.txt")

    print(f"Saved {name} | rows={len(df)} | checksum={checksum}")


def main():

    api_key = os.getenv("FRED_API_KEY")
    fred = Fred(api_key)

    print("\n📥 Downloading raw datasets from FRED...\n")

    datasets = {
        "DXY": "DTWEXBGS",
        "VIX": "VIXCLS",
        "FEDFUNDS": "FEDFUNDS",
        "ECB_RATE": "ECBDFR",
        "TRADE_BAL": "BOPGSTB",
        "USDJPY" : "DEXJPUS",
        "AUDUSD" : "DEXUSAL"
    }

    for name, series_id in datasets.items():
        try:
            series = fred.get_series(series_id)
            save_series(series, name)
        except Exception as e:
            print(f"❌ Failed to fetch {name} ({series_id}): {e}")

    print("\n✅ Raw data acquisition complete.")


if __name__ == "__main__":
    main()