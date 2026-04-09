import statsmodels.api as sm; import numpy as np; import pandas as pd

import os
os.chdir('/Users/michael/Documents/ECON 525/Problem Set 3')

df = pd.read_excel('Fama_MacBeth.xlsx', index_col = 'Date')

rf_df = pd.concat([df.RF] * 25, axis = 1) 
excess_df = df.iloc[:, 0:25] - rf_df.iloc[:, 0:25].values 
X = sm.add_constant(df[['Mkt-RF', 'CPIAUCSL_PCH', 'PCE_PCH']]) 

betas_df = pd.DataFrame()
for i in range(25):
    mod_first_stage = sm.OLS(excess_df.iloc[:, i], X).fit()
    betas_df[i + 1] = mod_first_stage.params.iloc[1:4] 
betas_df = sm.add_constant(betas_df.T)

r_bar = np.mean(df.iloc[:, 0:25], axis = 0) 

mod_second_stage = sm.OLS(r_bar.values, betas_df).fit()
print(mod_second_stage.summary())
