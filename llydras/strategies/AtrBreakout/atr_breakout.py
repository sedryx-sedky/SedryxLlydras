from llydras.backtester.backtester import Backtester
from llydras.data.reader import read_csv
from llydras.interface.graph_portfolio import create_graph, create_graph_with_price
import pandas as pd


def atr_breakout_strategy(row, dataset, i):
    if i < 20:
        return {}

    window = 14
    atr = dataset['High'].rolling(window).max() - dataset['Low'].rolling(window).min()
    atr_value = atr.iloc[i]

    recent_high = dataset['High'].iloc[i - 5:i].max()
    recent_low = dataset['Low'].iloc[i - 5:i].min()
    price = dataset['Close'].iloc[i]

    breakout_up = recent_high + 0.2 * atr_value
    breakout_down = recent_low - 0.2 * atr_value

    if price > breakout_up:
        return {'action': 'buy', 'quantity': 1}
    elif price < breakout_down:
        return {'action': 'sell', 'quantity': 1}
    return {}


if __name__ == "__main__":
    # data = yf.download("QQQ", start="2000-01-01", threads=False) # Helps against rate limiting
    data = read_csv("etfs", "QQQ")

    price_data = data[['Close']].copy()
    price_data = price_data.reset_index().rename(columns={'index': 'timestamp'})
    price_data['timestamp'] = pd.to_datetime(price_data['timestamp'])

    backtester = Backtester(data, atr_breakout_strategy)
    backtester_result = backtester.run()
    print(backtester_result)
    create_graph_with_price(backtester_result["portfolio_value"], price_data)
