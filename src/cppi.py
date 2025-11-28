import pandas as pd
import numpy as np

def calculate_cppi_strategy(price_series, rf_series, initial_capital=100, protection_level=0.95, multiplier=4):
    n = len(price_series)

    pv = np.zeros(n)
    risk_alloc = np.zeros(n)
    floor = np.zeros(n)

    pv[0] = initial_capital
    floor[0] = initial_capital * protection_level
    cushion = pv[0] - floor[0]
    risk_alloc[0] = min(multiplier * cushion, pv[0])

    for t in range(1, n):
        r_risk = float(price_series.iloc[t] / price_series.iloc[t-1] - 1)
        r_safe = float(rf_series.iloc[t])

        prev_r = risk_alloc[t-1]
        prev_s = pv[t-1] - prev_r

        pv[t] = prev_r * (1+r_risk) + prev_s * (1+r_safe)
        floor[t] = floor[t-1] * (1+r_safe)

        cushion = pv[t] - floor[t]
        risk_alloc[t] = 0 if cushion <= 0 else min(multiplier*cushion, pv[t])

    return pd.DataFrame({
        'Portfolio_Value': pv,
        'Risk_Allocation': risk_alloc,
        'Safe_Allocation': pv - risk_alloc,
        'Floor_Value': floor,
        'Cushion': pv-floor
    }, index=price_series.index)


def run_cppi_analysis(data, regimes):
    print("Running CPPI strategy...")

    results = {}
    initial_capital = 100
    protection_level = 0.95
    multiplier = 4

    for name in ['SP500','CSI300']:
        price = data[name]
        r = data[f'{name}_Return']
        rf = data['RF_Daily']
        regime = regimes[f'{name}_Regime_Label']

        full = calculate_cppi_strategy(price, rf, initial_capital, protection_level, multiplier)
        cppi_ret = full['Portfolio_Value'].pct_change().dropna()

        results[name] = {
            'full_sample': {
                'cppi_returns': cppi_ret,
                'benchmark_returns': r,
                'cppi_values': full['Portfolio_Value']
            }
        }

    return results
