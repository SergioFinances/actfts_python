# Get Started

## Demo Data

This package includes a three-time series that automatically updates from the FRED (s.f) database of the United States. These datasets allow you to practice using the package’s functions. Below is a brief description of each:

**Gross Domestic Product**, This measure quantifies the total monetary value of all goods and services produced within a country over a specific period, typically a quarter or a year. It provides a comprehensive overview of a nation’s economic activity, reflecting its size and economic health. Economists often use GDP to compare economic performance across countries or regions and assess the impact of economic policies.

Below is a practical code example to retrieve GDP data.

```bash
GDP_data = DPIEEUU_dataset()
print(GDP_data.head())
```

**Personal Consumption Expenditures** This represents the total value of goods and services consumed by households and nonprofit institutions serving households within an economy. As a critical component of GDP, PCE reveals consumer behavior and spending patterns. It covers expenditures on durable goods, non durable goods, and services, providing insights into consumer confidence and living standards.

Below is a handy code that allows you to retrieve PCE data

```bash
PCEC_data = PCECEEUU_dataset()
print(PCEC_data.head())
```

**Disposable Personal Income** refers to the amount of money households have available for spending and saving after deducting taxes and other mandatory charges. It is an indicator of consumer purchasing power and financial health. DPI significantly impacts consumer spending and saving behaviors, affecting overall economic growth. Analysts frequently study DPI to identify trends in personal savings rates and consumption patterns.

Below is a practical code snippet for obtaining DPI data.

```bash
DPI_data = DPIEEUU_dataset()
print(DPI_data.head())
```

## Previews Concepts:

Before beginning with the examples, define the concepts that the `acfinter()` is the function used to calculate essentials.

### ACF (Autocorrelation Function)

ACF measures the correlation between a time series and its lags at different intervals. It helps identify patterns of temporal dependence (Box & Jenkins, 1976).

### PACF (Partial Autocorrelation Function)

PACF measures the correlation between a time series and its lags, removing the influence of the intermediate lags. It is essential to determine the appropriate order in an AR(p) model (Box & Jenkins, 1976).

### Ljung-Box Test

The Ljung-Box Test statistically evaluates whether the autocorrelations of a time series differ from zero. Analysts commonly use it to check the independence of residuals in ARIMA models (Ljung & Box, 1978)

### Box-Pierce Test

Similar to the Ljung-Box test, the Box-Pierce Test is a statistical test that evaluates the independence of residuals in a time series model. It is a simpler and less refined version compared to the Ljung-Box test (Box & Pierce, 1970)

### KPSS Test

The KPSS Test (Kwiatkowski-Phillips-Schmidt-Shin) is a statistical test that checks the stationarity of a time series, mainly whether a series is stationary around its mean or a deterministic trend (Kwiatkowski et al., 1992)

### Box-Cox Transformation

The Box-Cox Transformation is a data transformation technique that applies a power function to stabilize variance and make the time series more closely resemble a normal distribution (Box & Cos, 1964)

### Kolmogorov-Smirnov Test

The Kolmogorov-Smirnov Test is a nonparametric test that compares a sample distribution with a reference probability distribution or compares two sample distributions to assess whether they differ significantly (Kolmogorov, 1933) (Smirnov, 1948)

### Shapiro-Wilk Test

The Shapiro-Wilk Test is a statistical test that evaluates the normality of a data set. It is particularly effective for small sample sizes and assesses whether a sample comes from a normally distributed population (Shapiro & Wilk, 1965)

## Applied Example

### Example one: basics testing

In this first example, we will analyze the United States GDP time series. We will use the `acfinter()` function to see the ACF, PACF, Box_Pierce, Pv_Box, Ljung_Box, and Pv_Ljung. We can also see the normality analysis and stationarity analysis. Finally, a plot with ACF, PACF, and Pv LJUNG BOX.

Therefore, we will use the following code to analyze the first ten lags and explain each result of the `acfinter()` function.

```python
db_GDP = GDP_data['GDP']
result = acfinter(db_GDP, lag = 10)
print(result)
```

