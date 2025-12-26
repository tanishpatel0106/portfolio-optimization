from __future__ import annotations

import numpy as np
import pandas as pd
from scipy.stats import norm


def compute_returns(prices: pd.Series) -> pd.Series:
    return prices.pct_change().dropna()


def performance_summary(returns: pd.Series) -> dict:
    cumulative = (1 + returns).prod() - 1
    cagr = (1 + cumulative) ** (252 / len(returns)) - 1 if len(returns) > 0 else 0.0
    vol = returns.std() * np.sqrt(252)
    sharpe = returns.mean() / returns.std() * np.sqrt(252) if returns.std() != 0 else 0.0
    drawdown = (1 + returns).cumprod().cummax() - (1 + returns).cumprod()
    max_dd = drawdown.max() if not drawdown.empty else 0.0
    return {
        "cumulative_return": cumulative,
        "cagr": cagr,
        "annualized_vol": vol,
        "sharpe": sharpe,
        "max_drawdown": max_dd,
    }


def var_cvar(returns: pd.Series, alpha: float = 0.05) -> dict:
    hist_var = returns.quantile(alpha)
    hist_cvar = returns[returns <= hist_var].mean()
    mu = returns.mean()
    sigma = returns.std()
    param_var = norm.ppf(alpha, mu, sigma)
    param_cvar = mu - sigma * norm.pdf(norm.ppf(alpha)) / alpha
    return {
        "hist_var": float(hist_var),
        "hist_cvar": float(hist_cvar),
        "param_var": float(param_var),
        "param_cvar": float(param_cvar),
    }


def risk_contributions(weights: np.ndarray, cov: np.ndarray) -> np.ndarray:
    port_var = weights.T @ cov @ weights
    mrc = cov @ weights
    rc = weights * mrc / port_var if port_var != 0 else np.zeros_like(weights)
    return rc
