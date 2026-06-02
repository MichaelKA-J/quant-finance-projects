# Natural Gas Price Forecasting & Statistical Backtesting

## Project Overview
Quantitative research project completed for the JPMorgan Chase & Co. Quantitative Research Virtual Experience on Forage. The objective was to analyze historical natural gas prices, establish a baseline benchmark, and construct an out-of-sample forecasting model capturing seasonality and market trends.

---

## Methodology

### 1. Data Processing
* Checked historical monthly natural gas price data for null and non-positive values.
* Identified cyclicality and winter demand peaks via time-series visualization.

### 2. Baseline Benchmark
* Selected a **Seasonal Naïve with Drift** benchmark instead of a standard Random Walk.
* Mapped forecasts to the same month from the prior year while accounting for an upward macro trend.

### 3. Model Evaluation & Constraints
* **SARIMA:** Evaluated $SARIMA(1,1,1) \times (1,1,1)_{12}$ but rejected it due to small sample size (48 observations) exploding MLE p-values.
* **Exponential Smoothing:** Implemented a Holt-Winters (ETS) model with additive trend and seasonal components for stable performance on short time series.

### 4. Statistical Backtesting
* Backtested models out-of-sample on a 12-month forward horizon.
* Tested predictive accuracy using the Harvey-Leybourne-Newbold (HLN) small-sample modification of the Diebold-Mariano test:
  $$HLN = DM \times \sqrt{\frac{T + 1 - 2h + \frac{h(h-1)}{T}}{T}}$$
* Confirmed statistically significant outperformance of the ETS model over the baseline.

---

## Key Results
* **Outperformance:** ETS framework successfully minimized forecast error relative to the drift-adjusted seasonal baseline.
* **Visualizations:** Generated `matplotlib` charts comparing training data, actual outcomes, and dual-model projection paths.
* **Next Steps:** Plan to validate model predictions against market expectations from the forward curve.
