from typing import List, Callable, Dict, Any
import pandas as pd


class Trade:
    def __init__(self, timestamp, action, price, quantity):
        self.timestamp = timestamp
        self.action = action  # 'buy' or 'sell'
        self.price = price
        self.quantity = quantity

    def __repr__(self):
        return f"{self.timestamp}: {self.action.upper()} {self.quantity} @ {self.price:.2f}"


class Portfolio:
    def __init__(self, initial_cash: float):
        self.cash = initial_cash
        self.position = 0
        self.trades: List[Trade] = []

    def buy(self, timestamp, price, quantity):
        cost = price * quantity
        if self.cash >= cost:
            self.cash -= cost
            self.position += quantity
            self.trades.append(Trade(timestamp, 'buy', price, quantity))

    def sell(self, timestamp, price, quantity):
        if self.position >= quantity:
            self.cash += price * quantity
            self.position -= quantity
            self.trades.append(Trade(timestamp, 'sell', price, quantity))

    def value(self, current_price):
        return self.cash + self.position * current_price


class Backtester:
    def __init__(self, data: pd.DataFrame, strategy: Callable[[pd.Series, pd.DataFrame, int], Dict[str, Any]],
                 initial_cash: float = 10000):
        self.data = data
        self.strategy = strategy
        self.portfolio = Portfolio(initial_cash)
        self.history = []  # Cash value and number of stock positions over time

    def run(self):
        if self.data.empty:
            return {
                'final_value': self.portfolio.cash,
                'trades': [],
                'error': 'No data available for backtest.'
            }

        for i in range(len(self.data)):
            row = self.data.iloc[i]
            signal = self.strategy(row, self.data, i)
            price = row['Close']
            timestamp = row['Date']  # yfinance uses DatetimeIndex, so the backtester is coupled to that

            if signal.get('action') == 'buy':
                self.portfolio.buy(timestamp, price, signal.get('quantity', 1))
            elif signal.get('action') == 'sell':
                self.portfolio.sell(timestamp, price, signal.get('quantity', 1))

            self.history.append(
                {"value": self.portfolio.cash, "position": self.portfolio.position, "timestamp": timestamp})

        final_price = self.data.iloc[-1]['Close']

        # Convert history to a pandas dataframe
        portfolio_history = pd.DataFrame(self.history)

        # Parse timestamps to be interpreted by the graphs
        portfolio_history['timestamp'] = pd.to_datetime(portfolio_history['timestamp'])
        return {
            'final_value': self.portfolio.value(final_price),
            'trades': self.portfolio.trades,
            'portfolio_value': portfolio_history
        }
