## Update on Tasks

# Noticable Error Found From Exploratory Analysis

While attempting to predict one-month-ahead values of the U.S. Dollar Index (DXY) using linear regression models with macroeconomic features (VIX, Fed Funds Rate, ECB Rate, Trade Balance, Interest Rate Differential) over the period January 2006 through January 2026. A suite of seven linear models was tuned via grid search with time-series cross-validation, and the best model was evaluated on a held-out test set covering the final 25% of the sample.

At first glance, the results appear excellent: predicted and actual DXY levels track each other almost perfectly on the test set, producing a visually compelling forecast. This apparent success is illusory. A formal comparison against a trivial persistence baseline — simply using the current month's DXY as the prediction for next month — reveals that the tuned model achieves only a 1.5% improvement in RMSE (1.8705 vs. 1.8987). This improvement is negligible and almost certainly within the noise of the split.

The underlying issue is a combination of target formulation and feature construction: the target variable DXY_next is highly autocorrelated with the feature DXY, and the best linear model has effectively learned the identity function DXY_next ≈ DXY, with macro features contributing only cosmetic adjustments. The visually impressive fit is, in substance, a persistence forecast.

The single most important diagnostic for any time-series forecasting model is comparison against a naive persistence baseline: the prediction that next period's value equals this period's value. For a highly autocorrelated series like a currency index, this baseline is notoriously hard to beat and is the standard benchmark in the forecasting literature. From our model, we see a 1.5% improvement in RMSE; however, is not meaningful. Small perturbations to the train/test split, the CV fold structure, or the random seed could easily flip this number negative. There is no evidence that the macro features provide predictive value beyond what is already contained in the current DXY level. Since DXY is a slow varying series, whose month-to-month changes are typically on the order of 1–2%, against a base value near 100. Therefore, from the heatmap, the correlation between DXY and DXY_next is approximately 0.99. When DXY is included as a feature and DXY_next is used as the target, a linear model will — correctly, from an optimization standpoint — place nearly all of its weight on DXY with a coefficient close to 1.0. The resulting prediction is indistinguishable from the input, which is indistinguishable from the target, which produces a near-perfect overlay plot.

The visual impression of accuracy is therefore a direct artifact of plotting a nearly-identity mapping against its own input, shifted by one period. It is not evidence that the model has learned anything about the economic drivers of the dollar. 

** **

# Looking Forward

> Reformulate the target
>> Replace DXY_next with the next-period log return: `np.log(DXY).diff().shift(-1)`. Returns are near-stationary and not dominated by their own lag, so any predictive signal you find will be real rather than an artifact of autocorrelation.

> Feature Rebuild
>> Drop DXY from the feature set entirely. Replace macro features with their first differences: change in VIX, change in Fed Funds, change in ECB rate, change in interest rate differential, change in trade balance. Keep VIX level as well since it is roughly stationary on its own. Add two or three lags of DXY returns as autoregressive features.

> Re-Examine Models
>> Rerun GridSearchCV on the new formulation. In the meantime, add in more complex model features like LSTM.

## Data

Our data are primarily from Federal Reserve St. Louis, accessed via FRED API. The dataset consists of 241 monthly observations from January 2006 to January 2026. 

