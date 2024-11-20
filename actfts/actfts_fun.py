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
from dash import Dash, dash_table, html, dcc
import base64
import io

def acfinter(datag, lag=72, ci_method="white", ci=0.95, interactive=None,
             delta="levels", download=False):
    
    """Perform autocorrelation (ACF), partial autocorrelation (PACF), and stationarity analysis.

    This function computes the autocorrelation function (ACF), partial autocorrelation function (PACF),
    and various stationarity tests for a given time series dataset. It also supports dynamic visualization
    of results and allows saving outputs.

    Parameters
    ----------
    datag : array-like
        The input time series data, which can be a numeric vector or a pandas Series.
    lag : int, optional
        Maximum number of lags to calculate ACF and PACF, by default 72.
    ci_method : str, optional
        Method for calculating confidence intervals for ACF and PACF, either "white" (default) 
        or "ma" (moving average).
    ci : float, optional
        Confidence level for ACF/PACF confidence intervals, by default 0.95.
    interactive : bool, optional
        If True, displays interactive plots; if None or False, produces static visualizations. 
        Default is None.
    delta : str, optional
        Transformation applied to the input data. Options are:
        - "levels" (default): no transformation,
        - "diff1": first differences,
        - "diff2": second differences,
        - "diff3": third differences.
    download : bool, optional
        If True, saves the output results as files. Default is False.

    Returns
    -------
    tuple
        - results_df (pd.DataFrame): A dataframe containing the ACF, PACF, Box-Pierce, and Ljung-Box statistics.
        - stationarity_results (pd.DataFrame): Results from stationarity tests (ADF, KPSS-Level, KPSS-Trend).
        - normality_results (pd.DataFrame): Results from normality tests (Shapiro-Wilks, Kolmogorov-Smirnov, Box-Cox if applicable).
    plot
        - tha ACF, PACF and pv ljung plots.

    Raises
    ------
    ValueError
        If the input data is not numeric or if `delta` or `ci_method` is invalid.

    Notes
    -----
    - Stationarity tests performed include:
      - Augmented Dickey-Fuller (ADF)
      - KPSS for level and trend
      - Phillips-Perron (PP)
    - Normality tests performed include:
      - Shapiro-Wilks
      - Kolmogorov-Smirnov
      - Box-Cox (only for positive data)
    - Confidence intervals for ACF/PACF can be computed using the white noise assumption or 
      moving average structure (ci_method="ma").
    - Box-Pierce and Ljung-Box statistics are calculated for serial correlation testing.
    """
    
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
        lag = ldata - 1
    
    acf_vals, acf_confint = acf(data, nlags=lag, alpha=ci)
    pacf_vals, pacf_confint = pacf(data, nlags=lag, alpha=ci)

    Box_Pierce = acorr_ljungbox(data, lags=lag, boxpierce=True)

    results_df = pd.DataFrame({
        'Lag': range(1, lag + 1),
        'ACF': acf_vals[1:],
        'PACF': pacf_vals[1:],
        'Box_Pierce': Box_Pierce['bp_stat'],
        'Pv_Box': Box_Pierce['bp_pvalue'],
        'Ljung_Box': Box_Pierce['lb_stat'],
        'Pv_Ljung': Box_Pierce['lb_pvalue']
    })

    def stationarity_tests(data):
        with warnings.catch_warnings():
            warnings.filterwarnings("ignore", category=InterpolationWarning)
            adf = adfuller(data)
            kpss_level = kpss(data, regression='c')
            kpss_trend = kpss(data, regression='ct')
            pp_result = PhillipsPerron(data)
        
        return pd.DataFrame({
            'Statistic': [adf[0], kpss_level[0], kpss_trend[0], pp_result.stat],
            'P_Value': [adf[1], kpss_level[1], kpss_trend[1], pp_result.pvalue]
        }, index=["ADF", "KPSS-Level", "KPSS-Trend", "PP"])

    stationarity_results = stationarity_tests(data)

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

    def get_clim1(x, ci=0.95, ci_type="white"):
        if ci_type not in ["white", "ma"]:
            raise ValueError('`ci_type` must be "white" or "ma"')
        
        clim0 = np.quantile(np.random.normal(size=100000), (1 + ci) / 2) / np.sqrt(ldata)
        
        if ci_type == "ma":
            clim = clim0 * np.sqrt(np.cumsum(np.concatenate(([1], 2 * results_df['ACF']**2))))
            return clim[:-1]
        else:
            lineci1 = np.full(len(results_df['ACF']), clim0)
            return lineci1

    def get_clim2(x, ci=0.95, ci_type="white"):
        if ci_type not in ["white", "ma"]:
            raise ValueError('`ci_type` must be "white" or "ma"')
        
        clim0 = np.quantile(np.random.normal(size=100000), (1 + ci) / 2) / np.sqrt(ldata)
        
        if ci_type == "ma":
            clim = clim0 * np.sqrt(np.cumsum(np.concatenate(([1], 2 * results_df['PACF']**2))))
            return clim[:-1]
        else:
            lineci2 = np.full(len(results_df['PACF']), clim0)
            return lineci2

    saveci1 = get_clim1(results_df['ACF'], ci=ci, ci_type=ci_method)
    saveci2 = get_clim2(results_df['PACF'], ci=ci, ci_type=ci_method)

    def fig_to_base64(fig):
        img_buf = io.BytesIO()
        fig.savefig(img_buf, format='png')
        img_buf.seek(0)
        return base64.b64encode(img_buf.read()).decode('utf-8')

    def generate_graphs():
        # Crear los gráficos
        fig, ax = plt.subplots(3, 1, figsize=(10, 12))

        ax[0].stem(range(len(acf_vals[1:])), acf_vals[1:], label='ACF', basefmt=" ")
        ax[0].set_title("Autocorrelation Function (ACF)")
        ax[0].set_xlabel('Lags')
        ax[0].set_ylabel('ACF')
        ax[0].grid(True, linestyle='dotted')
        if ci_method == "ma":
            ax[0].plot(range(len(saveci1)), saveci1, color='blue', linestyle='--', label='Upper CI')
            ax[0].plot(range(len(saveci1)), -saveci1, color='blue', linestyle='--', label='Lower CI')
        else:
            ax[0].axhline(y=saveci1[0], color='blue', linestyle='--', label='Upper CI')
            ax[0].axhline(y=-saveci1[0], color='blue', linestyle='--', label='Lower CI')

        ax[1].stem(range(len(pacf_vals[1:])), pacf_vals[1:], label='PACF', basefmt=" ")
        ax[1].set_title("Partial Autocorrelation Function (PACF)")
        ax[1].set_xlabel('Lags')
        ax[1].set_ylabel('PACF')
        ax[1].grid(True, linestyle='dotted')
        if ci_method == "ma":
            ax[1].plot(range(len(saveci2)), saveci2, color='blue', linestyle='--', label='Upper CI')
            ax[1].plot(range(len(saveci2)), -saveci2, color='blue', linestyle='--', label='Lower CI')
        else:
            ax[1].axhline(y=saveci2[0], color='blue', linestyle='--', label='Upper CI')
            ax[1].axhline(y=-saveci2[0], color='blue', linestyle='--', label='Lower CI')

        ax[2].plot(Box_Pierce['lb_pvalue'], label='Ljung-Box Statistic', color='red', linestyle='None', marker='o', markersize=5)
        ax[2].set_title("Ljung-Box Test (Pv)")
        ax[2].set_xlabel('Lags')
        ax[2].set_ylabel('Ljung-Box Stat')
        ax[2].grid(True, linestyle='dotted')
        ax[2].set_ylim(-0.02, 0.2)
        ax[2].axhline(y=0.05, color='blue', linestyle='--', label='0.05 Threshold')

        fig.subplots_adjust(hspace=0.52)

        # Convertir la figura a base64
        img_base64 = fig_to_base64(fig)
        return img_base64

    def show_dynamic_table():
        # Procesar los DataFrames en un formato unificado para ACF/PACF
        acf_pacf_results = results_df.copy()
        
        # Para Stationarity
        stationarity_results_mod = stationarity_results.reset_index().rename(columns={ 'index': 'Test', 'Statistic': 'Statistic', 'P_Value': 'P_Value' })

        # Para Normality
        normality_results_mod = normality_results.reset_index().rename(columns={ 'index': 'Test', 'Statistic': 'Statistic', 'P_Value': 'P_Value' })

        # Crear la aplicación Dash
        app = Dash(__name__)
        
        # Configurar la estructura básica del layout
        layout = html.Div([

            # Título
            html.H1("Interactive Results from Acfinter() Function", style={'text-align': 'center'}),

            # Tabs para las tablas
            dcc.Tabs([
                dcc.Tab(label='ACF/PACF', children=[
                    dash_table.DataTable(
                        id='acf-pacf-table',
                        columns=[{'name': col, 'id': col} for col in acf_pacf_results.columns],
                        data=acf_pacf_results.to_dict('records'),
                        page_size=10,
                        style_table={'height': '500px', 'overflowY': 'auto'},
                        style_cell={'textAlign': 'left', 'padding': '10px'},
                        style_header={'backgroundColor': 'lightgrey', 'fontWeight': 'bold'},
                        filter_action="native",
                        sort_action="native"
                    )
                ]),

                dcc.Tab(label='Stationarity', children=[
                    dash_table.DataTable(
                        id='stationarity-table',
                        columns=[{'name': col, 'id': col} for col in stationarity_results_mod.columns],
                        data=stationarity_results_mod.to_dict('records'),
                        page_size=10,
                        style_table={'height': '250px', 'overflowY': 'auto'},
                        style_cell={'textAlign': 'left', 'padding': '10px'},
                        style_header={'backgroundColor': 'lightgrey', 'fontWeight': 'bold'},
                        filter_action="native",
                        sort_action="native"
                    )
                ]),

                dcc.Tab(label='Normality', children=[
                    dash_table.DataTable(
                        id='normality-table',
                        columns=[{'name': col, 'id': col} for col in normality_results_mod.columns],
                        data=normality_results_mod.to_dict('records'),
                        page_size=10,
                        style_table={'height': '250px', 'overflowY': 'auto'},
                        style_cell={'textAlign': 'left', 'padding': '10px'},
                        style_header={'backgroundColor': 'lightgrey', 'fontWeight': 'bold'},
                        filter_action="native",
                        sort_action="native"
                    )
                ]),

                dcc.Tab(label='Plots', children=[
                    html.Div([
                        html.H3('ACF/PACF and PV Ljung', style={'textAlign': 'center'}),  # Centrar el título
                        html.Div([
                            html.Img(src=f"data:image/png;base64,{generate_graphs()}", style={'display': 'block', 'margin': '0 auto'})
                        ], style={'textAlign': 'center'})  # Centrar la imagen
                    ])
                ])
            ])
        ])
        
        app.layout = layout  # Asignar layout una sola vez

        # Ejecutar la aplicación Dash
        app.run_server(debug=True, use_reloader=False)

    # Condición para ejecutar la tabla interactiva
    if interactive:
        show_dynamic_table()
    else:
        fig, ax = plt.subplots(3, 1, figsize=(10, 12))

        ax[0].stem(range(len(acf_vals[1:])), acf_vals[1:], label='ACF', basefmt=" ")
        ax[0].set_title("Autocorrelation Function (ACF)")
        ax[0].set_xlabel('Lags')
        ax[0].set_ylabel('ACF')
        ax[0].grid(True, linestyle='dotted')
        if ci_method == "ma":
            ax[0].plot(range(len(saveci1)), saveci1, color='blue', linestyle='--', label='Upper CI')
            ax[0].plot(range(len(saveci1)), -saveci1, color='blue', linestyle='--', label='Lower CI')
        else:
            ax[0].axhline(y=saveci1[0], color='blue', linestyle='--', label='Upper CI')
            ax[0].axhline(y=-saveci1[0], color='blue', linestyle='--', label='Lower CI')

        ax[1].stem(range(len(pacf_vals[1:])), pacf_vals[1:], label='PACF', basefmt=" ")
        ax[1].set_title("Partial Autocorrelation Function (PACF)")
        ax[1].set_xlabel('Lags')
        ax[1].set_ylabel('PACF')
        ax[1].grid(True, linestyle='dotted')
        if ci_method == "ma":
            ax[1].plot(range(len(saveci2)), saveci2, color='blue', linestyle='--', label='Upper CI')
            ax[1].plot(range(len(saveci2)), -saveci2, color='blue', linestyle='--', label='Lower CI')
        else:
            ax[1].axhline(y=saveci2[0], color='blue', linestyle='--', label='Upper CI')
            ax[1].axhline(y=-saveci2[0], color='blue', linestyle='--', label='Lower CI')

        ax[2].plot(Box_Pierce['lb_pvalue'], label='Ljung-Box Statistic', color='red', linestyle='None', marker='o', markersize=5)
        ax[2].set_title("Ljung-Box Test (Pv)")
        ax[2].set_xlabel('Lags')
        ax[2].set_ylabel('Ljung-Box Stat')
        ax[2].grid(True, linestyle='dotted')
        ax[2].set_ylim(-0.02, 0.2)
        ax[2].axhline(y=0.05, color='blue', linestyle='--', label='0.05 Threshold')

        fig.subplots_adjust(hspace=0.52)
        plt.show()

    # Retornar las tablas procesadas
    return results_df, stationarity_results, normality_results

