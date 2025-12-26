from __future__ import annotations

from statistics import NormalDist

import numpy as np
import pandas as pd


def compute_returns(prices: pd.Series) -> pd.Series:
    return prices.pct_change().dropna()


def historical_var_cvar(returns: pd.Series, level: float = 0.95) -> tuple[float, float]:
    if returns.empty:
        return 0.0, 0.0
    threshold = returns.quantile(1 - level)
    cvar = returns[returns <= threshold].mean()
    return float(threshold), float(cvar)


def parametric_var_cvar(returns: pd.Series, level: float = 0.95) -> tuple[float, float]:
    if returns.empty:
        return 0.0, 0.0
    mean = returns.mean()
    std = returns.std(ddof=0)
    z = abs(NormalDist().inv_cdf(1 - level))
    var = mean - z * std
    cvar = mean - std * (NormalDist().pdf(-z) / (1 - level))
    return float(var), float(cvar)


def risk_contributions(weights: np.ndarray, cov: np.ndarray) -> np.ndarray:
    portfolio_var = float(weights.T @ cov @ weights)
    if portfolio_var == 0:
        return np.zeros_like(weights)
    marginal = cov @ weights
    contributions = weights * marginal / portfolio_var
    return contributions
