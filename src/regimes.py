import pandas as pd
import numpy as np

def identify_market_regimes(data, window=126):
    print("Identifying market regimes...")

    regimes = pd.DataFrame(index=data.index)
    
    regimes['SP500_Rolling_Return'] = data['SP500'].pct_change(window)
    regimes['SP500_Rolling_Vol'] = data['SP500_Return'].rolling(window).std()

    regimes['CSI300_Rolling_Return'] = data['CSI300'].pct_change(window)
    regimes['CSI300_Rolling_Vol'] = data['CSI300_Return'].rolling(window).std()
    
    sp_vol_median = regimes['SP500_Rolling_Vol'].median()
    regimes['SP500_Trend'] = np.where(regimes['SP500_Rolling_Return'] > 0, 'Bull', 'Bear')
    regimes['SP500_Vol_Regime'] = np.where(regimes['SP500_Rolling_Vol'] > sp_vol_median, 'High', 'Low')
    regimes['SP500_Regime'] = regimes['SP500_Trend'] + '_' + regimes['SP500_Vol_Regime']

    csi_vol_median = regimes['CSI300_Rolling_Vol'].median()
    regimes['CSI300_Trend'] = np.where(regimes['CSI300_Rolling_Return'] > 0, 'Bull', 'Bear')
    regimes['CSI300_Vol_Regime'] = np.where(regimes['CSI300_Rolling_Vol'] > csi_vol_median, 'High', 'Low')
    regimes['CSI300_Regime'] = regimes['CSI300_Trend'] + '_' + regimes['CSI300_Vol_Regime']

    regimes = regimes.dropna()
    
    regime_map = {
        'Bull_High': 'Volatile Bull',
        'Bull_Low': 'Stable Bull',
        'Bear_High': 'Panic Bear',
        'Bear_Low': 'Stable Bear'
    }
    
    regimes['SP500_Regime_Label'] = regimes['SP500_Regime'].map(regime_map)
    regimes['CSI300_Regime_Label'] = regimes['CSI300_Regime'].map(regime_map)
    
    return regimes