import os
import pandas as pd
import requests
from tempfile import NamedTemporaryFile

def obtener_dataset(url, dataset_name):
    headers = {
        'Cache-Control': 'no-cache',
        'Pragma': 'no-cache'
    }

    response = requests.get(url, headers=headers)
    response.raise_for_status()

    with NamedTemporaryFile(delete=False, suffix=".xls") as temp_file:
        temp_file.write(response.content)
        temp_file_path = temp_file.name

    data = pd.read_excel(temp_file_path, skiprows=10, usecols=[1], names=[dataset_name])

    os.remove(temp_file_path)

    start_date = pd.to_datetime("1947-01-01")
    end_date = pd.to_datetime("today")
    date_range = pd.date_range(start=start_date, end=end_date, freq="QE")[:-1]

    data["Date"] = date_range
    data.set_index("Date", inplace=True)
    
    return data

def DPIEEUU_dataset():
    """Retrieves the DPI dataset."""
    file_url = ("https://fred.stlouisfed.org/graph/fredgraph.xls?bgcolor=%23e1e9f0&chart_type=line&drp=0&fo=open%20sans&graph_bgcolor=%23ffffff&height=450&mode=fred&recession_bars=on&txtcolor=%23444444&ts=12&tts=12&width=1138&nt=0&thu=0&trc=0&show_legend=yes&show_axis_titles=yes&show_tooltip=yes&id=DPI&scale=left&cosd=1947-01-01&coed=2024-04-01&line_color=%234572a7&link_values=false&line_style=solid&mark_type=none&mw=3&lw=2&ost=-99999&oet=99999&mma=0&fml=a&fq=Quarterly&fam=avg&fgst=lin&fgsnd=2020-02-01&line_index=1&transformation=lin&vintage_date=2024-07-31&revision_date=2024-07-31&nd=1947-01-01")
    return obtener_dataset(file_url, "DPIEEUU")

