import numpy as np
import matplotlib.pyplot as plt
from statsmodels.tsa.stattools import acf, pacf
from statsmodels.stats.diagnostic import acorr_ljungbox
from statsmodels.tsa.stattools import adfuller
from statsmodels.tsa.stattools import kpss
from arch.unitroot import PhillipsPerron
import warnings
from statsmodels.tools.sm_exceptions import InterpolationWarning
import scipy.stats as stats
import pandas as pd

def acfinter(datag, lag=72, ci_method="white", ci=0.95, interactive=None,
             delta="levels", download=False):

    def gen(datag, delta="levels"):
        if not isinstance(datag, (np.ndarray, pd.Series)):
            raise ValueError("The input must be a numeric vector or a time series object.")
        
        if delta not in ["levels", "diff1", "diff2", "diff3"]:
            raise ValueError('The argument "delta" must be one of "levels", "diff1", "diff2", or "diff3".')
        
        if delta == "levels":
            return datag
        elif delta == "diff1":
            return np.diff(datag, n=1)
        elif delta == "diff2":
            return np.diff(datag, n=2)
        elif delta == "diff3":
            return np.diff(datag, n=3)
    
    data = gen(datag, delta)
    ldata = len(data)
    
    if ldata <= lag:
        lag = ldata - 1  # Adjust lag if it's larger than data length
    
    # Calcular ACF y PACF
    acf_vals, acf_confint = acf(data, nlags=lag, alpha=ci)
    pacf_vals, pacf_confint = pacf(data, nlags=lag, alpha=ci)

    # Calcular Box-Pierce
    Box_Pierce = acorr_ljungbox(data, lags=lag, boxpierce=True)

    # Crear el DataFrame con los resultados
    results_df = pd.DataFrame({
        'Lag': range(lag),
        'ACF': acf_vals[1:],
        'PACF': pacf_vals[1:],
        'Box_Pierce': Box_Pierce['bp_stat'],
        'Pv_Box': Box_Pierce['bp_pvalue'],
        'Ljung_Box': Box_Pierce['lb_stat'],
        'Pv_Ljung': Box_Pierce['lb_pvalue']
    })

    # Graficar ACF, PACF y Pv Ljung Box en un solo gráfico
    fig, ax = plt.subplots(3, 1, figsize=(10, 12))

    # ACF
    ax[0].stem(range(lag), acf_vals[1:], label='ACF', basefmt=" ")
    ax[0].set_title("Autocorrelation Function (ACF)")
    ax[0].set_xlabel('Lag')
    ax[0].set_ylabel('ACF')
    ax[0].grid(True, linestyle='--')

    # PACF
    ax[1].stem(range(lag), pacf_vals[1:], label='PACF', basefmt=" ")
    ax[1].set_title("Partial Autocorrelation Function (PACF)")
    ax[1].set_xlabel('Lag')
    ax[1].set_ylabel('PACF')
    ax[1].grid(True, linestyle='--')

    # Pv Ljung Box
    ax[2].plot(Box_Pierce['lb_stat'], label='Ljung-Box Statistic', color='red')
    ax[2].set_title("Ljung-Box Test (Pv)")
    ax[2].set_xlabel('Lag')
    ax[2].set_ylabel('Ljung-Box Stat')
    ax[2].grid(True, linestyle='--')
    
    plt.tight_layout()
    plt.show()

    # Stationarity test
    def stationarity_tests(data):
        with warnings.catch_warnings():
            warnings.filterwarnings("ignore", category=InterpolationWarning)
            adf = adfuller(data)
            kpss_level = kpss(data, regression='c')
            kpss_trend = kpss(data, regression='ct')
        
        return pd.DataFrame({
            'Statistic': [adf[0], kpss_level[0], kpss_trend[0]],
            'P_Value': [adf[1], kpss_level[1], kpss_trend[1]]
        }, index=["ADF", "KPSS-Level", "KPSS-Trend"])

    stationarity_results = stationarity_tests(data)
    
    # Normality Tests
    def normality_tests(data):
        if np.any(data <= 0):
            shapiro_result = stats.shapiro(data)
            ks_result = stats.ks_2samp(data, np.random.normal(np.mean(data), np.std(data), size=len(data)))
            return pd.DataFrame({
                'Statistic': [shapiro_result.statistic, ks_result.statistic],
                'P_Value': [shapiro_result.pvalue, ks_result.pvalue]
            }, index=["Shapiro Wilks", "Kolmogorov Smirnov"])


        else:
            shapiro_result = stats.shapiro(data)
            ks_result = stats.ks_2samp(data, np.random.normal(np.mean(data), np.std(data), size=len(data)))
            _, bc_lamda = stats.boxcox(data)
            return pd.DataFrame({
                'Statistic': [shapiro_result.statistic, ks_result.statistic, bc_lamda],
                'P_Value': [shapiro_result.pvalue, ks_result.pvalue, np.nan]
            }, index=["Shapiro Wilks", "Kolmogorov Smirnov", "Box Cox"])

    normality_results = normality_tests(data)

    return results_df, stationarity_results, normality_results

