from fastapi import FastAPI
from pydantic import BaseModel
import numpy as np
from scipy.stats import norm
from typing import Dict

app = FastAPI()

class OptionParams(BaseModel):
    S: float  # Spot price
    K: float  # Strike price
    T: float  # Time to expiration (years)
    r: float  # Risk-free rate (0.05 = 5%)
    sigma: float  # Volatility (0.2 = 20%)

def black_scholes(params: OptionParams):
    S, K, T, r, sigma = params.S, params.K, params.T, params.r, params.sigma
    
    # Avoid division by zero
    if T <= 0 or sigma <= 0:
        return {"call": max(0, S - K), "put": max(0, K - S), "delta": 1.0 if S > K else 0.0, "gamma": 0, "theta": 0, "vega": 0}

    d1 = (np.log(S / K) + (r + 0.5 * sigma**2) * T) / (sigma * np.sqrt(T))
    d2 = d1 - sigma * np.sqrt(T)
    
    # Prices
    call_price = S * norm.cdf(d1) - K * np.exp(-r * T) * norm.cdf(d2)
    put_price = K * np.exp(-r * T) * norm.cdf(-d2) - S * norm.cdf(-d1)
    
    # Greeks
    # Delta: dC/dS
    delta_call = norm.cdf(d1)
    delta_put = delta_call - 1
    
    # Gamma: d^2C/dS^2
    gamma = norm.pdf(d1) / (S * sigma * np.sqrt(T))
    
    # Vega: dC/dsigma
    vega = S * norm.pdf(d1) * np.sqrt(T)
    
    # Theta: dC/dt (annualized)
    theta_call = (- (S * norm.pdf(d1) * sigma) / (2 * np.sqrt(T)) - r * K * np.exp(-r * T) * norm.cdf(d2))
    theta_put = (- (S * norm.pdf(d1) * sigma) / (2 * np.sqrt(T)) + r * K * np.exp(-r * T) * norm.cdf(-d2))

    return {
        "call": float(call_price),
        "put": float(put_price),
        "delta": float(delta_call),
        "gamma": float(gamma),
        "theta": float(theta_call / 365), # Daily theta
        "vega": float(vega / 100),        # Vega for 1% vol change
    }

@app.post("/calculate")
async def calculate_option(params: OptionParams):
    return black_scholes(params)

@app.get("/plot")
async def get_plot_data(S: float, K: float, T: float, r: float, sigma: float):
    # Generate a range of spot prices for visualization
    s_range = np.linspace(S * 0.5, S * 1.5, 50)
    results = []
    for s in s_range:
        p = OptionParams(S=s, K=K, T=T, r=r, sigma=sigma)
        res = black_scholes(p)
        res['S'] = s
        results.append(res)
    return results

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
