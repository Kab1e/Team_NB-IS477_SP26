def load_data(api_key):
    import pandas as pd
    from fredapi import Fred

    fred = Fred(api_key)

    dxy_raw = fred.get_series('DTWEXBGS')
    vix_raw = fred.get_series('VIXCLS')

    ff_raw    = fred.get_series('FEDFUNDS')
    ecb_raw   = fred.get_series('ECBDFR')
    trade_raw = fred.get_series('BOPGSTB')

    def to_df(series, col_name):
        df = series.rename(col_name).to_frame()
        df.index.name = 'DATE'
        df.index = pd.to_datetime(df.index)
        return df

    dxy   = to_df(dxy_raw,   'DXY')
    vix   = to_df(vix_raw,   'VIX')
    ff    = to_df(ff_raw,    'FEDFUNDS')
    ecb   = to_df(ecb_raw,   'ECB_RATE')
    trade = to_df(trade_raw, 'TRADE_BAL')

    for df in [dxy, vix, ff, ecb, trade]:
        df.dropna(inplace=True)

    dxy_m = dxy.resample('ME').last()
    vix_m = vix.resample('ME').mean()

    ff_m    = ff.resample('ME').last()
    ecb_m   = ecb.resample('ME').last()
    trade_m = trade.resample('ME').last()

    merged = (dxy_m
        .join(vix_m,   how='inner')
        .join(ff_m,    how='inner')
        .join(ecb_m,   how='inner')
        .join(trade_m, how='inner')
    )

    merged['INT_DIFF'] = merged['FEDFUNDS'] - merged['ECB_RATE']
    merged['DXY_next'] = merged['DXY'].shift(-1)
    merged.dropna(inplace=True)
    merged.reset_index(inplace=True)
    merged['DATE'] = merged['DATE'].dt.strftime('%Y-%m-%d')
    merged["DATE"] = pd.to_datetime(merged["DATE"])
    merged["YEAR"] = merged["DATE"].dt.year
    merged["MONTH"] = merged["DATE"].dt.month
    merged["QUARTER"] = merged["DATE"].dt.quarter
    merged = merged.sort_values("DATE").reset_index(drop=True)

    return merged
