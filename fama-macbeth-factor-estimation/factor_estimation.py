import numpy as np
import pandas as pd
import statsmodels.api as sm

df = pd.read_excel('Fama_MacBeth.xlsx')

excess_df = df.iloc[:, 1:26].sub(df['RF'], axis=0)
factors = df.iloc[:, [26, 28, 29]]

# Stage 1 (Time-series regressions to estimate betas)
X_ts = sm.add_constant(factors)

betas = []

for portfolio in excess_df.columns:
    model = sm.OLS(excess_df[portfolio], X_ts).fit()
    betas.append(model.params.iloc[1:].values)   # exclude alpha

betas = np.array(betas)                  



# Stage 2 (Cross-sectional regression each period)
X_cs = sm.add_constant(betas)                 
lambdas = []

for t in range(len(excess_df)):
    y_t = excess_df.iloc[t].values

    model = sm.OLS(y_t, X_cs).fit()
    lambdas.append(model.params)

lambdas = np.array(lambdas)



# Fama-MacBeth estimates
lambda_hat = lambdas.mean(axis=0)

# Fama-MacBeth standard errors
fm_se = lambdas.std(axis=0, ddof=1) / np.sqrt(len(lambdas))

t_stats = lambda_hat / fm_se

results = pd.DataFrame({
    'Estimate': lambda_hat,
    'Std Error': fm_se,
    't-stat': t_stats
}, index=['Intercept', 'Mkt-RF', 'SMB', 'HML'])

print(results)
