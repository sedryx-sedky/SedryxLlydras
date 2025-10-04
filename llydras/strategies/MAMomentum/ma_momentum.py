from llydras.backtester.backtester import Backtester
from llydras.data.reader import read_csv
from llydras.interface.graph_portfolio import create_graph, create_graph_with_price
import pandas as pd


def ma_momentum_strategy(row, dataset, i):
    # Assumes row includes these columns: 'Close', 'MA_20', 'MA_50', 'Momentum'
    if row['MA_20'] > row['MA_50'] and row['Momentum'] > 0:
        return {'action': 'buy', 'quantity': 1}
    elif row['MA_20'] < row['MA_50'] and row['Momentum'] < 0:
        return {'action': 'sell', 'quantity': 1}
    return {}


if __name__ == "__main__":
    # data = yf.download("QQQ", start="2000-01-01", threads=False) # Helps against rate limiting
    data = read_csv("etfs", "QQQ")

    # Add technical data that will be used by the strategy
    data['MA_20'] = data['Close'].rolling(window=20).mean()
    data['MA_50'] = data['Close'].rolling(window=50).mean()
    data['Momentum'] = data['Close'].diff(5)  # 5-day momentum

    # Get a copy of the stock prices to graph
    price_data = data[['Close']].copy()
    price_data = price_data.reset_index().rename(columns={'index': 'timestamp'})
    price_data['timestamp'] = pd.to_datetime(price_data['timestamp'])

    backtester = Backtester(data, ma_momentum_strategy)
    backtester_result = backtester.run()
    print(backtester_result)
    create_graph_with_price(backtester_result["portfolio_value"], price_data)
