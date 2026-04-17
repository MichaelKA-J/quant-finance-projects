import numpy as np
from scipy.stats import norm

def bsm_call(S0, q, X, r, T, σ):
    r"""
    Compute the corresponding option price using put-call parity.

    Parameters
    ----------
    prem : float
        Known option premium (call or put).
    S0 : float
        Current price of the underlying asset.
    q : float
        Continuous dividend yield (annualized, decimal form).
    X : float
        Strike price of the option.
    r : float
        Continuously compounded risk-free interest rate (annualized, decimal form).
    T : float
        Time to maturity in years.
    call : int, optional
        Indicator for the type of known premium:
        - 1: prem is a call price, return the corresponding put price
        - 0: prem is a put price, return the corresponding call price

    Returns
    -------
    float
        Corresponding option price (put if call is given, call if put is given).

    Raises
    ------
    ValueError
        If `call` is not 0 or 1.

    Notes
    -----
    Put-call parity relationship:

        C0 - P0 = S0 * exp(-qT) - X * exp(-rT)

    Rearranged:
        P0 = C0 - (S0 * exp(-qT) - X * exp(-rT))
        C0 = P0 + (S0 * exp(-qT) - X * exp(-rT))
    """
    
    # compute call price
    d1 = (np.log(S0/X) + (r - q + ((σ**2)/2))*T) / (σ*(T**0.5))
    d2 = d1 - σ*(T**0.5)
    C0 = S0*np.exp(-q*T)*norm.cdf(d1) - X*np.exp(-r*T)*norm.cdf(d2)
    return C0

def put_call_parity(prem, S0, q, X, r, T, call=1):
    r"""
    

    Parameters
    ----------
    prem : TYPE
        DESCRIPTION.
    S0 : TYPE
        DESCRIPTION.
    q : TYPE
        DESCRIPTION.
    X : TYPE
        DESCRIPTION.
    r : TYPE
        DESCRIPTION.
    T : TYPE
        DESCRIPTION.
    call : TYPE, optional
        DESCRIPTION. The default is 1.

    Raises
    ------
    ValueError
        DESCRIPTION.

    Returns
    -------
    TYPE
        DESCRIPTION.

    """
    
    if call == 1:  
        P0 = prem - (S0*np.exp(-q*T) - X*np.exp(-r*T))
        return P0
    elif call == 0:  
        C0 = prem + (S0*np.exp(-q*T) - X*np.exp(-r*T))
        return C0
    else:
        raise ValueError("Call indicator must be 1 or 0!")

call_a = bsm_call(S0=205, q=0, X=212, σ=0.35, r=0.005, T=1)
call_b = bsm_call(S0=205, q=0, X=212, σ=0.80, r=0.005, T=1)
call_c = bsm_call(S0=205, q=0, X=207, σ=0.35, r=0.005, T=1)
print(call_a, "\n", call_b, "\n", call_c, "\n")


put_a = put_call_parity(call_a, S0=205, q=0, X=212, σ=0.35, r=0.005, T=1)
put_b = put_call_parity(call_b, S0=205, q=0, X=212, σ=0.80, r=0.005, T=1)
put_c = put_call_parity(call_c, S0=205, q=0, X=207, σ=0.35, r=0.005, T=1)
print(put_a, "\n", put_b, "\n", put_c)
