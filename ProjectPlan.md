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

**Model Development and Evaluation** - By April 10th (Both)
  * _Preprocess data for machine learning_
  * _Test and experiment with various machine learning models_ 
  * _Evaluate model performance using metrics such as accuracy score_

**Results Interpretation and Final Report** - By April 10th (Both)
  * _Interpret model results and create visualizations_
  * _Prepare final project report and project documentation on GitHub_ 

**Final Project Submission** - May 3rd

** **
## Constraints

** **
## Gaps
