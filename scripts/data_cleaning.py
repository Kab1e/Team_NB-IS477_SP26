import pandas as pd
import numpy as np

#Load raw data
def load_raw_data():

    def read_raw(name):
        path = f"data/raw/{name}.csv"
        df = pd.read_csv(path)

        df["DATE"] = pd.to_datetime(df["DATE"])
        df = df.sort_values("DATE")
        df = df.set_index("DATE")

        return df

    return (
        read_raw("DXY"),
        read_raw("VIX"),
        read_raw("FEDFUNDS"),
        read_raw("ECB_RATE"),
        read_raw("TRADE_BAL"),
        read_raw("USDJPY"),
        read_raw("AUDUSD")
    )


def clean_series(dxy, vix, ff, ecb, trade, jpy, aud):
    # Handle missing values within each dataset first
    dxy = dxy.dropna()
    vix = vix.dropna()
    ff = ff.dropna()
    ecb = ecb.dropna()
    trade = trade.dropna()
    jpy = jpy.dropna()
    aud = aud.dropna()


    # Monthly alignment AFTER cleaning
    dxy   = dxy.resample("ME").last()
    vix   = vix.resample("ME").mean()
    ff    = ff.resample("ME").last()
    ecb   = ecb.resample("ME").last()
    trade = trade.resample("ME").last()
    jpy = jpy.resample('ME').last()
    aud = aud.resample('ME').last()

    # AUD-JPY Exchange Rate (For the purpose of another risk sentiment indicator) 
    fx = jpy.join(aud, how='inner')
    fx['AUDJPY'] = fx['AUDUSD'] * fx['USDJPY']
    fx['AUDJPY_LOG'] = np.log(fx['AUDJPY'])
    audjpy = fx[["AUDJPY_LOG"]]

    return dxy, vix, ff, ecb, trade, audjpy

def load_data():

    dxy, vix, ff, ecb, trade, jpy, aud = load_raw_data()

    dxy, vix, ff, ecb, trade, audjpy = clean_series(dxy, vix, ff, ecb, trade, jpy, aud)

    merged = (
        dxy
        .join(vix, how="inner")
        .join(ff, how="inner")
        .join(ecb, how="inner")
        .join(trade, how="inner")
        .join(audjpy, how="inner")
    )

    # Feature Engineering
    merged["INT_DIFF"] = merged["FEDFUNDS"] - merged["ECB_RATE"]
    merged['DXY_next'] = merged['DXY'].shift(-1)
    merged["DXY_Diff"] = np.log(merged["DXY_next"] / merged["DXY"])
    merged["TRADE_DEFICIT"] = np.log(-merged["TRADE_BAL"])

    merged = merged.dropna().reset_index()

    merged["YEAR"] = merged["DATE"].dt.year
    merged["MONTH"] = merged["DATE"].dt.month
    merged["QUARTER"] = merged["DATE"].dt.quarter

    merged = merged.sort_values("DATE").reset_index(drop=True)

    merged = merged.drop(columns= ["FEDFUNDS", "TRADE_BAL"])

    return merged