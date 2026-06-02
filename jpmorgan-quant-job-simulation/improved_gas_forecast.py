#%% import libaries
import pandas as pd
import matplotlib.pyplot as plt 
import numpy as np
from sktime.forecasting.exp_smoothing import ExponentialSmoothing
from scipy.stats import t
import os
os.chdir("/Users/michael/Documents/jpm_qr_sim")



#%% data cleaning
df = pd.read_csv("Nat_Gas.csv")
df["Dates"] = pd.to_datetime(df["Dates"])
df.set_index('Dates', inplace=True)
df.isnull().values.any() # check for NAs
# df = df.dropna()
(df.Prices <= 0).any() # check for zeros and negatives
# df = df.loc[(df != 0).all(axis=1)]



#%% initial data visualization
plt.figure(figsize=(10, 6))
plt.plot(df.index.to_timestamp(), df.Prices, color='steelblue', linewidth=1.5)
plt.title('Natural Gas Prices (Historical Data)')
plt.xlabel('Date')
plt.ylabel('Price')
plt.grid(True, alpha=0.3)
plt.autoscale(enable=True, axis='x', tight=True)
plt.tight_layout()
plt.show() # fairly obvious seasonal trends



#%% forecast model brainstorming
'''
hln test (small-sample modified dm test)
- the small sample version of the dm test
- makes a bias correction to the original dm test stat
- imposes student t distr. for the test stat
- a + dm test stat suggests B outperforms A since it means the 
loss differentials (A - B) are + on avg. 
naïve benchmark: seasonal naïve with draft
- Data clearly trends upwards, so impose a model similar to RW+drift 
- Seasonality is strong enough to use Seasonal Naïve instead of monthly RW
- Seasonal Naïve: next month's price is the same as that month last year
- Beating a plain RW or even plain RW+drift is too easy
exponential smoothing
- ES is one of the best models for small samples
SARIMA
- SARIMA is a famous benchmark model for seasonal, trended data
- However, SARIMA requires a large sample size for MLE to be effective
- In this case, the 48 obs. were not enough, p-values exploded
order = (1, 1, 1)
seasonal_order = (1, 1, 1, 12) # 1 cycle of the pattern takes 12 months
model = SARIMAX(df.Prices, order=order, seasonal_order=seasonal_order) 
# NOTE: a 1D Pandas Series with a DatetimeIndex works best for SARIMAX 
results = model.fit()
print(results.summary())
'''  



#%% training and backtesting
# create training window
df.index = df.index.to_period('M')
y_train = df['Prices'].iloc[:-12]
y_test = df['Prices'].iloc[-12:]

# train 
def seasonal_naive_with_drift(series, h=12, sp=12):
    n = len(series)
    drift = (series.iloc[-1] - series.iloc[0]) / (n - 1)
    forecasts = [series.iloc[-sp + ((i - 1) % sp)] + (drift * i) for i in range(1, h + 1)]
    return pd.Series(forecasts, index=y_test.index)

es = ExponentialSmoothing(trend="add", seasonal="add", sp=12)
es.fit(y_train)

# forecast
y_pred = seasonal_naive_with_drift(y_train, h=12)
p_es = es.predict(fh=list(range(1, 13)))

# test 
def hln_test(actual, p_bench, p_model, h=1):
    T = len(actual)
    d = np.abs(actual - p_bench) - np.abs(actual - p_model)
    mean_d = np.mean(d)
    std_d = np.std(d, ddof=1)
    
    if std_d == 0: return 0.0, 1.0
    
    dm_stat = mean_d / (std_d / np.sqrt(T))
    correction = np.sqrt((T + 1 - 2*h + (h/T)*(h-1)) / T)
    hln_stat = dm_stat * correction
    p_value = 2 * (1 - t.cdf(np.abs(hln_stat), df=T-1))
    
    return hln_stat, p_value

stat, pval = hln_test(y_test.values, y_pred.values, p_es.values)

print(f"HLN Statistic: {stat:.4f}")
print(f"P-value: {pval:.4f}")

# visualize forecast performance
plt.figure(figsize=(10, 6))
plt.plot(
    y_train.index.to_timestamp(), 
    y_train, 
    label='Train', 
    color='gray', 
    alpha=0.5
    )
plt.plot(
    y_test.index.to_timestamp(), 
    y_test, 
    label='Actual', 
    color='black', 
    linewidth=2
    )
plt.plot(
    y_pred.index.to_timestamp(), 
    y_pred, 
    label='Seasonal Naive + Drift', 
    linestyle='--'
    )
plt.plot(
    p_es.index.to_timestamp(), 
    p_es, 
    label='Exp. Smoothing', 
    linestyle='--'
    )

plt.title('Natural Gas Price Forecast Comparison')
plt.xlabel('Date')
plt.ylabel('Price')
plt.legend()
plt.grid(True, alpha=0.3)
plt.tight_layout()
plt.show()



#%% console commands
"""
df.Date
print(df.columns)
"""


#%% lessons
'''
- first, visualize the data carefully before proposing models
- always ask, does this model (or statistical test) work at my sample size
- find a naive benchmark for testing an alternative forecasting model against
- you can enhance the naive benchmark to be more rigourous ie seasonal naive
- natural gas and many other commodities see prices spike in the cold months
- don't be allergic to AI
- acquire--> clean--> visualize--> brainstorm--> test--> execute
'''
