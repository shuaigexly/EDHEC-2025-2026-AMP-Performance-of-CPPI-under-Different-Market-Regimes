import yfinance as yf
import pandas as pd
import numpy as np
import warnings
warnings.filterwarnings('ignore')

def fetch_financial_data():
    """
    Fetch S&P 500, CSI 300 index data and US 3-month Treasury Bill rates
    """
    print("Fetching financial data...")
    
    start_date = '2015-01-01'
    end_date = '2024-11-01'
    
    print("Downloading S&P 500 data...")
    spy = yf.download('SPY', start=start_date, end=end_date, auto_adjust=True)

    print("Downloading CSI 300 data...")
    ashare = yf.download('ASHR', start=start_date, end=end_date, auto_adjust=True)
    
    print("Downloading risk-free rate data...")
    try:
        irx = yf.download('^IRX', start=start_date, end=end_date, auto_adjust=True)
        risk_free_rate = irx['Close'].resample('D').last().fillna(method='ffill')
    except:
        print("Could not fetch ^IRX, using 2% proxy")
        date_range = pd.date_range(start=start_date, end=end_date, freq='D')
        risk_free_rate = pd.Series(2.0, index=date_range)
    
    return spy, ashare, risk_free_rate


def process_data(spy, ashare, risk_free_rate):
    print("Processing data...")
    
    data = pd.DataFrame()
    data['SP500'] = spy['Close']
    data['CSI300'] = ashare['Close']

    data = data.asfreq('B').ffill().dropna()

    risk_free_daily = risk_free_rate.resample('B').last().ffill()
    data['RF_Daily'] = (risk_free_daily / 100) / 252
    data['RF_Daily'] = data['RF_Daily'].reindex(data.index).ffill()
    
    data['SP500_Return'] = np.log(data['SP500'] / data['SP500'].shift(1))
    data['CSI300_Return'] = np.log(data['CSI300'] / data['CSI300'].shift(1))
    
    data = data.dropna()
    
    print(f"Processed data period: {data.index[0].date()} to {data.index[-1].date()}")
    print(f"Total observations: {len(data)}")
    
    return data
