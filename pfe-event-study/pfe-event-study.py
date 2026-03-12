### CAPM Regressions

import statsmodels.api as sm
import pandas as pd

Data = pd.read_excel(
    '/Users/michael/Desktop/Moderna_Pfizer Event Study.xlsx',
    index_col='Date')

Data = Data.rename(columns={'Mkt-RF':'Mkt_RF'}) 
Data['Mkt_Excess_Dec'] = Data['Mkt_RF'] / 100
Data['RF_Dec'] = Data['RF'] / 100
Data['PFE_Excess_Dec'] = Data['PFE_Dec'] - Data['RF_Dec']

PFE_estimation_window = Data['2019-01-01':'2020-12-03']
PFE_CAPM_model = sm.formula.ols(
    formula = 'PFE_Excess_Dec ~ Mkt_Excess_Dec', 
    data = PFE_estimation_window)
PFE_CAPM_results = PFE_CAPM_model.fit()
print(PFE_CAPM_results.summary())



### Abnormal Returns

PFE_first20 = Data['2020-12-04':'2021-01-04'].copy() 
alpha_hat_PFE = PFE_CAPM_results.params['Intercept']
beta_hat_PFE = PFE_CAPM_results.params['Mkt_Excess_Dec']
PFE_first20['PFE_R_Hat'] = (
    alpha_hat_PFE + beta_hat_PFE * PFE_first20['Mkt_Excess_Dec']
    )
PFE_first20['PFE_AR'] = (
    PFE_first20['PFE_Excess_Dec'] - PFE_first20['PFE_R_Hat']
    )
print(PFE_first20.PFE_AR.head())



### Cumulative Abnormal Returns

PFE_all_cars = PFE_first20['PFE_AR'].cumsum()
T = [5, 10, 15, 20]
CARs = pd.DataFrame({
    'T': T,
    'PFE CAR': PFE_all_cars.iloc[[4,9,14,19]].values,
    })
print(CARs)
