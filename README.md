# Forecasting the U.S. Dollar Index Using Macroeconomic Indicators


## Project Summary
Our aim in this project is to develop a multivariate predictive model that forecasts the strength of US Dollar Index (DXY) over a one-month horizon using historical macroeconomic data from 2006 to present day. Specifically, our research was focused on a single question: To what extent can a multivariate predictive model accurately forecast the strength of the US Dollar Index (DXY) on a one-month time horizon, using *US-Eurozone interest rate differentials, global market volatility (VIX), and the US trade balance*?. 

The movement of US Dollar Index is heavily influenced by international market dynamics and other macroeconomic indictors. We wanted to better understand what factors actually play a role in determining the strength of the US Dollar worldwide. The factors the we choose to explore were the the interest rate differentials between the United States and the Eurozone, global market volatility measured by the VIX index, the U.S. trade balance (or trade deficit), and AUD-JPY exchange rates. For the modeling portion, we decided to test various machine learning models like Lasso regression or SGDRegressor. The performance of each model was futher visualized through a Streamlit dashboard that visualized the performance of each model and showed each model's prediction of the next month DXY value.

For our file structure, all datasets have a raw CSV file and SHA hash, which located within their respective folders in the ``data/`` directory. The integrated dataset has a cleaned CSV file and a JSON file documenting the overall cleaning history. This data is also located directly in ``data/``. Scripts for data acquisation, hash generation, quality analysis, data cleaning, integration, and analysis (streamlit dashboard) are in ``scripts/``. A ``outputs/`` folder contains the models, and ``requirements.txt`` records all software dependencies.

To summarize our findings, ***

---

## Contributors

### Nihanth:
- [x] Ethical data handling (Module 2)
- [x] Storage and organization (Modules 4/5)
- [x] Data quality (Module 9)
- [x] Data integration (Modules 7/8)
- [x] Workflow automation and provenance (Modules 11/12)

### Bob:
- [x] Data lifecycle (Module 1)
- [x] Data collection and acquisition (Module 3)
- [x] Data cleaning (Module 10)
- [x] Reproducibility and transparency (Module 13)
- [x] Metadata and data documentation (Module 15)


---

## Data Profile

### Nominal Broad U.S. Dollar Index

**Source:** Federal Reserve Bank of St. Louis (FRED) 

**Dataset Location:** ``data/raw/DXY.csv``

**Acquisition Method:**
The data is accessed via the FRED website or API in CSV/JSON format. For this project, the dataset was programmatically retrieved using Python (FRED API) and converted into a CSV file.

**Coverage:**

* **Time Range:** 2006–present 
* **Geography:** United States (trade-weighted index against major global currencies)

**Format:**

* **Structure:** Time series
* **Frequency:** Daily
* **File types:** JSON via API (pandas series) -> converted to CSV
* **Common attribute:** Date/Time Period

**Variables:**

``DATE`` - Observation Date

``DTWEXBGS`` - Nominal Broad U.S. Dollar Index (index level, base year varies)

**Description:**
This dataset measures the value of the U.S. dollar relative to a basket of foreign currencies, weighted by trade volumes. It is a key indicator of dollar strength in global markets.

**Ethical / Legal Considerations:**

* Publicly available government data; no usage restrictions
* No personally identifiable information (PII)
* Must cite FRED as the data source

### CBOE Volatility Index (VIX)

**Source:** Chicago Board Options Exchange via Federal Reserve Bank of St. Louis

**Dataset Loxation:** ``data/raw/VIX.csv``

**Acquisition Method:** 
The data was programmatically retrieved from FRED API and converted into a CSV file.

**Coverage:**

* **Time range:** 1990–present (filtered to 2006 to present)
* **Frequency:** Daily
* **Market:** U.S. equity markets

**Format:**

* **Structure:** Time series
* **File types:** JSON via API (pandas series) -> converted to CSV
* **Common attribute:** Date/Time Period

**Variables:**

``DATE`` - Observation date

``VIXCLS`` -  Closing value of the VIX index

**Description:**
The VIX measures expected market volatility over the next 30 days based on S&P 500 options. Often referred to as the “fear index,” it captures investor sentiment and uncertainty.

**Ethical / Legal Considerations:**

* Public financial data; free for academic use
* No PII or sensitive data
* Proper attribution to CBOE and FRED required

