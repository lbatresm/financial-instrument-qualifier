import yfinance as yf
import pandas as pd
from math import sqrt
import numpy as np




def _sort_history_dataframe (data: pd.DataFrame) -> pd.DataFrame:
    data = data[["Open", "Close", "High", "Low", "Dividends", "Stock Splits", "Volume"]]
    return data

def _get_volatility (ticker: str) -> float:
    """
    Function to compute volatility of returns, not volatility of prices
    """

    data = yf.download(ticker, period='max', repair=True, actions=True, rounding=True)

    # Compute logarithmic returns using Close price only
    close_prices = data['Close']
    log_returns = np.log(close_prices / close_prices.shift(1)).dropna()

    # Daily and annual volatility
    daily_vol = log_returns.std()
    annual_vol = daily_vol * np.sqrt(252)

    print(daily_vol)

    # Convert to scalar if it's a Series
    if isinstance(annual_vol, pd.Series):
        annual_vol = annual_vol.iloc[0]
    elif isinstance(annual_vol, np.ndarray):
        annual_vol = float(annual_vol)
    
    return float(annual_vol)



def main():

    ticker = "0P00000SUJ.F"
    ticker_volatility = _get_volatility(ticker)
    print(f"Volatilidad anual: {ticker_volatility:.2%}")

    # TODO: Adjust closing price to account for dividends and stock splits

    # TODO: Currency conversion


    

if __name__ == "__main__":
    main()