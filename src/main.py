from data_fetch import fetch_financial_data, process_data
from regimes import identify_market_regimes
from stats_module import (
    calculate_descriptive_stats, plot_returns_with_regimes,
    print_detailed_statistics, save_data_to_excel
)
from cppi import run_cppi_analysis
from buy_hold import run_buy_hold_analysis
from bookstrap import (
    run_block_bootstrap_simulation,
    calculate_comprehensive_metrics,
    plot_comparison_table
)

def main():

    print("\n=== MODULE 1 — Data Fetching ===")
    spy, ashare, rf = fetch_financial_data()
    data = process_data(spy, ashare, rf)

    print("\n=== MODULE 2 — Market Regimes ===")
    regimes = identify_market_regimes(data)

    print("\n=== MODULE 3 — Statistics & Charts ===")
    stats = calculate_descriptive_stats(data, regimes)
    plot_returns_with_regimes(data, regimes)
    print_detailed_statistics(stats)
    save_data_to_excel(data, regimes, stats)

    print("\n=== MODULE 4 — CPPI Strategy ===")
    cppi_results = run_cppi_analysis(data, regimes)

    print("\n=== MODULE 5 — Buy & Hold ===")
    bh_results = run_buy_hold_analysis(data, regimes)

    print("\n=== MODULE 6 — Block Bootstrap Simulation ===")
    bootstrap_results = run_block_bootstrap_simulation(data, regimes, 1000)
    summary_df = calculate_comprehensive_metrics(bootstrap_results)
    
    if not summary_df.empty:
        plot_comparison_table(summary_df)
        summary_df.to_excel("strategy_comparison_results.xlsx", index=False)

    print("\n=== All tasks completed successfully! ===")

if __name__ == "__main__":
    main()