### U.S.–Eurozone Interest Rate Differentials

**Sources:**

Federal Reserve (Federal Funds Rate)
& European Central Bank (Deposit Facility Rate)
Distributed via Federal Reserve Bank of St. Louis

**Dataset Location:**

``data/raw/FEDFUNDS.csv``

``data/raw/ECB_RATE.csv``

**Acquisition Method:**
Both series are pulled separately via the FRED API and converted into a CSV file.. 

**Coverage:**

* **Time Range:**
  * FEDFUNDS: 1954–present (monthly - filtered to 2006 to present)
  * ECBDFR: 1999–present (monthly - filtered to 2006 to present)
* **Geography:** United States (FEDFUNDS) and Eurozone (ECBDFR)

**Format:**

* **Structure:** Time series (merged dataset)
* **Frequency:** Monthly (after alignment)
* **File types:** JSON via API (pandas series) -> converted to CSV
* **Common attribute:** Date/Time Period

**Variables:**

``DATE`` - Observation date

``FEDFUNDS`` - U.S. Federal Funds Rate (%)

``ECBDFR`` - ECB Deposit Facility Rate (%)

**Description:**
These datasets shows the interest rates for banks in the U.S. and Eurozone respectively. The merged dataset will have a variable called ``INT_DIFF`` which will capture the interest rate differentials between US and Eurozone for each corresponding time period which is a key driver of exchange rate movements and capital flows. 

**Ethical / Legal Considerations:**

* Public macroeconomic data; no restrictions
* No PII
* Requires citation of original central bank sources and FRED

### Trade Balance: Goods and Services (BOP Basis)

**Source:** U.S. Bureau of Economic Analysis via Federal Reserve Bank of St. Louis

**Dataset Location:** ``data/raw/TRADE_BAL.csv``

**Acquisition Method:**
The data was programmatically retrieved from FRED API and converted into a CSV file.

**Coverage:**

* **Time range:** 1960–present (filtered to 2006 to present)
* **Frequency:** Monthly
* **Geography:** United States

**Format:**

* **Structure:** Time series
* **File types:** JSON via API (pandas series) -> converted to CSV
* **Common attribute:** Date/Time Period

**Variables:**

``DATE`` - Observation date

``BOPGSTB`` - Trade balance (billions of USD, seasonally adjusted)

**Description:**
This dataset represents the difference between U.S. exports and imports of goods and services. A negative value indicates a trade deficit, while a positive value indicates a surplus.

**Ethical / Legal Considerations:**

* Public government dataset
* No sensitive or personal data
* Attribution to BEA and FRED required

### USD/JPY Exchange Rate

**Source:** Board of Governors of the Federal Reserve System via Federal Reserve Bank of St. Louis

**Dataset Location:** data/raw/USDJPY.csv

**Acquisition Method:**
The data was programmatically retrieved from FRED API and converted into a CSV file.

**Coverage:**

* **Time Range**: 1971–present
* **Frequency**: Daily
* **Geography**: United States / Japan

**Format:**

* **Structure**: Time series
* **File types**: CSV / JSON
* **Common attribute**: Date/Time Period

**Variables:**
``DATE`` - Observation date
``DEXJPUS`` - Japanese Yen per 1 U.S. Dollar (noon buying rate)

**Description:**
This dataset represents the daily exchange rate between the U.S. dollar and the Japanese yen. The yen is widely regarded as a "safe haven" currency — during periods of market stress, investors tend to unwind carry trades and move capital into yen-denominated assets, causing the yen to appreciate. This series is used in conjunction with the AUD/USD rate to construct the AUD/JPY cross rate, a composite risk sentiment indicator.
Ethical / Legal Considerations:

* Public government dataset
* No sensitive or personal data
* Requires citation of original central bank sources and FRED

### AUD/USD Exchange Rate

**Source:** Board of Governors of the Federal Reserve System via Federal Reserve Bank of St. Louis

**Dataset Location:** ``data/raw/AUDUSD.csv``

**Acquisition Method:**
The data was programmatically retrieved from FRED API and converted into a CSV file.

**Coverage:**

* **Time Range:** 1971–present
* **Frequency:** Daily
* **Geography:** United States / Australia

**Format:**

* **Structure:** Time series
* **File types:** CSV / JSON
* **Common attribute:** Date/Time Period

**Variables:**