import os
import pandas as pd
import requests
from tempfile import NamedTemporaryFile

# Función para descargar y procesar cualquier dataset
def obtener_dataset(url, dataset_name):
    """Descarga y procesa el dataset desde una URL específica."""
    headers = {
        'Cache-Control': 'no-cache',  # Evitar caché
        'Pragma': 'no-cache'  # Para compatibilidad con navegadores antiguos
    }

    response = requests.get(url, headers=headers)
    response.raise_for_status()

    # Guardar el archivo temporalmente
    with NamedTemporaryFile(delete=False, suffix=".xls") as temp_file:
        temp_file.write(response.content)
        temp_file_path = temp_file.name

    # Leer y procesar los datos
    data = pd.read_excel(temp_file_path, skiprows=10, usecols=[1], names=[dataset_name])

    # Eliminar el archivo temporal
    os.remove(temp_file_path)

    # Generar el rango de fechas
    start_date = pd.to_datetime("1947-01-01")
    end_date = pd.to_datetime("today")
    date_range = pd.date_range(start=start_date, end=end_date, freq="QE")[:-1]

    # Asignar las fechas y configurar el índice
    data["Date"] = date_range
    data.set_index("Date", inplace=True)
    
    return data

def DPIEEUU_dataset():
    """Obtiene el dataset de DPIEEUU."""
    file_url = ("https://fred.stlouisfed.org/graph/fredgraph.xls?bgcolor=%23e1e9f0&chart_type=line&drp=0&fo=open%20sans&graph_bgcolor=%23ffffff&height=450&mode=fred&recession_bars=on&txtcolor=%23444444&ts=12&tts=12&width=1138&nt=0&thu=0&trc=0&show_legend=yes&show_axis_titles=yes&show_tooltip=yes&id=DPI&scale=left&cosd=1947-01-01&coed=2024-04-01&line_color=%234572a7&link_values=false&line_style=solid&mark_type=none&mw=3&lw=2&ost=-99999&oet=99999&mma=0&fml=a&fq=Quarterly&fam=avg&fgst=lin&fgsnd=2020-02-01&line_index=1&transformation=lin&vintage_date=2024-07-31&revision_date=2024-07-31&nd=1947-01-01")
    return obtener_dataset(file_url, "DPIEEUU")

def GDPEEUU_dataset():
    """Obtiene el dataset de GDPEEUU."""
    file_url = ("https://fred.stlouisfed.org/graph/fredgraph.xls?bgcolor=%23e1e9f0&chart_type=line&drp=0&fo=open%20sans&graph_bgcolor=%23ffffff&height=450&mode=fred&recession_bars=on&txtcolor=%23444444&ts=12&tts=12&width=1138&nt=0&thu=0&trc=0&show_legend=yes&show_axis_titles=yes&show_tooltip=yes&id=GDP&scale=left&cosd=1947-01-01&coed=2024-04-01&line_color=%234572a7&link_values=false&line_style=solid&mark_type=none&mw=3&lw=2&ost=-99999&oet=99999&mma=0&fml=a&fq=Quarterly&fam=avg&fgst=lin&fgsnd=2020-02-01&line_index=1&transformation=lin&vintage_date=2024-07-30&revision_date=2024-07-30&nd=1947-01-01")
    return obtener_dataset(file_url, "GDPEEUU")

def PCECEEUU_dataset():
    """Obtiene el dataset de PCECEEUU."""
    file_url = ("https://fred.stlouisfed.org/graph/fredgraph.xls?bgcolor=%23e1e9f0&chart_type=line&drp=0&fo=open%20sans&graph_bgcolor=%23ffffff&height=450&mode=fred&recession_bars=on&txtcolor=%23444444&ts=12&tts=12&width=1138&nt=0&thu=0&trc=0&show_legend=yes&show_axis_titles=yes&show_tooltip=yes&id=PCEC&scale=left&cosd=1947-01-01&coed=2024-04-01&line_color=%234572a7&link_values=false&line_style=solid&mark_type=none&mw=3&lw=2&ost=-99999&oet=99999&mma=0&fml=a&fq=Quarterly&fam=avg&fgst=lin&fgsnd=2020-02-01&line_index=1&transformation=lin&vintage_date=2024-07-31&revision_date=2024-07-31&nd=1947-01-01")
    return obtener_dataset(file_url, "PCECEEUU")

x = DPIEEUU_dataset()

x = x.squeeze()

eva = acfinter(x)
print(eva)
