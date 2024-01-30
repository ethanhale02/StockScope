#Imports / API key
import csv
import requests
import pandas as pd
import plotly.graph_objects as go
from IPython.display import display, HTML
from ipywidgets import interact_manual,interact, widgets
from ipywidgets import AppLayout, Button, Layout
api_key = '' #Enter API key here

# Functions
def get_stock_data(Stock):
    url = f'https://www.alphavantage.co/query?function=TIME_SERIES_INTRADAY&symbol={Stock}&interval=60min&apikey={api_key}'
    response = requests.get(url)
    response.raise_for_status()
    data = response.json()
    return data

def add_to_dataframe(data):
    time = data['Time Series (60min)']
    data_df = pd.DataFrame(time)
    return data_df

def Create_dict(data_df):
    open_dic = {}
    close_dic = {}
    high_dic = {}
    low_dic = {}
    vol_dic = {}
    for i in data_df:
        info = data_df[i]
        open_dic[i]= float(info[0])
        close_dic[i] = float(info[3])
        high_dic[i] = float(info[1])
        low_dic[i] = float(info[2])
        vol_dic[i] = int(info[4])
    return open_dic, close_dic, high_dic, low_dic, vol_dic

def create_openclose_df(open_dic, close_dic):
    openclose_df = pd.DataFrame({'open':pd.Series(open_dic),'close':pd.Series(close_dic)})
    return openclose_df

def create_highlow_df(high_dic, low_dic):
    highlow_df = pd.DataFrame({'high':pd.Series(high_dic),'low':pd.Series(low_dic)})
    return highlow_df

def create_vol_df(vol_dic):
    vol_df = pd.DataFrame({'vol':pd.Series(vol_dic)})
    return vol_df

def make_ticker_list():
    with open("us_symbols.csv", 'r') as ticker_file:
        ticker = csv.DictReader(ticker_file)
        ticker_list = []
        for row in ticker:
            ticker_list.append(row['ticker'])
    return ticker_list

# Main Code
ticker_list = make_ticker_list()
display(HTML("<h1>StockScope</h1>"))
@interact(Stock=ticker_list)
def display_graph_and_df(Stock):
    data = get_stock_data(Stock)
    data_df = pd.DataFrame(data['Time Series (60min)'])
    open_dic, close_dic, high_dic, low_dic, vol_dic = Create_dict(data_df)
    openclose_df = create_openclose_df(open_dic, close_dic)
    highlow_df = create_highlow_df(high_dic, low_dic)
    vol_df = create_vol_df(vol_dic)
    HL_graph = highlow_df.plot.line(y = ['high', 'low'], figsize = (12,8), title = "High/Low Graph", ylabel = "USD", xlabel = "Date/Time", style = ["+-", "o-"])
    OC_graph = openclose_df.plot.line(y = ['open', 'close'], figsize = (12,8), title = "Open/Close Graph", ylabel = "USD", xlabel = "Date/Time", style = ["+-", "o-"])
    vol_graph = vol_df[0:35].plot.bar(y = 'vol', figsize = (12,4), title = "Volume Graph", ylabel = "Sale Volume", xlabel = "Date/Time")
    display(data_df)