<img src="https://i.ibb.co/mF5RLb1/README-example-2.png" alt="Example Image" style="width: 1000px; height: 360px;">

The outcome variable encompasses three primary tests: ACF-PACF, Stationarity, and Normality. The ACF-PACF component shows multiple lags significant correlations tested with Box-Pierce and Ljung-Box tests. Regarding stationarity tests, the function `acfinter()` provides ADF, KPSS-Level, KPSS-Trend, and PP results. While each test has nuances, their common aim is to determine if the series is stationary. Both the ADF and PP tests yield p-values of 0.99. Since these values exceed the significance level of 0.95, we do not reject the null hypothesis of stationarity, confirming the presence of a unit root and a trend component in the GDP time series.

In contrast, the KPSS-Level and KPSS-Trend tests both return p-values of 0.01, indicating the rejection of the null hypothesis in both cases. These tests show a non-stationary time series at any level or trend.

For the third component, the Shapiro-Wilk and Kolmogorov-Smirnov normality tests are used to conclude a non-normal distribution time series. These results lead us to reject the null hypothesis of normality.

Finally, a Box-Cox transformation test determine if a transformation was needed to stabilize the time series variance. Based on the test results, the transformations are:

* 1: No transformation.
* 0: Natural logarithm.
* 0.5: Square root.
* 2: Square.
* -1: Inverse.

The results in both tests are near 0, so the tests show we should apply to natural logarithm transformation.

### Example two: use the confidence interval

The output of the function `acfinter()` has been discussed. The following examples will explore how to utilize each argument of the function and provide important considerations for its proper application.

The argument `ci.method` allows for the selection of constant confidence intervals ("white") or dynamic confidence intervals ("ma"). The `ci` argument specifies any desired value between 0 and 0.99.

When utilizing these arguments, one would set the ci.method argument to "ma" and the ci argument to a confidence interval of 0.98. Thus, the following code can be used:

```bash
datag = DPIEEUU_dataset()
```
As illustrated, the function `acfinter()` with the arguments ci.method and ci adjusts the results according to the specified confidence interval. Additionally, it can be observed that the confidence intervals in the plot are not constant but display dynamic behavior.

## Example 3: Use the differences

Continuing GDP analysis, the "delta" argument can be employed to examine the first three differences in the time series. This analysis will focus on the first difference, and the following code will be utilized.

```bash
datag = DPIEEUU_dataset()
```
By setting the argument "delta" to "diff1", the function `acfinter()` will display the first difference of the time series. Firstly, the ACF-PACF test indicates significant autocorrelation at the 10th lag. The Box-Pierce and Ljung-Box tests confirm this finding supported by the plot.

The stationarity tests confirm the first difference in stationarity for the GDP time series; the null hypothesis is rejected. However, the KPSS test results, both at the level and trend, suggest that the first difference of the GDP time series is not stationary.

Conversely, the normality test indicates that the first difference of the GDP time series is not normally distributed, as the null hypothesis is rejected in both tests. It should be noted that the Box-Cox test for variance stabilization applies only to level time series and not to their differences.

### Example 4: Interactive mode

Finally, the function `acfinter()` lets users view the results interactively. The interactive argument should be used, and `acftable` should be specified. Additionally, dynamic visualization of the results is possible.

Moreover, results from a time series analysis can be downloaded by setting the download argument to TRUE, generating an Excel file containing the numerical results and a PNG image with a resolution of 300 dpi, which includes the ACF, PACF, and Ljung-Box Pv graphs. The files will be saved in the user's Documents folder. Below is an example of the code to use:

```bash
datag = DPIEEUU_dataset()
```

# Final considerations

You can analyze time series in xts, ts, integer, and vector (numeric) formats. So, if you use a different format, the `acfinter()` function won't work. In this case, you must convert your data to any format we initially showed you.

Finally, the packages that `acfinter()` uses for its operation are: xts (Ryan & Ulrich, 2020), tseries (Trapletti & Hornik, 2020), reactable (Glaz, 2023), openxlsx (Walker, 2023), plotly (Sievert, 2020), forecast (Hyndman & Khandakar, 2008) and stats (R Core Team, 2023).