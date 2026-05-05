import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

st.title("💵 DXY Forecast Dashboard")

performance = pd.read_csv("outputs/model_performance.csv")
st.subheader("Model Performance")
st.dataframe(performance)

model_choice = st.selectbox("Select Model", performance["model"])

preds = pd.read_csv(f"outputs/{model_choice}_predictions.csv")

# Convert returns → DXY
last_price = 100  # base value for visualization
predicted_price = last_price * np.exp(np.cumsum(preds["predicted"]))

st.subheader("Forecast vs Actual")

fig, ax = plt.subplots()

ax.plot(predicted_price, label="Predicted DXY")
ax.plot(last_price * np.exp(np.cumsum(preds["actual"])), label="Actual DXY")

ax.legend()
st.pyplot(fig)

# Latest prediction
latest_return = preds["predicted"].iloc[-1]
latest_dxy = last_price * np.exp(latest_return)

st.subheader("Next Month Forecast")
st.write(f"Predicted DXY: {latest_dxy:.2f}")