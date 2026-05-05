import pandas as pd
import numpy as np

# Load raw data

def load_raw_data():

    def read_raw(name):
        path = f"data/raw/{name}.csv"
        df = pd.read_csv(path)

        df["DATE"] = pd.to_datetime(df["DATE"])
        df = df.sort_values("DATE")

        df = df.set_index("DATE")
        return df

    dxy   = read_raw("DXY")
    vix   = read_raw("VIX")
    ff    = read_raw("FEDFUNDS")
    ecb   = read_raw("ECB_RATE")
    trade = read_raw("TRADE_BAL")

    return dxy, vix, ff, ecb, trade


# Clean datasets and integrate them into a single dataset

def load_data():

    dxy, vix, ff, ecb, trade = load_raw_data()

    # Monthly alignment 
    dxy   = dxy.resample("ME").last()
    vix   = vix.resample("ME").mean()
    ff    = ff.resample("ME").last()
    ecb   = ecb.resample("ME").last()
    trade = trade.resample("ME").last()

    # Merge
    merged = (
        dxy
        .join(vix, how="inner")
        .join(ff, how="inner")
        .join(ecb, how="inner")
        .join(trade, how="inner")
    )

    # Feature Engineering
    merged["INT_DIFF"] = merged["FEDFUNDS"] - merged["ECB_RATE"]

    merged["DXY_return_next"] = (
        np.log(merged["DXY"].shift(-1)) - np.log(merged["DXY"])
    )

    merged["d_VIX"] = merged["VIX"].diff()
    merged["d_FEDFUNDS"] = merged["FEDFUNDS"].diff()
    merged["d_ECB_RATE"] = merged["ECB_RATE"].diff()
    merged["d_TRADE_BAL"] = merged["TRADE_BAL"].diff()
    merged["d_INT_DIFF"] = merged["INT_DIFF"].diff()

    merged = merged.dropna().reset_index()

    # Time features
    merged["YEAR"] = merged["DATE"].dt.year
    merged["MONTH"] = merged["DATE"].dt.month
    merged["QUARTER"] = merged["DATE"].dt.quarter

    merged = merged.sort_values("DATE").reset_index(drop=True)

    return merged
