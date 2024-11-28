# actfts: Tools for Analysis of Time Series

The actfts package offers a flexible approach to time series analysis by focusing on Autocorrelation (ACF), Partial Autocorrelation (PACF), and stationarity tests, generating interactive plots for dynamic data visualization. It processes input data by validating and transforming it according to specified differences. It calculates ACF and PACF up to several lags and performs Box-Pierce, Ljung-Box, ADF, KPSS, and PP tests. The function organizes results into tables, with options to save them as TIFF files or Excel spreadsheets, and interactive mode provides on-screen visualization of the ACF-PACF and stationarity test outcomes.

[<img src="https://i.ibb.co/NxmBNBf/Logo-R-ACTFTS.png" width="100">](https://github.com/SergioFinances/actfts.git)

You can view all the package information at the following link
[actfts Web Page](https://github.com/SergioFinances/actfts.git)

## Example

This is a basic example which shows you how to use actfts packcage:

```bash
pip install actfts=0.1.0

import pandas as pd
from actfts.actfts_fun import acfinter

datag = DPIEEUU_dataset()
data = datag['DPIEEUU']
result = acfinter(data, lag = 15)
```
<img src="https://i.imgur.com/M4OHSh9.png" alt="Example Image" style="width: 1000px; height: 360px;">

## References

* U.S. Bureau of Economic Analysis, Gross Domestic Product (GDP), retrieved from FRED, Federal Reserve Bank of St. Louis; https://fred.stlouisfed.org/series/GDP.
* U.S. Bureau of Economic Analysis, Personal Consumption Expenditures (PCEC), retrieved from FRED, Federal Reserve Bank of St. Louis; https://fred.stlouisfed.org/series/PCEC
* U.S. Bureau of Economic Analysis, Disposable Personal Income (DPI), retrieved from FRED, Federal Reserve Bank of St. Louis;https://fred.stlouisfed.org/series/DPI
