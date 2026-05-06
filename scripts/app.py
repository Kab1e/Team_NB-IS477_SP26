import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

st.set_page_config(page_title="DXY Forecast Dashboard", layout="wide")
st.title("💵 DXY Forecast Dashboard")

# Load model performance
performance = pd.read_csv("outputs/model_performance.csv")

st.subheader("Model Performance")
st.dataframe(performance.style.format({"rmse": "{:.4f}", "mae": "{:.4f}", "r2": "{:.4f}"}), use_container_width=True)

# Model selector
model_choice = st.selectbox("Select Model", performance["model"])

# Load predictions (already in DXY levels)
preds = pd.read_csv(f"outputs/{model_choice}_predictions.csv")
preds["date"] = pd.to_datetime(preds["date"])

# Forecast vs Actual plot
st.subheader("Forecast vs Actual")

fig, ax = plt.subplots(figsize=(10, 5))
ax.plot(preds["date"], preds["actual"].shift(1), label="Actual DXY", color="#1f77b4")
ax.plot(preds["date"], preds["predicted"], label="Predicted DXY", color="#ff7f0e", linestyle="--")
ax.set_xlabel("Date")
ax.set_ylabel("DXY Index")
ax.legend()
ax.grid(True, alpha=0.3)
plt.tight_layout()
st.pyplot(fig)

# Residuals plot
st.subheader("Prediction Residuals")

residuals = preds["actual"] - preds["predicted"]

fig2, ax2 = plt.subplots(figsize=(10, 4))
ax2.bar(preds["date"], residuals, color=np.where(residuals >= 0, "#2ca02c", "#d62728"), width=20)
ax2.axhline(y=0, color="gray", linestyle="-", linewidth=0.5)
ax2.set_xlabel("Date")
ax2.set_ylabel("Residual (Actual - Predicted)")
ax2.grid(True, alpha=0.3)
plt.tight_layout()
st.pyplot(fig2)


# Latest prediction
# st.subheader("Latest Prediction")
# latest = preds.iloc[-1]
# col1, col2, col3 = st.columns(3)
# col1.metric("Date", latest["date"].strftime("%Y-%m-%d"))
# col2.metric("Actual DXY", f"{latest['actual']:.2f}")
# col3.metric("Predicted DXY", f"{latest['predicted']:.2f}", delta=f"{latest['predicted'] - latest['actual']:.2f}")