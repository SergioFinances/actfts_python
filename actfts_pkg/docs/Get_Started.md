# Get Started

## Demo Data

This package includes a three-time series that automatically updates from the FRED (s.f) database of the United States. These datasets allow you to practice using the package’s functions. Below is a brief description of each:

**Gross Domestic Product**, This measure quantifies the total monetary value of all goods and services produced within a country over a specific period, typically a quarter or a year. It provides a comprehensive overview of a nation’s economic activity, reflecting its size and economic health. Economists often use GDP to compare economic performance across countries or regions and assess the impact of economic policies.

Below is a practical code example to retrieve GDP data.

```python
GDP_data = DPIEEUU_dataset()
print(GDP_data.head())

               GDP
1947-03-31 243.164
1947-07-01 245.968
1947-10-01 249.585
1947-12-31 259.745
1948-03-31 265.742
1948-07-01 272.567
```

**Personal Consumption Expenditures** This represents the total value of goods and services consumed by households and nonprofit institutions serving households within an economy. As a critical component of GDP, PCE reveals consumer behavior and spending patterns. It covers expenditures on durable goods, non durable goods, and services, providing insights into consumer confidence and living standards.

Below is a handy code that allows you to retrieve PCE data

```python
PCEC_data = PCECEEUU_dataset()
print(PCEC_data.head())

              PCEC
1947-01-01 156.161
1947-04-01 160.031
1947-07-01 163.543
1947-10-01 167.672
1948-01-01 170.372
1948-04-01 174.142
```

**Disposable Personal Income** refers to the amount of money households have available for spending and saving after deducting taxes and other mandatory charges. It is an indicator of consumer purchasing power and financial health. DPI significantly impacts consumer spending and saving behaviors, affecting overall economic growth. Analysts frequently study DPI to identify trends in personal savings rates and consumption patterns.

Below is a practical code snippet for obtaining DPI data.

```python
DPI_data = DPIEEUU_dataset()
print(DPI_data.head())

               DPI
1947-03-31 170.548
1947-07-01 170.245
1947-10-01 178.047
1947-12-31 179.916
1948-03-31 185.295
1948-07-01 193.025
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

 $`ACF-PACF Test`
   lag       acf          pacf Box_Pierce Pv_Box Ljung_Box Pv_Ljung
1    1 0.9853471  0.9853470819   300.9818      0  303.9039        0
2    2 0.9709040 -0.0001677573   593.2047      0  599.9219        0
3    3 0.9565352 -0.0047242367   876.8421      0  888.1789        0
4    4 0.9422924 -0.0029745719  1152.0958      0 1168.8297        0
5    5 0.9284525  0.0065815855  1419.3232      0 1442.1902        0
6    6 0.9146149 -0.0068823059  1678.6445      0 1708.3357        0
7    7 0.9010486  0.0021906137  1930.3300      0 1967.4970        0
8    8 0.8877256  0.0014678003  2174.6276      0 2219.8839        0
9    9 0.8747132  0.0039691400  2411.8158      0 2465.7401        0
10  10 0.8620923  0.0067800862  2642.2087      0 2705.3488        0

$`Stationary Test`
           Statistic P_Value
ADF         2.586751    0.99
KPSS-Level  4.708600    0.01
KPSS-Trend  1.215522    0.01
PP          3.431542    0.99

$`Normality Test`
                   Statistic P_Value
Shapiro Wilks        0.84705       0
Kolmogorov Smirnov   0.17555       0
Box Cox              0.15000      NA
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

```python
db_GDP = GDP_data['GDP']
result = acfinter(db_GDP, lag = 10, ci_method = "ma", ci = 0.98)
print(result)

$`ACF-PACF Test`
   lag       acf          pacf Box_Pierce Pv_Box Ljung_Box Pv_Ljung
1    1 0.9849981  0.9849981360   300.7686      0  303.6887        0
2    2 0.9702311  0.0003276145   592.5866      0  599.2965        0
3    3 0.9555439 -0.0047507255   875.6365      0  886.9564        0
4    4 0.9409487 -0.0043825005  1150.1057      0 1166.8073        0
5    5 0.9267058  0.0043661368  1416.3286      0 1439.1403        0
6    6 0.9125019 -0.0058830766  1674.4531      0 1704.0575        0
7    7 0.8985872  0.0023755846  1924.7654      0 1961.8049        0
8    8 0.8849702  0.0028907399  2167.5489      0 2212.6275        0
9    9 0.8716864  0.0043086528  2403.0984      0 2456.7851        0
10  10 0.8588828  0.0093318494  2631.7791      0 2694.6130        0

