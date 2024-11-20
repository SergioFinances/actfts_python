# Get Started

## Demo Data

This package includes a three-time series that automatically updates from the FRED (s.f) database of the United States. These datasets allow you to practice using the package’s functions. Below is a brief description of each:

**Gross Domestic Product**, This measure quantifies the total monetary value of all goods and services produced within a country over a specific period, typically a quarter or a year. It provides a comprehensive overview of a nation’s economic activity, reflecting its size and economic health. Economists often use GDP to compare economic performance across countries or regions and assess the impact of economic policies.

Below is a practical code example to retrieve GDP data.

```python
GDP_data = GDPEEUU_dataset()
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
db_GDP = GDP_data['GDPEEUU']
result = acfinter(db_GDP, lag = 10)
print(result)

(    Lag       ACF      PACF   Box_Pierce         Pv_Box    Ljung_Box       Pv_Ljung
1     0  0.984998  0.988186   300.768612   2.240358e-67   303.688695   5.177797e-68
2     1  0.970231  0.000853   592.586602  2.096304e-129   599.296530  7.318331e-131
3     2  0.955544 -0.005648   875.636514  1.704292e-189   886.956375  5.973796e-192
4     3  0.940949 -0.005204  1150.105700  1.042756e-247  1166.807310  2.498762e-251
5     4  0.926706  0.006052  1416.328609  3.986894e-304  1439.140253  4.545097e-309
6     5  0.912502 -0.007168  1674.453137   0.000000e+00  1704.057532   0.000000e+00
7     6  0.898587  0.003485  1924.765441   0.000000e+00  1961.804854   0.000000e+00
8     7  0.884970  0.004182  2167.548857   0.000000e+00  2212.627456   0.000000e+00
9     8  0.871686  0.006059  2403.098398   0.000000e+00  2456.785120   0.000000e+00
10    9  0.858883  0.012611  2631.779100   0.000000e+00  2694.613050   0.000000e+00,             

             Statistic  P_Value
ADF          8.948893     1.00
KPSS-Level   2.421314     0.01
KPSS-Trend   0.688871     0.01
PP           9.217001     1.00,                       

                     Statistic       P_Value
Shapiro Wilks        0.846595  6.921281e-17
Kolmogorov Smirnov   0.212903  1.450757e-06
Box Cox              0.124312           NaN)
```

<img src="https://i.ibb.co/gPDFtDd/Example-1-mkdocs-actfts.png" alt="Example Image" style="width: 1000px; height: 360px;">

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
db_GDP = GDP_data['GDPEEUU']
result = acfinter(db_GDP, lag = 10, ci_method = "ma", ci = 0.98)
print(result)

(    Lag       ACF      PACF   Box_Pierce         Pv_Box    Ljung_Box       Pv_Ljung
1     0  0.984998  0.988186   300.768612   2.240358e-67   303.688695   5.177797e-68
2     1  0.970231  0.000853   592.586602  2.096304e-129   599.296530  7.318331e-131
3     2  0.955544 -0.005648   875.636514  1.704292e-189   886.956375  5.973796e-192
4     3  0.940949 -0.005204  1150.105700  1.042756e-247  1166.807310  2.498762e-251
5     4  0.926706  0.006052  1416.328609  3.986894e-304  1439.140253  4.545097e-309
6     5  0.912502 -0.007168  1674.453137   0.000000e+00  1704.057532   0.000000e+00
7     6  0.898587  0.003485  1924.765441   0.000000e+00  1961.804854   0.000000e+00
8     7  0.884970  0.004182  2167.548857   0.000000e+00  2212.627456   0.000000e+00
9     8  0.871686  0.006059  2403.098398   0.000000e+00  2456.785120   0.000000e+00
10    9  0.858883  0.012611  2631.779100   0.000000e+00  2694.613050   0.000000e+00,    

             Statistic  P_Value
ADF          8.948893     1.00
KPSS-Level   2.421314     0.01
KPSS-Trend   0.688871     0.01
PP           9.217001     1.00,

                     Statistic       P_Value
Shapiro Wilks        0.846595  6.921281e-17
Kolmogorov Smirnov   0.196774  1.154750e-05
Box Cox              0.124312           NaN)
```

<img src="https://i.ibb.co/gV4ytJB/Example-2-mkdocs-actfts.png" alt="Example Image" style="width: 1000px; height: 360px;">

As illustrated, the function `acfinter()` with the arguments ci.method and ci adjusts the results according to the specified confidence interval. Additionally, it can be observed that the confidence intervals in the plot are not constant but display dynamic behavior.

### Example Three: Use the differences

Continuing GDP analysis, the "delta" argument can be employed to examine the first three differences in the time series. This analysis will focus on the first difference, and the following code will be utilized.

```python
db_GDP = GDP_data['GDPEEUU']
result = acfinter(db_GDP, lag = 10, delta = "diff1")
print(result)

