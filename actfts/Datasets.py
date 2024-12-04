import os
import pandas as pd
import requests
from tempfile import NamedTemporaryFile

def obtener_dataset(url, dataset_name):
    """
    Downloads an Excel file from a URL, processes it to extract a dataset, 
    and returns a DataFrame with a column of values associated with a time series.

    Parameters
    ----------
    url : str
        The URL of the Excel file containing the dataset to be processed.
    dataset_name : str
        The name of the column to assign to the extracted dataset.

    Returns
    -------
    pd.DataFrame
        A pandas DataFrame with the processed data, where:
        - The index is a time series with quarterly frequency starting from 1947-01-01.
        - A column with the name specified in `dataset_name` contains the extracted data.

    Raises
    ------
    requests.exceptions.HTTPError
        If an error occurs while downloading the file from the provided URL.
    """
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
    """
    Downloads and processes the Disposable Personal Income (DPI) dataset for the United States 
    from the Federal Reserve Economic Data (FRED) system. The data is quarterly and starts 
    from January 1947.

    Returns
    -------
    pd.DataFrame
        A pandas DataFrame containing:
        - A time series index with quarterly frequency.
        - A single column labeled "DPIEEUU" representing the Disposable Personal Income values.

    Raises
    ------
    requests.exceptions.HTTPError
        If there is an issue with downloading the dataset from the provided URL.

    Examples
    --------
    >>> df = DPIEEUU_dataset()
    >>> print(df.head())

                 DPIEEUU
    Date               
    1947-03-31  123.456
    1947-06-30  127.890
    1947-09-30  130.567
    1947-12-31  135.234
    1948-03-31  140.123
    """
    file_url = ("https://fred.stlouisfed.org/graph/fredgraph.xls?bgcolor=%23e1e9f0&chart_type=line&drp=0&fo=open%20sans&graph_bgcolor=%23ffffff&height=450&mode=fred&recession_bars=on&txtcolor=%23444444&ts=12&tts=12&width=1138&nt=0&thu=0&trc=0&show_legend=yes&show_axis_titles=yes&show_tooltip=yes&id=DPI&scale=left&cosd=1947-01-01&coed=2024-04-01&line_color=%234572a7&link_values=false&line_style=solid&mark_type=none&mw=3&lw=2&ost=-99999&oet=99999&mma=0&fml=a&fq=Quarterly&fam=avg&fgst=lin&fgsnd=2020-02-01&line_index=1&transformation=lin&vintage_date=2024-07-31&revision_date=2024-07-31&nd=1947-01-01")
    return obtener_dataset(file_url, "DPIEEUU")

def GDPEEUU_dataset():
    """
    Downloads and processes the Gross Domestic Product (GDP) dataset for the United States 
    from the Federal Reserve Economic Data (FRED) system. The data is quarterly and starts 
    from January 1947.

    Returns
    -------
    pd.DataFrame
        A pandas DataFrame containing:
        - A time series index with quarterly frequency.
        - A single column labeled "GDPEEUU" representing the GDP values.

    Raises
    ------
    requests.exceptions.HTTPError
        If there is an issue with downloading the dataset from the provided URL.

    Examples
    --------
    >>> df = GDPEEUU_dataset()
    >>> print(df.head())

                 GDPEEUU
    Date               
    1947-03-31  200.456
    1947-06-30  210.890
    1947-09-30  220.567
    1947-12-31  230.234
    1948-03-31  240.123
    """
    file_url = ("https://fred.stlouisfed.org/graph/fredgraph.xls?bgcolor=%23e1e9f0&chart_type=line&drp=0&fo=open%20sans&graph_bgcolor=%23ffffff&height=450&mode=fred&recession_bars=on&txtcolor=%23444444&ts=12&tts=12&width=1138&nt=0&thu=0&trc=0&show_legend=yes&show_axis_titles=yes&show_tooltip=yes&id=GDP&scale=left&cosd=1947-01-01&coed=2024-04-01&line_color=%234572a7&link_values=false&line_style=solid&mark_type=none&mw=3&lw=2&ost=-99999&oet=99999&mma=0&fml=a&fq=Quarterly&fam=avg&fgst=lin&fgsnd=2020-02-01&line_index=1&transformation=lin&vintage_date=2024-07-30&revision_date=2024-07-30&nd=1947-01-01")
    return obtener_dataset(file_url, "GDPEEUU")

def PCECEEUU_dataset():
    """
    Downloads and processes the Personal Consumption Expenditures (PCEC) dataset for the United States 
    from the Federal Reserve Economic Data (FRED) system. The data is quarterly and starts 
    from January 1947.

    Returns
    -------
    pd.DataFrame
        A pandas DataFrame containing:
        - A time series index with quarterly frequency.
        - A single column labeled "PCECEEUU" representing the PCEC values.

    Raises
    ------
    requests.exceptions.HTTPError
        If there is an issue with downloading the dataset from the provided URL.

    Examples
    --------
    >>> df = PCECEEUU_dataset()
    >>> print(df.head())

                 PCECEEUU
    Date               
    1947-03-31  300.456
    1947-06-30  310.890
    1947-09-30  320.567
    1947-12-31  330.234
    1948-03-31  340.123
    """
    file_url = ("https://fred.stlouisfed.org/graph/fredgraph.xls?bgcolor=%23e1e9f0&chart_type=line&drp=0&fo=open%20sans&graph_bgcolor=%23ffffff&height=450&mode=fred&recession_bars=on&txtcolor=%23444444&ts=12&tts=12&width=1138&nt=0&thu=0&trc=0&show_legend=yes&show_axis_titles=yes&show_tooltip=yes&id=PCEC&scale=left&cosd=1947-01-01&coed=2024-04-01&line_color=%234572a7&link_values=false&line_style=solid&mark_type=none&mw=3&lw=2&ost=-99999&oet=99999&mma=0&fml=a&fq=Quarterly&fam=avg&fgst=lin&fgsnd=2020-02-01&line_index=1&transformation=lin&vintage_date=2024-07-31&revision_date=2024-07-31&nd=1947-01-01")
    return obtener_dataset(file_url, "PCECEEUU")