``DATE`` - Observation date

``DEXUSAL`` - U.S. Dollars per 1 Australian Dollar (noon buying rate)

**Description:**
This dataset represents the daily exchange rate between the Australian dollar and the U.S. dollar. The Australian dollar is a commodity-linked, high-yield "risk-on" currency — it tends to appreciate during periods of global economic optimism and sell off sharply during risk-off episodes. Combined with the USD/JPY rate, the derived AUD/JPY cross rate (computed as AUDUSD × USDJPY) serves as a pure risk sentiment proxy in our feature set, capturing risk-on versus risk-off capital flows that VIX alone may not fully reflect.

**Ethical / Legal Considerations:**

* Publicly available government data; no usage restrictions
* No personally identifiable information (PII)
* Must cite the Federal Reserve Board and FRED as the data source

___

## Data Quality Assessment
Data quality is central to this project because we had to compare and integrate five datasets for different purposes and in different geographical locations. The assessment is based on summary statistics generated by ``scripts/quality_report.py``.

**Completeness and Missingness**

***

**Accuracy**

***

**Consistency**

***

**Issues Identified and Fixes**

***

---

## Data Cleaning
All five datasets were programatically acquired using the FRED (Federal Reserve Economic Data) API and converted into CSV files through the ``scripts/acquire_data.py``. The datasets can also be acquired through the FRED website as well through manual CSV download. The API key is stored securely in an ``.env`` file which is excluded from the repository via ``.gitignore``.

As all of five datasets came from the same source (FRED API), not too much cleaning was required but the datasets had to be extensively standardized. For missing values, FRED represents them as ``NaN``. All five dataframes were scanned and their missing values were dropped using dropna() before further processing. For data standardization, we had to standardize the times format of all series as DXY and VIX are published as daily series while FEDFUNDS, ECB rate, and trade balance are published as monthly series. To standardize the daily series, they were resampled to monthly — DXY via resample('ME').last() and VIX via resample('ME').mean(). 

In addition to the five core macroeconomic series, we had in status report, two foreign exchange rates (USD/JPY and AUD/USD) were acquired from FRED and cleaned using the same procedure. Both series are published daily, so they were resampled to monthly frequency via resample('ME').last() to align with the other datasets. After resampling, the two series were joined on their date index, and the AUD/JPY cross rate was derived by multiplying AUD/USD by USD/JPY. The resulting cross rate was then log-transformed to produce the AUDJPY_LOG feature, which serves as a risk sentiment indicator in the model — AUD/JPY captures the spread between a "risk-on" currency (AUD) and a "safe haven" currency (JPY), providing a complementary measure of market risk appetite alongside VIX. The raw USD/JPY and AUD/USD columns were dropped after the cross rate was computed, as only the composite indicator was needed for modeling.

After cleaning and integrating the datasets into a singular dataset (further explained below), we added four new columns to the merged dataset. The first column ``INT_DIFF``, which is computed as ``FEDFUNDS - ECB_RATE``, represents the interest rate differentials between US and Eurozone. The second column is ``DXY_next`` which is computed as DXY.shift(-1), the one-month-ahead DXY value which serves as the prediction target for all models. The third column ``DXY_Diff``, which computes log return of ``DXY`` and ``DXY_next``, represents the percentage change in log terms between ``DXY`` and ``DXY_next``. The fourth column ``TRADE_DEFICIT``, which converts the ``TRADE_BAL`` to a log-scaled measure, represents the trade deficit. After deriving these columns, ``FEDFUNDS`` and ``TRADE_BAL`` columns were dropped as we only needed the ``INT_DIFF`` and ``TRADE_DEFICIT`` for analysis and these variables didn't contribute to model development. 

---

## Data Integration

**Merge Statistics:**
* DXY: 5,305 observations
* VIX: 9,480 observations
* FEDFUNDS: 862 observations
* ECB_RATE: 9,987 observations
* TRADE_BAL: 411 observations

After resampling all datasets to a common monthly frequency and performing an inner join across all datasets, the final integrated dataset contained:

**Final merged dataset size:** 241 observations ranging from 2006-01-31 to 2026-02-28 (monthly frequency) 

**Overall merge rate:** 58.64%

**Assessment:** Although the merge rate of 58.64% represents a reduction in sample size, it shouldn't be treated as data loss in a traditional sense but as a necessary trade-off. 