(    Lag       ACF      PACF  Box_Pierce        Pv_Box   Ljung_Box      Pv_Ljung
1     0  0.154409  0.154910    7.367184  6.642486e-03    7.438943  6.382737e-03
2     1  0.278084  0.262190   31.262305  1.627334e-07   31.645400  1.343658e-07
3     2  0.269260  0.219267   53.665171  1.322574e-11   54.414327  9.154778e-12
4     3  0.212764  0.115314   67.653116  7.099425e-14   68.677444  4.316517e-14
5     4  0.279403  0.167227   91.775569  2.845872e-18   93.355348  1.324498e-18
6     5  0.155001  0.014507   99.199386  3.686059e-19  100.975174  1.570574e-19
7     6  0.204146  0.051024  112.077115  3.402988e-21  114.236676  1.211351e-21
8     7  0.153491  0.006622  119.357036  4.500494e-22  121.758455  1.436530e-22
9     8  0.165349  0.033302  127.805195  3.351084e-23  130.516380  9.286704e-24
10    9  0.155431  0.023311  135.270229  3.917246e-24  138.281014  9.481200e-25,

            Statistic       P_Value
ADF         -3.818244  2.726072e-03
KPSS-Level   1.928992  1.000000e-02
KPSS-Trend   0.201485  1.544302e-02
PP         -18.813147  2.022372e-30,

                     Statistic       P_Value
Shapiro Wilks        0.552883  2.316493e-27
Kolmogorov Smirnov   0.265372  5.652336e-10)
```

<img src="https://i.ibb.co/gy04VN5/Example-3-mkdocs-actfts.png" alt="Example Image" style="width: 1000px; height: 360px;">

By setting the argument "delta" to "diff1", the function `acfinter()` will display the first difference of the time series. Firstly, the ACF-PACF test indicates significant autocorrelation at the 10th lag. The Box-Pierce and Ljung-Box tests confirm this finding supported by the plot.

The stationarity tests confirm the first difference in stationarity for the GDP time series; the null hypothesis is rejected. However, the KPSS test results, both at the level and trend, suggest that the first difference of the GDP time series is not stationary.

Conversely, the normality test indicates that the first difference of the GDP time series is not normally distributed, as the null hypothesis is rejected in both tests. It should be noted that the Box-Cox test for variance stabilization applies only to level time series and not to their differences.

### Example Four: Interactive mode

Finally, the function `acfinter()` lets users view the results interactively. The interactive argument should be used, and `True` should be specified. Additionally, dynamic visualization of the results is possible.

Moreover, results from a time series analysis can be downloaded by setting the download argument to TRUE, generating an Excel file containing the numerical results. The file will be saved in the user's Documents folder. Below is an example of the code to use:

```python
db_GDP = GDP_data['GDPEEUU']
result = acfinter(db_GDP, lag = 10, interactive = True, download = True)
```

When you run the code, a link will appear in the terminal for you to access, as shown in the image.

<img src="https://i.ibb.co/GdbMBF3/Parte-1-Interactive.png" alt="Example Image" style="width: 230px; height: 80px;">

When you open the link, you can see a dashboard with four tabs will load in your browser, allowing you to interactively view the results of the ACF and PACF analysis, stationarity tests, normality tests, and a chart displaying the obtained results.

<img src="https://i.ibb.co/L5fy6ZQ/Parte-2-Interactive.png" alt="Example Image" style="width: 1000px; height: 360px;">

# Final considerations

You can analyze time series in xts, ts, integer, and vector (numeric) formats. So, if you use a different format, the `acfinter()` function won't work. In this case, you must convert your data to any format we initially showed you.

Finally, the packages that `acfinter()` uses for its operation are: NumPy (Harris et al., 2020); Matplotlib (Hunter, 2007); Statsmodels (Seabold, S & Perktold, 2010); ARCH (Sheppard, 2023); SciPy (Virtanen, 2020); Pandas (McKinney, 2010) and Plotly (Plotly Technologies Inc, 2024).