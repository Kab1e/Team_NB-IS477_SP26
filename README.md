# Forecasting the U.S. Dollar Index Using Macroeconomic Indicators


## Project Summary
Our aim in this project is to ***. Specifically, our research was focused on a single question: ***. 


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

___

## Challenges


---

## Reproducing the Dashboard


---

## Licensing
