# Pfizer (PFE) Event Study: CAPM and Cumulative Abnormal Returns

This project implements a standard Financial Event Study to analyze the Abnormal Returns (AR) and Cumulative Abnormal Returns (CAR) of Pfizer stock ($PFE$) relative to market benchmarks using the Capital Asset Pricing Model (CAPM).

---

## Methodology

### 1. CAPM Regression (Estimation Window)
The model establishes a baseline for Pfizer's performance using an estimation window from **2019-01-01** to **2020-12-03**. The relationship between Pfizer's excess returns and market excess returns is defined by the CAPM formula:

$$R_{i,t} - R_{f,t} = \alpha_i + \beta_i(R_{m,t} - R_{f,t}) + \epsilon_{i,t}$$

*   **Intercept ($\alpha$):** Represents the risk-adjusted excess return.
*   **Beta ($\beta$):** Measures the stock's sensitivity to market movements.

### 2. Abnormal Returns (Event Window)
Abnormal Returns are calculated for the period **2020-12-04** to **2021-01-04**. The $AR$ is the difference between the actual observed return and the return predicted by the CAPM model:

$$AR_{i,t} = R_{actual,t} - (\hat{\alpha}_i + \hat{\beta}_i(R_{m,t} - R_{f,t}))$$

### 3. Cumulative Abnormal Returns (CAR)
The $CAR$ aggregates the abnormal returns over specific time horizons ($T = 5, 10, 15, 20$ days) to measure the total impact of the event over the specified window.
