# Forecasting the U.S. Dollar Index Using Macroeconomic Indicators


## Project Summary
Our aim in this project is to ***. Specifically, our research was focused on a single question: ***. 


---

## Contributors

Nihanth 


Bob


---

## Data Profile

### Nominal Broad U.S. Dollar Index

**Source:** Federal Reserve Bank of St. Louis (FRED) 

**Dataset Link:** https://fred.stlouisfed.org/series/DTWEXBGS

**Acquisition Method:**
Data is accessed via the FRED website or API in CSV/JSON format. For this project, the dataset is programmatically retrieved using Python (e.g., pandas_datareader or FRED API).

**Coverage:**

* **Time Range:** 2006–present 
* **Geography:** United States (trade-weighted index against major global currencies)

**Format:**

* **Structure:** Time series
* **Frequency:** Daily
* **File types:** CSV / JSON
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

**Dataset Link:** https://fred.stlouisfed.org/series/VIXCLS

**Acquisition Method:** 
Downloaded from FRED using API or direct CSV export.

**Coverage:**

* Time range: 1990–present
* Frequency: Daily
* Market: U.S. equity markets

**Format:**

* Structure: Time series
* File types: CSV / JSON
* Common attribute: Date/Time Period

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

**Dataset Links:**

https://fred.stlouisfed.org/series/FEDFUNDS

https://fred.stlouisfed.org/series/ECBDFR

**Acquisition Method:**
Both series are pulled separately via the FRED API and merged on the common date field to compute the spread. This merging process is further explained below. 

**Coverage:**

* **Time Range:**
  * FEDFUNDS: 1954–present (monthly)
  * ECBDFR: 1999–present (monthly)
* **Geography:** United States and Eurozone

**Format:**

* **Structure:** Time series (merged dataset)
* **Frequency:** Monthly (after alignment)
* **Common attribute:** Date/Time Period

Variables:

``DATE`` - Observation date

``FEDFUNDS`` - U.S. Federal Funds Rate (%)

``ECBDFR`` - ECB Deposit Facility Rate (%)

``INT_DIFF`` - Calculated variable (FEDFUNDS − ECBDFR which is in the integrated dataset)

**Description:**
This dataset(s) captures the interest rate differential between the U.S. and Eurozone, a key driver of exchange rate movements and capital flows.

**Ethical / Legal Considerations:**

* Public macroeconomic data; no restrictions
* No PII
* Requires citation of original central bank sources and FRED

### Trade Balance: Goods and Services (BOP Basis)

**Source:** U.S. Bureau of Economic Analysis via Federal Reserve Bank of St. Louis

**Dataset Link:** https://fred.stlouisfed.org/series/BOPGSTB

**Acquisition Method:**
Retrieved via FRED API or CSV download.

**Coverage:**

* **Time range:** 1960–present
* **Frequency:** Monthly
* **Geography:** United States

**Format:**

* **Structure:** Time series
* **File types:** CSV / JSON
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


---

## Data Cleaning
For this project, we required five seperate datasets for integration and analysis. As all of five datasets came from the same source (FRED API), not too much cleaning was required but the datasets had to be extensively standardized. 

---

## Data Integration

**Merge Statistics:**
* DXY: 5,305 observations
* VIX: 9,480 observations
* FEDFUNDS: 862 observations
* ECB_RATE: 9,987 observations
* TRADE_BAL: 411 observations

After resampling all datasets to a common monthly frequency and performing an inner join across all datasets, the final integrated dataset contained:

**Final merged dataset size:** 241 observations

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
