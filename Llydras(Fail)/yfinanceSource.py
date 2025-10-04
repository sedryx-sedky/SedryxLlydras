import yfinance as yf

k = {'M': '1mo', 'D': '1d'}

def yfinanceSource(start, end, tickers, freq):

    return yf.download(' '.join(tickers), start = start, end = end, interval = k[freq], auto_adjust = False)['Close']