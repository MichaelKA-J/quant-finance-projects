# AR and MA Time Series Simulation

This project simulates moving-average and autoregressive time series processes in Python and compares their sample properties across subsamples.

## Objective

The goal is to build intuition for how common stationary time series models behave in finite samples.

The project simulates:

- An **MA(2)** process
- An **AR(2)** process

and compares their sample moments over different portions of the simulated series.

## Models

### Moving-Average Process (MA(2))
$$Y_t = \mu + \epsilon_t + \theta_1 \epsilon_{t-1} + \theta_2 \epsilon_{t-2}$$

### Autoregressive Process (AR(2))
$$Y_t = c + \phi_1 Y_{t-1} + \phi_2 Y_{t-2} + \epsilon_t$$

## Method

### For the MA(2) simulation:
1. Generate error terms
2. Construct the **MA(2)** series using two lagged shocks
3. Extract different subsamples of the simulated series
4. Compute:
   - **Sample mean**
   - **Sample variance**
   - **Sample autocovariances**

### For the AR(2) simulation:
1. Generate **Gaussian shocks**
2. Initialize the first observations
3. Recursively simulate the **AR(2)** process
4. Extract different subsamples of the simulated series
5. Compute:
   - **Sample mean**
   - **Sample variance**
   - **Sample autocovariances**

## Output

The script reports sample statistics for different subsamples of each process, including:

- **Mean**
- **Variance**
- **Autocovariances** at several lags

This helps illustrate how finite-sample estimates can vary across time even when the underlying model is fixed.

## Tools

- **Python**
- **NumPy**
- **statsmodels**

## Skills Demonstrated

- Simulation of **MA and AR processes**
- Construction of **lagged variables**
- **Recursive** time series generation
- Comparison of **finite-sample moments**
- Use of **autocovariance functions** in Python
