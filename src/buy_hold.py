import pandas as pd
import numpy as np

def calculate_buy_hold_strategy(price_data, initial_capital=100):
    pv = (price_data / price_data.iloc[0]) * initial_capital
    return pd.DataFrame({
        'Portfolio_Value': pv,
        'Returns': pv.pct_change().dropna()
    })


def run_buy_hold_analysis(data, regimes):
    print("Running Buy-and-Hold analysis...")

    results = {}

    for name in ['SP500','CSI300']:
        returns = data[f'{name}_Return']
        values = (1 + returns).cumprod() * 100

        results[name] = {
            'full_sample': {
                'returns': returns,
                'values': values
            }
        }

    return results
