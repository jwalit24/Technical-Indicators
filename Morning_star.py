
import yfinance as yf
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt


def Morning_star_strategy():
    
# Define function to calculate returns based on strategy
 def calc_strategy_profit(df):
    # Calculate morning pattern
    # df['morning_star'] = (((df['Close'] > df['Open']) & df['Close']>df['Open'].shift(2)) & ( (abs(df['Close'].shift(1)-df['Open'].shift(1))/df['Close'].shift(1))<0.0001) & (df['Open'].shift(2) > df['Close'].shift(2)))
    df['morning_star'] = np.where((df['Close'].shift(2) < df['Open'].shift(2)) & (df['Open'].shift(1) < df['Close'].shift(2)) & (df['Close'].shift(1) < df['Close'].shift(2)) & (df['Close'].shift(1) > df['Open'].shift(1)) & (df['Open'] > df['Close'].shift(1)) & (df['Close'] > df['Open'].shift(2)), 1, 0)
    # Calculate returns
    df['profit'] = df['Close']-df['Close'].shift(1)
    # Calculate strategy profit
    df['strategy_profit'] = np.where(df['morning_star'].shift(1) , df['profit'], 0)
    # Calculate cumulative profit
    df['cumulative_profit'] = df['strategy_profit'].cumsum()
    # Calculate total return
    # print(df['cumulative_profit'])
    total_return = df['cumulative_profit']
    return total_return, df

# Define list of stocks
 stocks = ['AAPL', 'GOOG', 'TSLA', 'AMZN', 'MSFT', 'NFLX', 'NVDA', 'V', 'JPM']

# Define start and end dates
 start_date = '2022-01-01'
 end_date = '2022-12-31'

# Initialize dictionary to store results
 results = {}

# Loop over stocks
 for stock in stocks:
    # Download stock data
    data = yf.download(stock, start=start_date, end=end_date)
    # Calculate strategy profit
    total_return, data = calc_strategy_profit(data)
    # Store results in dictionary
    results[stock] = {'total_return': total_return, 'data': data}

# Plot cumulative profit for each stock
 for stock in stocks:
    plt.plot(results[stock]['total_return'], label=stock)
 plt.xlabel("time")
 plt.ylabel("profit")
 plt.legend()
 plt.show()

# Print results
 for stock in stocks:
    print(stock, ':', results[stock]['total_return'])

Morning_star_strategy()




