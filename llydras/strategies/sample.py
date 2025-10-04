from llydras.backtester.backtester import Backtester
from llydras.data.reader import read_csv
from llydras.interface.graph_portfolio import create_graph
import yfinance as yf


def sample_strat(row):
    if row['Close'] < 100:
        return {'action': 'buy', 'quantity': 1}
    elif row['Close'] > 150:
        return {'action': 'sell', 'quantity': 1}
    return {}


if __name__ == "__main__":
    # data = yf.download("QQQ", start="2000-01-01", threads=False) # Helps against rate limiting
    data = read_csv("etfs", "QQQ")

    backtester = Backtester(data, sample_strat)
    backtester_result = backtester.run()
    print(backtester_result)
    create_graph(backtester_result["portfolio_value"])