$`Stationary Test`
           Statistic P_Value
ADF         2.548975    0.99
KPSS-Level  4.698172    0.01
KPSS-Trend  1.206680    0.01
PP          3.713440    0.99

$`Normality Test`
                   Statistic P_Value
Shapiro Wilks        0.84660       0
Kolmogorov Smirnov   0.17612       0
Box Cox              0.10000      NA
```
As illustrated, the function `acfinter()` with the arguments ci.method and ci adjusts the results according to the specified confidence interval. Additionally, it can be observed that the confidence intervals in the plot are not constant but display dynamic behavior.

### Example 3: Use the differences

Continuing GDP analysis, the "delta" argument can be employed to examine the first three differences in the time series. This analysis will focus on the first difference, and the following code will be utilized.

```python
db_GDP = GDP_data['GDP']
result = acfinter(db_GDP, lag = 10, delta = "diff1")
print(result)

$`ACF-PACF Test`
   lag       acf        pacf Box_Pierce       Pv_Box  Ljung_Box     Pv_Ljung
1    1 0.1544086 0.154408617   7.367184 6.642486e-03   7.438943 6.382737e-03
2    2 0.2780836 0.260451259  31.262305 1.627334e-07  31.645400 1.343658e-07
3    3 0.2692604 0.216815739  53.665171 1.322575e-11  54.414327 9.154788e-12
4    4 0.2127638 0.113243611  67.653116 7.094325e-14  68.677444 4.318768e-14
5    5 0.2794033 0.163670374  91.775569 0.000000e+00  93.355348 0.000000e+00
6    6 0.1550010 0.013327941  99.199386 0.000000e+00 100.975174 0.000000e+00
7    7 0.2041458 0.049165792 112.077115 0.000000e+00 114.236676 0.000000e+00
8    8 0.1534914 0.005921702 119.357036 0.000000e+00 121.758455 0.000000e+00
9    9 0.1653491 0.031889369 127.805195 0.000000e+00 130.516380 0.000000e+00
10  10 0.1554306 0.022115623 135.270229 0.000000e+00 138.281014 0.000000e+00

$`Stationary Test`
              Statistic    P_Value
ADF          -5.2254355 0.01000000
KPSS-Level    2.6917228 0.01000000
KPSS-Trend    0.2107036 0.01198615
PP         -375.4889572 0.01000000

$`Normality Test`
                   Statistic P_Value
Shapiro Wilks        0.55288       0
Kolmogorov Smirnov   0.27634       0
```
By setting the argument "delta" to "diff1", the function `acfinter()` will display the first difference of the time series. Firstly, the ACF-PACF test indicates significant autocorrelation at the 10th lag. The Box-Pierce and Ljung-Box tests confirm this finding supported by the plot.

The stationarity tests confirm the first difference in stationarity for the GDP time series; the null hypothesis is rejected. However, the KPSS test results, both at the level and trend, suggest that the first difference of the GDP time series is not stationary.

Conversely, the normality test indicates that the first difference of the GDP time series is not normally distributed, as the null hypothesis is rejected in both tests. It should be noted that the Box-Cox test for variance stabilization applies only to level time series and not to their differences.

### Example 4: Interactive mode

Finally, the function `acfinter()` lets users view the results interactively. The interactive argument should be used, and `acftable` should be specified. Additionally, dynamic visualization of the results is possible.

Moreover, results from a time series analysis can be downloaded by setting the download argument to TRUE, generating an Excel file containing the numerical results and a PNG image with a resolution of 300 dpi, which includes the ACF, PACF, and Ljung-Box Pv graphs. The files will be saved in the user's Documents folder. Below is an example of the code to use:

```python
datag = DPIEEUU_dataset()
```

# Final considerations

You can analyze time series in xts, ts, integer, and vector (numeric) formats. So, if you use a different format, the `acfinter()` function won't work. In this case, you must convert your data to any format we initially showed you.

Finally, the packages that `acfinter()` uses for its operation are: xts (Ryan & Ulrich, 2020), tseries (Trapletti & Hornik, 2020), reactable (Glaz, 2023), openxlsx (Walker, 2023), plotly (Sievert, 2020), forecast (Hyndman & Khandakar, 2008) and stats (R Core Team, 2023).