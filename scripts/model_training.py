import numpy as np
import pandas as pd

from sklearn.model_selection import GridSearchCV, TimeSeriesSplit
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import StandardScaler
from sklearn.linear_model import (
    LinearRegression, Ridge, Lasso, ElasticNet,
    BayesianRidge, HuberRegressor, SGDRegressor
)
from sklearn.metrics import mean_squared_error, mean_absolute_error, r2_score

import torch
import torch.nn as nn
from torch.utils.data import DataLoader, TensorDataset

class LSTMModel(nn.Module):
    def __init__(self, input_size, hidden_size=64, num_layers=2):
        super().__init__()

        self.lstm = nn.LSTM(
            input_size=input_size,
            hidden_size=hidden_size,
            num_layers=num_layers,
            batch_first=True
        )

        self.fc = nn.Linear(hidden_size, 1)

    def forward(self, x):
        out, _ = self.lstm(x)
        out = out[:, -1, :]
        return self.fc(out)

def create_sequences(X, y, lookback=12):
    Xs, ys = [], []
    for i in range(lookback, len(X)):
        Xs.append(X[i-lookback:i])
        ys.append(y.iloc[i])
    return np.array(Xs), np.array(ys)

def train_lstm(X_train, y_train, X_test, y_test):

    device = torch.device("mps" if torch.backends.mps.is_available() else "cpu")

    X_train = torch.tensor(X_train, dtype=torch.float32)
    y_train = torch.tensor(y_train, dtype=torch.float32).view(-1, 1)

    X_test = torch.tensor(X_test, dtype=torch.float32)
    y_test = torch.tensor(y_test, dtype=torch.float32).view(-1, 1)

    train_loader = DataLoader(
        TensorDataset(X_train, y_train),
        batch_size=16,
        shuffle=False
    )

    model = LSTMModel(input_size=X_train.shape[2]).to(device)

    criterion = nn.MSELoss()
    optimizer = torch.optim.Adam(model.parameters(), lr=0.001)

    # -------------------
    # Training loop
    # -------------------
    for epoch in range(30):
        model.train()
        epoch_loss = 0

        for xb, yb in train_loader:
            xb, yb = xb.to(device), yb.to(device)

            preds = model(xb)
            loss = criterion(preds, yb)

            optimizer.zero_grad()
            loss.backward()
            optimizer.step()

            epoch_loss += loss.item()

        if epoch % 5 == 0:
            print(f"Epoch {epoch} | Loss: {epoch_loss:.6f}")

    # -------------------
    # Evaluation
    # -------------------
    model.eval()
    with torch.no_grad():
        preds = model(X_test.to(device)).cpu().numpy().flatten()

    return model, preds

def train_models(df):

    target = "DXY_return_next"

    X = df.drop(columns=[target, "DATE", "DXY"], errors="ignore")
    y = df[target]

    split_idx = int(len(df) * 0.75)

    X_train, X_test = X.iloc[:split_idx], X.iloc[split_idx:]
    y_train, y_test = y.iloc[:split_idx], y.iloc[split_idx:]

    cv = TimeSeriesSplit(n_splits=5)

    models = {
    "LinearRegression": (
        Pipeline([
            ("scaler", StandardScaler()),
            ("model", LinearRegression())
        ]),
        {}
    ),

    "Ridge": (
        Pipeline([
            ("scaler", StandardScaler()),
            ("model", Ridge())
        ]),
        {
            "model__alpha": [0.1, 1, 10]
        }
    ),

    "Lasso": (
        Pipeline([
            ("scaler", StandardScaler()),
            ("model", Lasso(max_iter=10000))
        ]),
        {
            "model__alpha": [0.001, 0.01]
        }
    ),

    "ElasticNet": (
        Pipeline([
            ("scaler", StandardScaler()),
            ("model", ElasticNet(max_iter=10000))
        ]),
        {
            "model__alpha": [0.001, 0.01, 0.1, 1.0],
            "model__l1_ratio": [0.1, 0.5, 0.9]
        }
    ),

    "BayesianRidge": (
        Pipeline([
            ("scaler", StandardScaler()),
            ("model", BayesianRidge())
        ]),
        {
            "model__alpha_1": [1e-6, 1e-5],
            "model__alpha_2": [1e-6, 1e-5],
            "model__lambda_1": [1e-6, 1e-5],
            "model__lambda_2": [1e-6, 1e-5]
        }
    ),


    "HuberRegressor": (
        Pipeline([
            ("scaler", StandardScaler()),
            ("model", HuberRegressor(max_iter=500))
        ]),
        {
            "model__epsilon": [1.1, 1.35, 1.5],
            "model__alpha": [1e-5, 1e-4, 1e-3]
        }
    ),

    "SGDRegressor": (
        Pipeline([
            ("scaler", StandardScaler()),
            ("model", SGDRegressor(max_iter=5000, random_state=42))
        ]),
        {
            "model__loss": ["squared_error", "huber"],
            "model__penalty": ["l2", "l1", "elasticnet"],
            "model__alpha": [1e-5, 1e-4, 1e-3],
            "model__learning_rate": ["constant", "optimal", "adaptive"]
        }
    ),
}
    results = []

    # -------------------
    # sklearn models 
    # -------------------
    for name, (pipe, grid) in models.items():

        gs = GridSearchCV(pipe, grid, cv=cv, scoring="neg_root_mean_squared_error")
        gs.fit(X_train, y_train)

        preds = gs.best_estimator_.predict(X_test)

        rmse = np.sqrt(mean_squared_error(y_test, preds))
        mae = mean_absolute_error(y_test, preds)
        r2 = r2_score(y_test, preds)

        results.append({"model": name, "rmse": rmse, "mae": mae, "r2": r2})

        pd.DataFrame({
            "actual": y_test.values,
            "predicted": preds
        }).to_csv(f"outputs/{name}_predictions.csv", index=False)

    # -------------------
    # Pytorch LSTM
    # -------------------
    scaler = StandardScaler()
    X_scaled = scaler.fit_transform(X)

    lookback = 12
    X_seq, y_seq = create_sequences(X_scaled, y, lookback)

    split_seq = int(len(X_seq) * 0.75)

    X_train_seq = X_seq[:split_seq]
    X_test_seq = X_seq[split_seq:]

    y_train_seq = y_seq[:split_seq]
    y_test_seq = y_seq[split_seq:]

    lstm_model, lstm_preds = train_lstm(
        X_train_seq, y_train_seq,
        X_test_seq, y_test_seq
    )

    rmse = np.sqrt(mean_squared_error(y_test_seq, lstm_preds))
    mae = mean_absolute_error(y_test_seq, lstm_preds)
    r2 = r2_score(y_test_seq, lstm_preds)

    results.append({"model": "LSTM", "rmse": rmse, "mae": mae, "r2": r2})

    pd.DataFrame({
        "actual": y_test_seq,
        "predicted": lstm_preds
    }).to_csv("outputs/LSTM_predictions.csv", index=False)

    results_df = pd.DataFrame(results).sort_values("rmse")
    results_df.to_csv("outputs/model_performance.csv", index=False)

    return results_df