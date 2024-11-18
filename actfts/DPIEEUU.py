import os
import pandas as pd
import requests
from tempfile import NamedTemporaryFile

def DPIEEUU_dataset ():
    file_url = ("https://fred.stlouisfed.org/graph/fredgraph.xls?"
                "bgcolor=%23e1e9f0&chart_type=line&drp=0&fo=open%20sans&"
                "graph_bgcolor=%23ffffff&height=450&mode=fred&recession_bars=on&"
                "txtcolor=%23444444&ts=12&tts=12&width=1138&nt=0&thu=0&trc=0&"
                "show_legend=yes&show_axis_titles=yes&show_tooltip=yes&id=DPI&"
                "scale=left&cosd=1947-01-01&coed=2024-04-01&line_color=%234572a7&"
                "link_values=false&line_style=solid&mark_type=none&mw=3&lw=2&"
                "ost=-99999&oet=99999&mma=0&fml=a&fq=Quarterly&fam=avg&fgst=lin&"
                "fgsnd=2020-02-01&line_index=1&transformation=lin&vintage_date=2024-07-31&"
                "revision_date=2024-07-31&nd=1947-01-01")

    response = requests.get(file_url)
    response.raise_for_status()

    with NamedTemporaryFile(delete=False, suffix=".xls") as temp_file:
        temp_file.write(response.content)
        temp_file_path = temp_file.name

    data = pd.read_excel(temp_file_path, skiprows=10, usecols=[1], names=["DPI"])

    os.remove(temp_file_path)

    start_date = pd.to_datetime("1947-01-01")
    end_date = pd.to_datetime("today")
    date_range = pd.date_range(start=start_date, end=end_date, freq="QE")[:-1]

    data["Date"] = date_range
    data.set_index("Date", inplace=True)
    return data

def save_data(data, file_path="actfts/data/DPIEEUU.csv"):
    os.makedirs(os.path.dirname(file_path), exist_ok=True)
    data.to_csv(file_path, index=False)
    print(f"Data saved to {file_path}")

def load_data(file_path="actfts/data/DPIEEUU.csv"):
    data = pd.read_csv(file_path, parse_dates=["Date"])
    return data