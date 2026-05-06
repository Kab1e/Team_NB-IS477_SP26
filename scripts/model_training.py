def training():
    from data_cleaning import load_data
    from sklearn.model_selection import GridSearchCV, TimeSeriesSplit
    from sklearn.metrics import mean_squared_error, mean_absolute_error, r2_score
    import numpy as np
    from statsmodels.tsa.statespace.sarimax import SARIMAX
    import itertools
    from sklearn.pipeline import Pipeline
    from sklearn.preprocessing import StandardScaler
    from sklearn.linear_model import (
        LinearRegression,
        Ridge,
        Lasso,
        ElasticNet,
        BayesianRidge,
        HuberRegressor,
        SGDRegressor,
    )
    import pandas as pd
    from sklearn.svm import SVR
    import warnings
    warnings.filterwarnings("ignore")

    # Data Preparation
    df = load_data()

    X = df[['DXY', 'VIX', 'ECB_RATE', 'TRADE_DEFICIT', 'INT_DIFF', 'YEAR', 'MONTH', 'QUARTER', 'AUDJPY_LOG']]
    y = df['DXY_Diff']

    split = int(len(df) * 0.75)
    X_train, X_test = X.iloc[:split], X.iloc[split:]
    y_train, y_test = y.iloc[:split], y.iloc[split:]

    cv = TimeSeriesSplit(n_splits=5)

    # Model Training
    # HistGradientBoostingRegressor
    from sklearn.ensemble import HistGradientBoostingRegressor

    HistGB_param_grid = {
        "max_iter": [100, 500, 1000, 10_000, 100_000],
        "learning_rate": [0.00001, 0.0001, 0.001, 0.01, 0.1, 1],
        "max_depth": [1, 2, 3, 5, 7],
        "min_samples_leaf": [5, 10, 20, 30],
        "l2_regularization": [0.0, 0.1, 1.0, 3.0, 5.0],
        "max_leaf_nodes": [8, 15, 31]
    }

    HistGB = GridSearchCV(
        estimator=HistGradientBoostingRegressor(random_state=42, early_stopping=True, validation_fraction=0.15, n_iter_no_change=15),
        param_grid=HistGB_param_grid,
        scoring="neg_root_mean_squared_error",
        cv=cv,
        n_jobs=-1,
        verbose=1,
    )
    HistGB.fit(X_train, y_train)

    best_HistGB = HistGB.best_estimator_
    y_pred_histgb = best_HistGB.predict(X_test)

    print(f"Histogram Gradient Boosting Regressor")
    print(f"Best params: {HistGB.best_params_}")
    print(f"RMSE: {np.sqrt(mean_squared_error(y_test, y_pred_histgb)):.4f}")
    print(f"MAE:  {mean_absolute_error(y_test, y_pred_histgb):.4f}")
    print(f"R²:   {r2_score(y_test, y_pred_histgb):.4f}")



    # SARIMAX
    best_aic = np.inf
    best_order = None
    best_sarimax = None

    for p, d, q in itertools.product(range(4), range(2), range(4)):
        try:
            mod = SARIMAX(y_train.values, exog=X_train, order=(p, d, q),
                        enforce_stationarity=False, enforce_invertibility=False)
            res = mod.fit(disp=False, maxiter=200)
            if res.aic < best_aic:
                best_aic = res.aic
                best_order = (p, d, q)
                best_sarimax = res
        except Exception:
            continue

    y_pred_sarimax = best_sarimax.forecast(steps=len(y_test), exog=X_test)

    print("SARIMAX")
    print(f"Best order (p,d,q): {best_order}")
    print(f"AIC:  {best_aic:.2f}")
    print(f"RMSE: {np.sqrt(mean_squared_error(y_test, y_pred_sarimax)):.4f}")
    print(f"MAE:  {mean_absolute_error(y_test, y_pred_sarimax):.4f}")
    print(f"R²:   {r2_score(y_test, y_pred_sarimax):.4f}")



    # Linear Model
    scoring = {
        "rmse": "neg_root_mean_squared_error",
        "mae":  "neg_mean_absolute_error",
        "mape": "neg_mean_absolute_percentage_error",
        "r2":   "r2",
    }
    refit_metric = "rmse"

    models = {
        "LinearRegression": (
            Pipeline([("scaler", StandardScaler()), ("model", LinearRegression())]),
            {
                "model__fit_intercept": [True, False],
            },
        ),
        "Ridge": (
            Pipeline([("scaler", StandardScaler()), ("model", Ridge(random_state=42))]),
            {
                "model__alpha": [0.001, 0.01, 0.1, 1.0, 10.0, 100.0],
                "model__solver": ["auto", "svd", "cholesky", "lsqr", "saga"],
            },
        ),
        "Lasso": (
            Pipeline([("scaler", StandardScaler()), ("model", Lasso(random_state=42, max_iter=10000))]),
            {
                "model__alpha": [0.0001, 0.001, 0.01, 0.1, 1.0, 10.0],
                "model__selection": ["cyclic", "random"],
            },
        ),
        "ElasticNet": (
            Pipeline([("scaler", StandardScaler()), ("model", ElasticNet(random_state=42, max_iter=10000))]),
            {
                "model__alpha": [0.0001, 0.001, 0.01, 0.1, 1.0],
                "model__l1_ratio": [0.1, 0.3, 0.5, 0.7, 0.9],
            },
        ),
        "BayesianRidge": (
            Pipeline([("scaler", StandardScaler()), ("model", BayesianRidge())]),
            {
                "model__alpha_1": [1e-7, 1e-6, 1e-5],
                "model__alpha_2": [1e-7, 1e-6, 1e-5],
                "model__lambda_1": [1e-7, 1e-6, 1e-5],
                "model__lambda_2": [1e-7, 1e-6, 1e-5],
            },
        ),
        "HuberRegressor": (
            Pipeline([("scaler", StandardScaler()), ("model", HuberRegressor(max_iter=500))]),
            {
                "model__epsilon": [1.1, 1.35, 1.5, 2.0],
                "model__alpha": [1e-5, 1e-4, 1e-3, 1e-2],
            },
        ),
        "SGDRegressor": (
            Pipeline([("scaler", StandardScaler()), ("model", SGDRegressor(random_state=42, max_iter=5000))]),
            {
                "model__loss": ["squared_error", "huber", "epsilon_insensitive"],
                "model__penalty": ["l2", "l1", "elasticnet"],
                "model__alpha": [1e-5, 1e-4, 1e-3, 1e-2],
                "model__learning_rate": ["constant", "optimal", "invscaling", "adaptive"],
                "model__eta0": [0.001, 0.01, 0.1],
            },
        ),
    }

    results = []
    best_estimators = {}

    for name, (pipe, grid) in models.items():
        gs = GridSearchCV(
            estimator=pipe,
            param_grid=grid,
            scoring=scoring,
            refit=refit_metric,
            cv=cv,
            n_jobs=-1,
            verbose=1,
            return_train_score=True,
        )
        gs.fit(X_train, y_train)

        best_estimators[name] = gs.best_estimator_

        idx = gs.best_index_
        row = {"model": name, "best_params": gs.best_params_}
        for metric in scoring:
            mean = gs.cv_results_[f"mean_test_{metric}"][idx]
            std  = gs.cv_results_[f"std_test_{metric}"][idx]

            if metric != "r2":
                mean, std = -mean, std
            row[f"{metric}_mean"] = mean
            row[f"{metric}_std"]  = std
        results.append(row)

    results_df = pd.DataFrame(results).sort_values("rmse_mean")
    best_linear_name = results_df.iloc[0]["model"]
    best_linear_model = best_estimators[best_linear_name]

    y_pred_linear = best_linear_model.predict(X_test)

    print(f"Best Linear Model: {best_linear_name}")
    print(f"RMSE: {np.sqrt(mean_squared_error(y_test, y_pred_linear)):.4f}")
    print(f"MAE:  {mean_absolute_error(y_test, y_pred_linear):.4f}")
    print(f"R²:   {r2_score(y_test, y_pred_linear):.4f}")


    # SVR
    SVR_param_grid = {
        "kernel": ["rbf"],
        "C": [0.1, 1.0, 10.0, 100.0],
        "epsilon": [0.01, 0.05, 0.1, 0.2],
        "gamma": ["scale", "auto"],
    }

    best_svr = GridSearchCV(SVR(), SVR_param_grid, scoring="neg_root_mean_squared_error", cv=cv, n_jobs=-1)
    best_svr.fit(X_train, y_train)
    y_pred_svr = best_svr.predict(X_test)

    print("SVR (RBF)")
    print(f"Best params: {best_svr.best_params_}")
    print(f"RMSE: {np.sqrt(mean_squared_error(y_test, y_pred_svr)):.4f}")
    print(f"MAE:  {mean_absolute_error(y_test, y_pred_svr):.4f}")
    print(f"R²:   {r2_score(y_test, y_pred_svr):.4f}")


    import joblib
    joblib.dump(best_HistGB, "outputs/models/histgb.joblib")
    joblib.dump(best_sarimax, "outputs/models/sarimax.joblib")
    joblib.dump(best_linear_model, "outputs/models/linear_model.joblib")
    joblib.dump(best_svr, "outputs/models/svr.joblib")

    return best_HistGB, best_sarimax, best_linear_model, best_svr

def train_models(TRAIN_AGAIN = False):
    import joblib
    import os
    if TRAIN_AGAIN == False and all(
    os.path.exists(p) for p in [
        "outputs/models/histgb.joblib",
        "outputs/models/sarimax.joblib",
        "outputs/models/linear_model.joblib",
        "outputs/models/svr.joblib",
    ]
    ):
        best_HistGB = joblib.load("outputs/models/histgb.joblib")
        best_sarimax = joblib.load("outputs/models/sarimax.joblib")
        best_linear_model = joblib.load("outputs/models/linear_model.joblib")
        best_svr = joblib.load("outputs/models/svr.joblib")

    else:
        best_HistGB, best_sarimax, best_linear_model, best_svr = training()

    return best_HistGB, best_sarimax, best_linear_model, best_svr