import pandas as pd


def read_csv(etfs_or_stocks, name):
    return pd.read_csv(f"C:/Users/44785/Documents/StockData/NASDAQ/{etfs_or_stocks}/{name}.csv", parse_dates=["Date"])
