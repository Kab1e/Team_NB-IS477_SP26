## Overview
The overall goal of this project is to develop a multivariate predictive model that forecasts the strength of US Dollar Index (DXY) over a one-month horizon. The US Dollar Index measures the value of the US dollar relative to a basket of other major currencies worldwide. The movement of this index is heavily influenced by international market dynamics and market sentiment. Our approach is to create a model that uses macroeconomic and financial indicators that are known to influence exchange rates between currencies. Specifically, we will analyze the relationship between the DXY and three key predictors: the interest rate differential between the United States and the Eurozone, global market volatility measured by the VIX index, and the U.S. trade balance.

The project will involve collecting time-series data from public sources such as FRED, cleaning/integrating the datasets, and building predictive models using Python. Instead of focusing on one specific ML model, we will train and evaluate several machine learning models to determine which one provides the most accurate forecast for DXY. 

** **
## Team

Nihanth Beeram - 

Bob Zou - 

** **
## Research Question
To what extent can a multivariate predictive model accurately forecast the strength of the US Dollar Index (DXY) on a one-month time horizon, using *US-Eurozone interest rate differentials*, *global market volatility (VIX)*, and *the US trade balance*?"

** **
## Datasets
Nominal Broad U.S. Dollar Index: https://fred.stlouisfed.org/series/DTWEXBGS (Common Attribute: Date/Time Period)

CBOE Volatility Index (VIX): https://fred.stlouisfed.org/series/VIXCLS (Common Attribute: Date/Time Period)

US-Eurozone Interest Rate Differentials: https://fred.stlouisfed.org/series/FEDFUNDS & https://fred.stlouisfed.org/series/ECBDFR (Common Attribute: Date/Time Period)

Trade Balance: Goods and Services, Balance of Payments Basis (BOPGSTB): https://fred.stlouisfed.org/series/BOPGSTB (Common Attribute: Date/Time Period)

## Timeline 

**Project Planning** - By March 10th (Both)
  * _Define area of research and research question_
  * _Identify datasets that will help answer the question_
  * _Create project plan and timeline_

**Data Collection** - By March 13th (Both)
  * _Download datasets from the sources_
  * _Document metadata and sources_

**Data Cleaning and Integration** - By March 27th (Nihanth)
  * _Standardize time formats of datasets_
  * _Clean data and handle missing values in datasets_
  * _Merge datasets by date_

**Exploratory Data Analysis** - By March 31st (Bob)
  * _Visualize trends between factors_
  * _Identify and engineer features_ 
  * _Analyze correlations between factors_ 

**Interim Status Report** - March 31st

**Model Development and Evaluation** - By April 17th (Both)
  * _Preprocess data for machine learning_
  * _Test and experiment with various machine learning models_ 
  * _Evaluate model performance using metrics such as accuracy score_

**Results Interpretation and Final Report** - By May 1st (Both)
  * _Interpret model results and create visualizations_
  * _Prepare final project report and project documentation on GitHub_ 

**Final Project Submission** - May 3rd

** **
## Constraints

All four datasets are sourced from FRED. One key constraint is the differing frequencies and publication schedules of our datasets. The DXY and VIX are available at a daily frequency, while the trade balance (BOPGSTB) is reported monthly, and the ECB deposit facility rate changes only at policy meetings. This means our integrated dataset will need to be aligned to a common frequency, which reduces the number of observations available for model training and evaluation. Additionally, some series may have reporting lags — for example, trade balance figures are typically released with a delay of several weeks, which could affect the real-world applicability of a one-month-ahead forecast. Another constraint is that our model assumes the selected three predictors capture the primary drivers of DXY movement. In reality, exchange rates are influenced by many additional factors, such as geopolitical events, fiscal policy changes, and market speculation, that are difficult to quantify and are not included in our model. This limits the explanatory and predictive power we can reasonably expect.
Additionally, any unexpected circumstances, including war, may introduce significant uncertainty into DXY forecasting by causing a spike in VIX while not necessarily affecting the value of the US Dollar proportionally. Trade policy decisions, tariff announcements, and shifting geopolitical alliances can cause sudden and sharp movements in the dollar that are not captured by our selected macroeconomic indicators. For example, unexpected changes in US trade policy toward major partners like China or the EU could move the dollar in ways that the trade balance, VIX, and interest rate differential alone cannot explain. These black-swan-driven shocks are inherently difficult to quantify and model, which may limit our model's accuracy during periods of heightened policy uncertainty.

** **
## Gaps

We have not yet determined the exact date range for our analysis. This will depend on the overlapping availability of all four series, which we will assess during the data collection phase. We also need to decide on a specific method for computing the interest rate differential, which may evolve as we explore the data. We also need additional input on which machine learning models are most appropriate for time-series forecasting with a small number of features and limited observations. We plan to research this further and may consult with the instructor or TA for guidance on model selection and evaluation metrics suitable for our use case. We have not yet identified a reliable way to account for (geo-)political and policy uncertainty in our model. One possibility is incorporating a policy uncertainty index as an additional feature, but we need to evaluate whether this improves forecast performance without overfitting. This is an area we plan to explore further during the model development phase.
