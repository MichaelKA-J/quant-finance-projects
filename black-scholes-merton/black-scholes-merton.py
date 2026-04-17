# Black-Scholes-Merton (BSM) European option pricing model 
# put price is derived from call price using put-cal parity

import numpy as np
from scipy.stats import norm

def bsm(S0, q, X, r, T, σ, call=1):
    r"""
    Compute the Black–Scholes–Merton (BSM) price of a European option.

    Parameters
    ----------
    S0 : float
        Current price of the underlying asset.
    q : float
        Continuous dividend yield (annualized, in decimal form).
    X : float
        Strike price of the option.
    r : float
        Continuously compounded risk-free interest rate 
        (annualized, in decimal form).
    T : float
        Time to maturity in years.
    σ : float
        Volatility of the underlying asset 
        (annualized standard deviation of log returns).
    call : int, optional
        Option type indicator:
        - 1: return call option price
        - 0: return put option price
        Default is 1.

    Returns
    -------
    float
        Price of the European option (call or put).

    Raises
    ------
    ValueError
        If `call` is not 0 or 1.

    Notes
    -----
    The Black–Scholes–Merton call price is given by:

        C0 = S0 * exp(-qT) * N(d1) - X * exp(-rT) * N(d2)

    where:

        d1 = [ln(S0/X) + (r - q + 0.5σ^2)T] / (σ√T)
        d2 = d1 - σ√T

    The put price is obtained using put-call parity:

        P0 = C0 - (S0 * exp(-qT) - X * exp(-rT))

    This implementation assumes:
    - European-style options (no early exercise)
    - Constant volatility and interest rates
    - Lognormal price dynamics
    """
    
    d1 = (np.log(S0/X) + (r - q + 0.5*σ**2)*T) / (σ*np.sqrt(T))
    d2 = d1 - σ*np.sqrt(T)
    
    C0 = S0*np.exp(-q*T)*norm.cdf(d1) - X*np.exp(-r*T)*norm.cdf(d2)
    
    if call == 1:
        return C0
    elif call == 0:
        P0 = C0 - (S0*np.exp(-q*T) - X*np.exp(-r*T))
        return P0
    else:
        raise ValueError("Call indicator must be 1 or 0!")
