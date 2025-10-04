import matplotlib.pyplot as plt
import pandas as pd
import matplotlib.dates as mdates
from matplotlib.ticker import MaxNLocator

def create_graph(portfolio_history):
    # Time axis (index)
    time = list(range(len(portfolio_history)))

    # Extract values and positions
    values = [point['value'] for point in portfolio_history]
    positions = [point['position'] for point in portfolio_history]

    # Plot both lines
    plt.plot(time, values, label='Value', marker='o')
    plt.plot(time, positions, label='Position', marker='x')

    # Add labels and title
    plt.xlabel('Time (Index)')
    plt.ylabel('Metric')
    plt.title('Value and Position over Time')
    plt.legend()
    plt.grid(True)
    plt.show()


def create_graph_with_price(portfolio_history, price_data):
    merged = pd.merge(portfolio_history, price_data, left_index=True, right_index=True)

    # Plot with dual y-axes
    fig, ax1 = plt.subplots()

    ax1.set_xlabel('Time')
    ax1.set_ylabel('Portfolio Value', color='tab:blue')
    ax1.plot(merged.index, merged['value'], label='Portfolio Value', color='tab:blue')
    ax1.tick_params(axis='y', labelcolor='tab:blue')

    ax2 = ax1.twinx()
    ax2.set_ylabel('Stock Price', color='tab:red')
    ax2.plot(merged.index, merged['Close'], label='Stock Price', color='tab:red')
    ax2.tick_params(axis='y', labelcolor='tab:red')

    fig.tight_layout()
    plt.title('Portfolio Value vs Stock Price Over Time')
    plt.show()