def GDPEEUU_dataset():
    """Retrieves the GDP dataset."""
    file_url = ("https://fred.stlouisfed.org/graph/fredgraph.xls?bgcolor=%23e1e9f0&chart_type=line&drp=0&fo=open%20sans&graph_bgcolor=%23ffffff&height=450&mode=fred&recession_bars=on&txtcolor=%23444444&ts=12&tts=12&width=1138&nt=0&thu=0&trc=0&show_legend=yes&show_axis_titles=yes&show_tooltip=yes&id=GDP&scale=left&cosd=1947-01-01&coed=2024-04-01&line_color=%234572a7&link_values=false&line_style=solid&mark_type=none&mw=3&lw=2&ost=-99999&oet=99999&mma=0&fml=a&fq=Quarterly&fam=avg&fgst=lin&fgsnd=2020-02-01&line_index=1&transformation=lin&vintage_date=2024-07-30&revision_date=2024-07-30&nd=1947-01-01")
    return obtener_dataset(file_url, "GDPEEUU")

def PCECEEUU_dataset():
    """Retrieves the PCEC dataset."""
    file_url = ("https://fred.stlouisfed.org/graph/fredgraph.xls?bgcolor=%23e1e9f0&chart_type=line&drp=0&fo=open%20sans&graph_bgcolor=%23ffffff&height=450&mode=fred&recession_bars=on&txtcolor=%23444444&ts=12&tts=12&width=1138&nt=0&thu=0&trc=0&show_legend=yes&show_axis_titles=yes&show_tooltip=yes&id=PCEC&scale=left&cosd=1947-01-01&coed=2024-04-01&line_color=%234572a7&link_values=false&line_style=solid&mark_type=none&mw=3&lw=2&ost=-99999&oet=99999&mma=0&fml=a&fq=Quarterly&fam=avg&fgst=lin&fgsnd=2020-02-01&line_index=1&transformation=lin&vintage_date=2024-07-31&revision_date=2024-07-31&nd=1947-01-01")
    return obtener_dataset(file_url, "PCECEEUU")

datag = GDPEEUU_dataset()
data = datag["GDPEEUU"]

x = acfinter(data, interactive=True)
print(x)