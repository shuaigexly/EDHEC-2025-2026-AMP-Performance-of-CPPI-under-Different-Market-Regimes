import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from scipy import stats
from statsmodels.stats.diagnostic import acorr_ljungbox, het_arch
from matplotlib.patches import Patch

plt.style.use('seaborn-v0_8')


# ------------------------------------------------------
# 1. 计算某一段回报的统计指标
# ------------------------------------------------------
def calculate_statistics_for_period(returns):
    if len(returns) == 0:
        return {}

    annualized_mean = returns.mean() * 252
    annualized_std = returns.std() * np.sqrt(252)
    skewness = stats.skew(returns.dropna())
    kurtosis = stats.kurtosis(returns.dropna())

    try:
        lb = acorr_ljungbox(returns.dropna(), lags=10, return_df=True)
        lb_pvalue = lb['lb_pvalue'].iloc[-1]
    except:
        lb_pvalue = np.nan

    try:
        arch_stat, arch_pvalue, _, _ = het_arch(returns.dropna())
    except:
        arch_pvalue = np.nan

    return {
        'Annualized Mean': annualized_mean,
        'Annualized Std': annualized_std,
        'Skewness': skewness,
        'Kurtosis': kurtosis,
        'Ljung-Box p-value': lb_pvalue,
        'ARCH p-value': arch_pvalue,
        'Observations': len(returns)
    }


# ------------------------------------------------------
# 2. 计算 SP500 & CSI300 的全样本 + 各 regime 统计
# ------------------------------------------------------
def calculate_descriptive_stats(data, regimes):
    print("Calculating descriptive statistics...")
    results = {}

    for index_name in ['SP500', 'CSI300']:
        return_col = f'{index_name}_Return'
        regime_col = f'{index_name}_Regime_Label'

        combined = pd.DataFrame({
            'returns': data[return_col],
            'regime': regimes[regime_col]
        }).dropna()

        stats_dict = {}
        stats_dict['Full Sample'] = calculate_statistics_for_period(combined['returns'])

        for regime in combined['regime'].unique():
            r = combined[combined['regime'] == regime]['returns']
            stats_dict[regime] = calculate_statistics_for_period(r)

        results[index_name] = stats_dict

    return results


# ------------------------------------------------------
# 3. 绘制累计收益 + 市场状态背景色
# ------------------------------------------------------
def plot_returns_with_regimes(data, regimes):
    print("Plotting returns with regimes...")

    fig, axes = plt.subplots(2, 1, figsize=(16, 10))

    colors = {
        'Stable Bull': '#E6F2FF',
        'Volatile Bull': '#99CCFF',
        'Stable Bear': '#3399FF',
        'Panic Bear': '#0066CC'
    }

    legends = [Patch(facecolor=c, alpha=0.4, label=r) for r, c in colors.items()]

    for idx, (name, ax) in enumerate(zip(['SP500','CSI300'], axes)):
        cum = (1 + data[f'{name}_Return']).cumprod()
        ax.plot(cum.index, cum, color='navy', linewidth=2)

        regime_series = regimes[f'{name}_Regime_Label']

        current = regime_series.iloc[0]
        start = regime_series.index[0]

        for date, r in regime_series.iloc[1:].items():
            if r != current:
                ax.axvspan(start, date, color=colors[current], alpha=0.4)
                current = r
                start = date

        ax.axvspan(start, regime_series.index[-1], color=colors[current], alpha=0.4)

        ax.legend(handles=legends, loc='upper left')
        ax.set_title(name)

    plt.tight_layout()
    plt.show()


# ------------------------------------------------------
# 4. 打印表格结果（你 main.py 需要它）
# ------------------------------------------------------
def print_detailed_statistics(results):
    print("\n=========== DETAILED STATISTICS ===========\n")

    for index, stats_dict in results.items():
        print(f"\n---- {index} ----")
        for period, metrics in stats_dict.items():
            print(f"\n{period}")
            for k, v in metrics.items():
                print(f"  {k}: {v}")


# ------------------------------------------------------
# 5. 保存 Excel 文件
# ------------------------------------------------------
def save_data_to_excel(data, regimes, stats_results, filename="financial_analysis_data.xlsx"):
    print("Saving data to Excel...")

    with pd.ExcelWriter(filename) as writer:
        data.to_excel(writer, sheet_name='Processed Data')
        regimes.to_excel(writer, sheet_name='Regimes')

        for index_name, index_stats in stats_results.items():
            df = pd.DataFrame(index_stats).T
            df.to_excel(writer, sheet_name=f'{index_name} Stats')

    print("Saved to Excel.")
