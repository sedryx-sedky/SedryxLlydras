from llydras.backtester.backtester import Backtester
from llydras.data.reader import read_csv
from llydras.interface.graph_portfolio import create_graph, create_graph_with_price
import pandas as pd


def atr_breakout_strategy(data, portfolio, i):
    if i < 20:
        return

    window = 14
    atr = data['High'].rolling(window).max() - data['Low'].rolling(window).min()
    atr_value = atr.iloc[i]

    recent_high = data['High'].iloc[i - 5:i].max()
    recent_low = data['Low'].iloc[i - 5:i].min()
    price = data['Close'].iloc[i]
    timestamp = data.index[i]

    breakout_up = recent_high + 0.5 * atr_value
    breakout_down = recent_low - 0.5 * atr_value

    if price > breakout_up:
        portfolio.buy(timestamp, price, quantity=1)
    elif price < breakout_down:
        portfolio.sell(timestamp, price, quantity=1)


if __name__ == "__main__":
    # data = yf.download("QQQ", start="2000-01-01", threads=False) # Helps against rate limiting
    data = read_csv("etfs", "QQQ")

    # Add technical data that will be used by the strategy
    data['MA_20'] = data['Close'].rolling(window=20).mean()
    data['MA_50'] = data['Close'].rolling(window=50).mean()
    data['Momentum'] = data['Close'].diff(5)  # 5-day momentum

    price_data = data[['Close']].copy()
    price_data = price_data.reset_index().rename(columns={'index': 'timestamp'})
    price_data['timestamp'] = pd.to_datetime(price_data['timestamp'])

    backtester = Backtester(data, atr_breakout_strategy)
    backtester_result = backtester.run()
    print(backtester_result)
    create_graph_with_price(backtester_result["portfolio_value"], price_data)
