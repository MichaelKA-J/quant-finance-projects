import numpy as np
from statsmodels.tsa.stattools import acovf


ma_shocks = np.random.poisson(lam=5, size=1000)

ma_shocks_lag1 = np.zeros(1000)
ma_shocks_lag1[1:] = ma_shocks[:-1]

ma_shocks_lag2 = np.zeros(1000)
ma_shocks_lag2[2:] = ma_shocks[:-2]

ma_mu = 5
ma_theta1 = 1.5
ma_theta2 = 2.0

ma_series = (
    ma_mu
    + ma_shocks
    + ma_theta1 * ma_shocks_lag1
    + ma_theta2 * ma_shocks_lag2
)

ma_last_quarter = ma_series[750:]
ma_last_mean = np.mean(ma_last_quarter)
ma_last_var = np.var(ma_last_quarter, ddof=1)
ma_last_acov = acovf(ma_last_quarter, nlag=3, adjusted=True)

ma_prev_quarter = ma_series[500:750]
ma_prev_mean = np.mean(ma_prev_quarter)
ma_prev_var = np.var(ma_prev_quarter, ddof=1)
ma_prev_acov = acovf(ma_prev_quarter, nlag=3, adjusted=True)


ar_shocks = np.random.normal(0, np.sqrt(2), 1000)

ar_const = 2
ar_phi1 = 0.5
ar_phi2 = 0.2

ar_series = np.zeros(1000)

ar_series[0] = ar_const + ar_shocks[0]
ar_series[1] = ar_const + ar_phi1 * ar_series[0] + ar_shocks[1]

for t in range(2, 1000):
    ar_series[t] = (
        ar_const
        + ar_phi1 * ar_series[t - 1]
        + ar_phi2 * ar_series[t - 2]
        + ar_shocks[t]
    )

ar_last_quarter = ar_series[750:]
ar_last_mean = np.mean(ar_last_quarter)
ar_last_var = np.var(ar_last_quarter, ddof=1)
ar_last_acov = acovf(ar_last_quarter, nlag=2, adjusted=True)

ar_prev_quarter = ar_series[500:750]
ar_prev_mean = np.mean(ar_prev_quarter)
ar_prev_var = np.var(ar_prev_quarter, ddof=1)
ar_prev_acov = acovf(ar_prev_quarter, nlag=2, adjusted=True)
