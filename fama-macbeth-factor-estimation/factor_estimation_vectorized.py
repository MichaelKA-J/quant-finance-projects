import statsmodels.api as sm; import numpy as np; import pandas as pd
from sklearn.linear_model import LinearRegression as lr

df = pd.read_excel('Fama_MacBeth.xlsx')
excess_df = df.iloc[:, 1:26].sub(df.RF, axis = 0)

# 1st stage
betas = sm.add_constant(lr().fit(df.iloc[:, [26, 28, 29]], excess_df).coef_)

# 2nd stage
sm.OLS(np.mean(df.iloc[:, 1:26], axis = 0).values, betas).fit().summary()
