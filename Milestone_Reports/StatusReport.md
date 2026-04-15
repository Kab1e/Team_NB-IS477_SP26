# Interim Status Report
We maintain our conviction in a multivariate framework for one-month DXY forecasting, anchored on US-Eurozone rate differentials, VIX, and the US trade balance. Since the project plan of March 10, the team has executed on the first three milestones: data collection, cleaning and integration, and exploratory analysis. Findings to date support the theoretical framework motivating our predictor selection, though one structural issue in the data has been identified and is discussed below. The team remains on track for the May 3 final submission.


## Table of Contents
[Milestones](#milestones)
- [Updated Timeline](#updated-timeline)
- [Data Collection and Acquisation](#data-collection-and-acquisation)
- [Data Cleaning and Integration](#data-cleaning-and-integration)
- [Exploratory Data Analysis](#exploratory-data-analysis)
- [Model Development and Evaluation](#model-development-and-evaluation )

[Problems & Future Steps](#problems-&-future-steps)
- [Noticable Error Found From Exploratory Analysis](#noticable-error-found-from-exploratory-analysis)
- [Looking Forward](#looking-forward)

[Data](#data)

[Contribution Summary](#contribution-summary)


# Milestones

## Updated Timeline 
**Data Collection and Acquisation** - Completed

**Data Cleaning and Integration** - Completed

**Exploratory Data Analysis** - Completed

**Model Development and Evaluation** - In Progress (Will Complete by **April 25th**)

**Results Interpretation and Final Report** - Not Yet Started (Will Complete by **May 1st**)

**Final Project Submission** - **May 3rd**



## Data Collection and Acquisation 

All five datasets were programatically acquired using the FRED (Federal Reserve Economic Data) API instead of manual CSV downloads. The API key is stored securely in an `.env` file which is excluded from the repository via `.gitignore`. The five series are Nominal Broad USD Index (DTWEXBGS), CBOE Volatility Index (VIXCLS), US Federal Funds Rate (FEDFUNDS), ECB Deposit Facility Rate (ECB), and US Trade Balance (BOPGSTB).


## Data Cleaning and Integration

The raw series data need to be cleaned before it could be used for modeling. Before cleaning, the five series were converted into individual dataframes with named columns. For missing values within each dataframe, FRED represents missing observations as `NaN`. All five dataframes were scanned and their missing values were dropped using `dropna()` before further processing. The data indexes were converted to `datatime` standardized to `YYYY-MM-DD` format. As mentioned in the project plan, we had to standardize the times format of the series as DXY and VIX are published as daily series while FEDFUNDS, ECB rate, and trade balance are published as monthly series. The daily series were resampled to monthly — DXY via `resample('ME').last()` and VIX via `resample('ME').mean()`. The monthly series were aligned to month-end format. The overall data cleaning process is shown in the [data_cleaning.ipynb](https://github.com/Kab1e/Team_NB-IS477_SP26/blob/main/data_cleaning.ipynb)


After cleaning the raw series data, the five dataframes were merged into a single unified monthly dataset. This was done by joining the five dataframes on the date index using `how='inner'`, which produced 241 monthly observations from 2006-01-31 to 2026-01-31. The start date is constrained by the DXY series (DTWEXBGS) which begins in January 2006. The integration process is shown in [data_cleaning.ipynb](https://github.com/Kab1e/Team_NB-IS477_SP26/blob/main/data_cleaning.ipynb) and the final cleaned dataset is [dxy_dataset.csv](https://github.com/Kab1e/Team_NB-IS477_SP26/blob/main/dxy_dataset.csv)


## Exploratory Data Analysis

From the data integration process, two additional columns were derived after merging the dataframes. The first column is `INT_DIFF` which is computed as `FEDFUNDS - ECB_RATE`, representing the US-Eurozone interest rate differential which is a key predictor of exchange rate movement. The second column is `DXY_next` which is computed as DXY.shift(-1), the one-month-ahead DXY value which serves as the prediction target for all models. 

EDA was conducted on the cleaned dataset and we primarily looked at the correlations between features within the cleaned dataset. This correlation heatmap is shown in [Exploratory_Analysis.ipynb](https://github.com/Kab1e/Team_NB-IS477_SP26/blob/main/Exploratory_Analysis.ipynb). 


## Model Development and Evaluation 

Seven linear models was trained and tuned via grid search with time-series cross-validation on 75% of the data, evaluated on a held-out test set covering the final 25% of the sample (approximately 60 observations). The best performing model was Lasso but a formal comparison against a trivial persistence baseline — simply using the current month's DXY as the prediction for next month — reveals that the tuned model achieves only a 1.5% improvement in RMSE. This problem is further explained in ***. From this initial model development, we decided to rebuild the features and add more complex models to GridSearchCV like LSTM. The initial model development is shown in [Exploratory_Analysis.ipynb](https://github.com/Kab1e/Team_NB-IS477_SP26/blob/main/Exploratory_Analysis.ipynb). 

** **

# Problems & Future Steps

## Noticable Error Found From Exploratory Analysis

While attempting to predict one-month-ahead values of the U.S. Dollar Index (DXY) using linear regression models with macroeconomic features (VIX, Fed Funds Rate, ECB Rate, Trade Balance, Interest Rate Differential) over the period January 2006 through January 2026. A suite of seven linear models was tuned via grid search with time-series cross-validation, and the best model was evaluated on a held-out test set covering the final 25% of the sample.

At first glance, the results appear excellent: predicted and actual DXY levels track each other almost perfectly on the test set, producing a visually compelling forecast. This apparent success is illusory. A formal comparison against a trivial persistence baseline — simply using the current month's DXY as the prediction for next month — reveals that the tuned model achieves only a 1.5% improvement in RMSE (1.8705 vs. 1.8987). This improvement is negligible and almost certainly within the noise of the split.

The underlying issue is a combination of target formulation and feature construction: the target variable DXY_next is highly autocorrelated with the feature DXY, and the best linear model has effectively learned the identity function DXY_next ≈ DXY, with macro features contributing only cosmetic adjustments. The visually impressive fit is, in substance, a persistence forecast.

The single most important diagnostic for any time-series forecasting model is comparison against a naive persistence baseline: the prediction that next period's value equals this period's value. For a highly autocorrelated series like a currency index, this baseline is notoriously hard to beat and is the standard benchmark in the forecasting literature. From our model, we see a 1.5% improvement in RMSE; however, is not meaningful. Small perturbations to the train/test split, the CV fold structure, or the random seed could easily flip this number negative. There is no evidence that the macro features provide predictive value beyond what is already contained in the current DXY level. Since DXY is a slow varying series, whose month-to-month changes are typically on the order of 1–2%, against a base value near 100. Therefore, from the heatmap, the correlation between DXY and DXY_next is approximately 0.99. When DXY is included as a feature and DXY_next is used as the target, a linear model will — correctly, from an optimization standpoint — place nearly all of its weight on DXY with a coefficient close to 1.0. The resulting prediction is indistinguishable from the input, which is indistinguishable from the target, which produces a near-perfect overlay plot.

The visual impression of accuracy is therefore a direct artifact of plotting a nearly-identity mapping against its own input, shifted by one period. It is not evidence that the model has learned anything about the economic drivers of the dollar. 


## Looking Forward

Data:
> Reformulate the target
>> Replace DXY_next with the next-period log return: `np.log(DXY).diff().shift(-1)`. Returns are near-stationary and not dominated by their own lag, so any predictive signal you find will be real rather than an artifact of autocorrelation.

> Feature Rebuild
>> Drop DXY from the feature set entirely. Replace macro features with their first differences: change in VIX, change in Fed Funds, change in ECB rate, change in interest rate differential, change in trade balance. Keep VIX level as well since it is roughly stationary on its own. Add two or three lags of DXY returns as autoregressive features.

> Re-Examine Models
>> Rerun GridSearchCV on the new formulation. In the meantime, add in more complex model features like LSTM.

Final Deliverable:
We are planning to deliver a `Streamlit` web app as our final artifact, which will allow users to interact with the trained model, visualize DXY forecasts against historical data, and compare the performance of the different machine learning models we evaluate. Detailed features and layout will be finalized soon.

** **

# Data

Our data are primarily from Federal Reserve St. Louis, accessed via FRED API. The dataset consists of 241 monthly observations from January 2006 to January 2026. 

** **

# Contribution Summary

__Nihanth__ - For this current milestone, I did the data cleaning and integration parts of the project. I collected the raw series data from the FRED API and converted the raw series into dataframes. After this, I cleaned the dataframes and removed the missing values from it. After cleaning the dataframes, I combined the five dataframes into a single unified monthly dataset by resampling the daily series to monthly and adjusting the monthly series. I worked on [data_cleaning.ipynb](https://github.com/Kab1e/Team_NB-IS477_SP26/blob/main/data_cleaning.ipynb) and [dxy_dataset.csv](https://github.com/Kab1e/Team_NB-IS477_SP26/blob/main/dxy_dataset.csv)

__Bob__ — As of April 14 (the day before Tax Day), I have completed the exploratory analysis for this project, including the major issue identified above [briefly name it]. After Nihanth finished cleaning and integrating the four FRED time series (DXY, VIX, US-Eurozone interest rate differential, and US trade balance) into a unified dataset, I took the merged data and conducted a thorough exploratory analysis to understand its underlying structure and relationships before model development.Beyond the EDA, I also reformatted and restructured several of our project deliverables to streamline them for downstream use in the final product. This included setting up [requirements.txt](https://github.com/Kab1e/Team_NB-IS477_SP26/blob/main/requirements.txt), [.gitignore](https://github.com/Kab1e/Team_NB-IS477_SP26/blob/main/.gitignore), and [utils.py](https://github.com/Kab1e/Team_NB-IS477_SP26/blob/main/utils.py) (codes are primarily from Nihanth's [data_cleaning.ipynb](https://github.com/Kab1e/Team_NB-IS477_SP26/blob/main/data_cleaning.ipynb)). 
