import numpy as np
import statsmodels.api as sm


def simulate_df_stat():

    shocks = np.random.normal(0.0, 1.0, size=(225, 1))
    drift = 0.25

    series = np.zeros((225, 1))
    series[0] = 0

    for t in range(1, 225):
        series[t] = drift + series[t-1] + shocks[t]

    sample = series[150:225]

    y_t = sample[1:75]
    y_lag = sample[0:74]
    delta_y = y_t - y_lag

    X = sm.add_constant(y_lag)

    model = sm.OLS(delta_y, X)
    results = model.fit()

    df_t_stat = results.params[1] / results.bse[1]

    return df_t_stat


df_statistics = np.zeros((10000, 1))

for i in range(10000):
    df_statistics[i] = simulate_df_stat()

print("5th percentile:", np.percentile(df_statistics, 5))
print("Mean DF statistic:", np.mean(df_statistics))