___

## Findings and Future Work

The first and most important finding was methodological. Our initial model formulation, which predicted the next-month DXY level using current DXY as a feature, appeared to perform well visually but was illusory. The correlation between DXY and DXY_next was approximately 0.99, and the best linear model achieved only a 1.5% RMSE improvement over a naive persistence baseline (predicting that next month's DXY equals this month's). The model had effectively learned the identity function. This finding aligns with the Meese-Rogoff puzzle (1983), which established that exchange rate models consistently fail to outperform a random walk in out-of-sample forecasting — a result that has held for over four decades in the academic literature.

After identifying this issue, we reformulated the problem. We replaced the target with the log return of DXY, and rebuilt features as first differences of macroeconomic variables to capture changes rather than levels. This reformulation eliminated the autocorrelation artifact and produced meaningful out-of-sample results.
Across the model families we tested — linear models (Ridge, Lasso, ElasticNet, BayesianRidge, HuberRegressor, SGDRegressor), histogram-based gradient boosting, support vector regression, and SARIMAX — we found that the macro features explain a modest but real share of next-month DXY return variance. An R-squared of approximately 0.05–0.08 on monthly FX returns is consistent with what the academic literature considers a meaningful result in this domain. OLS regression identified VIX and the interest rate differential as the two statistically significant predictors, while temporal features (year, month) and the trade deficit were not significant and were dropped via backward elimination.

We ultimately decided against using LSTM (Long Short-Term Memory) networks for this project because our dataset contains only 241 monthly observations. LSTMs are deep learning models that require substantially more training data to learn meaningful temporal patterns without overfitting. With 241 rows, an LSTM would almost certainly memorize the training set rather than generalize, and there would not be enough data to construct a proper train/validation/test split that leaves sufficient samples in each partition. 

For future work, several directions could improve the model. First, adding lagged returns of DXY as autoregressive features would let models capture momentum and mean-reversion dynamics directly. Second, the AUD/JPY cross rate was included as a risk sentiment proxy but its contribution relative to VIX should be evaluated more carefully, given that JPY constitutes 13.6% of the DXY basket and introduces partial endogeneity. Third, expanding the feature set to include commodity prices (oil, gold), yield curve slope, or positioning data (CFTC Commitments of Traders) could provide additional predictive signal. 
___

## Challenges

The most significant challenge was the target formulation problem described above and in our status report. The near-perfect visual fit of our initial models was misleading. Specifically, comparison against the naive persistence baseline, we identified that the model was not learning anything beyond the identity mapping. This experience reinforced that visual inspection of predictions is insufficient without a formal baseline comparison, particularly for highly autocorrelated time series.

A second challenge was the small sample size. With only 241 monthly observations spanning 2006 to 2026, we had limited data for training complex models. This constrained our hyperparameter search spaces and ruled out data-hungry approaches like LSTMs or deep neural networks. We addressed this by favoring models with strong regularization (high min_samples_leaf, shallow tree depth for HistGradientBoosting, L2 penalties for linear models) and using TimeSeriesSplit cross-validation to respect the temporal ordering of observations.

---

## Reproducing the Dashboard
This section will go over how exactly someone can reproduce our streamlit dashboard from setting up the environment to verifying the outputs

### Step 1: Clone the Repository
>
> ```bash
> git clone https://github.com/[anonymized]/Team_NB-IS477_SP26.git
> cd Team_NB-IS477_SP26
> ```

### Step 2: Set Up the Python Environment
>
**Using pip**
> ```bash
> python -m venv venv
> source venv/bin/activate
> pip install -r requirements.txt
> ```
>
**Using conda**
> ```bash
> conda create -n is477-project python=3.12.2
> conda activate is477-project
> pip install -r requirements.txt
> ```

### Step 3: Set Up Environment Variables
To acquire the data, an `.env` file with your own API key from Fred is needed. You can get your own free API key from [FRED]( https://fred.stlouisfed.org) by creating an account for free. After getting an API key, create an .env file in the root directory of the project. It should look like:

> `'FRED_API_KEY' = "YOUR_API_KEY"`

### Step 4: Run the Project and Verify the Outputs
To run the pipeline, you should put this into the terminal: `python scripts/run_all.py`. After running the pipeline, confirm that the following files exist: 

---

## Workflow


---

## Licensing
