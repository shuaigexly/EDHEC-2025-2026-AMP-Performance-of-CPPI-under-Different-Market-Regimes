import pandas as pd
import numpy as np
from sklearn.utils import resample

def block_bootstrap_sample(data, block_size=20, n_samples=252):
    n_blocks = int(np.ceil(n_samples / block_size))
    idx = []

    for _ in range(n_blocks):
        start = np.random.randint(0, len(data)-block_size)
        idx.extend(list(range(start, start+block_size)))

    return data.iloc[idx[:n_samples]]


def evaluate_strategy_performance(returns, initial=100):
    if len(returns) == 0: return None

    pv = (1 + returns).cumprod() * initial

    total = (pv.iloc[-1]/initial - 1)
    ann = (1+total)**(252/len(returns)) - 1
    std = returns.std() * np.sqrt(252)

    neg_pct = (returns < 0).mean() * 100
    var5 = np.percentile(returns, 5) * 100

    return {
        'Average Return': ann,
        'Standard Deviation': std,
        '% < 0': neg_pct,
        'VaR 5%': var5,
        'Skewness': returns.skew(),
        'Kurtosis': returns.kurtosis()
    }


def calculate_information_ratio(cppi, bh):
    m = min(len(cppi), len(bh))
    if m == 0: return 0

    excess = cppi[:m] - bh[:m]
    annualized = excess.mean() * 252
    te = excess.std() * np.sqrt(252)
    return annualized / te if te>0 else 0


def run_block_bootstrap_simulation(data, regimes, n_simulations=1000):
    print("Running bootstrap simulation...")

    results = {}

    for market in ['SP500','CSI300']:
        returns = data[f'{market}_Return'].dropna()

        results[market] = {'CPPI':[], 'BH':[], 'Excess':[]}

        for sim in range(n_simulations):
            sample = block_bootstrap_sample(returns)

            if len(sample) < 252:
                continue

            prices = (1 + sample).cumprod() * 100

            avg_rf = data['RF_Daily'].mean()
            rf_series = pd.Series([avg_rf]*len(prices), index=sample.index)

            from cppi import calculate_cppi_strategy
            cppi = calculate_cppi_strategy(prices, rf_series)
            cppi_ret = cppi['Portfolio_Value'].pct_change().dropna()

            bh_ret = sample

            m = min(len(cppi_ret), len(bh_ret))
            excess = cppi_ret.iloc[:m] - bh_ret.iloc[:m]

            results[market]['CPPI'].append(cppi_ret.iloc[:m])
            results[market]['BH'].append(bh_ret.iloc[:m])
            results[market]['Excess'].append(excess)

    return results


def calculate_comprehensive_metrics(results):
    rows = []

    for market, strategies in results.items():
        cppi_list = strategies['CPPI']
        bh_list = strategies['BH']
        exc_list = strategies['Excess']

        avg_cppis = []
        avg_bhs = []
        info_ratios = []

        for cppi, bh, exc in zip(cppi_list, bh_list, exc_list):
            cppi_m = evaluate_strategy_performance(cppi)
            bh_m = evaluate_strategy_performance(bh)
            ir = calculate_information_ratio(cppi, bh)

            avg_cppis.append(cppi_m)
            avg_bhs.append(bh_m)
            info_ratios.append(ir)

        df = pd.DataFrame({
            'Scenario': market,
            'CPPI Avg Return': np.mean([x['Average Return'] for x in avg_cppis]),
            'BH Avg Return': np.mean([x['Average Return'] for x in avg_bhs]),
            'Info Ratio': np.mean(info_ratios),
        }, index=[0])

        rows.append(df)

    return pd.concat(rows, ignore_index=True)


def plot_comparison_table(df):
    print("\n=== Strategy Comparison ===\n")
    print(df.to_string(index=False))
