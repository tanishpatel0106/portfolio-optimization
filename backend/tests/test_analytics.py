import numpy as np
import pandas as pd

from app.services import analytics


def test_returns_and_var():
    prices = pd.Series([100, 102, 101, 103])
    returns = analytics.compute_returns(prices)
    summary = analytics.performance_summary(returns)
    var = analytics.var_cvar(returns)
    assert "cumulative_return" in summary
    assert var["hist_var"] <= 0.05


def test_risk_contributions():
    weights = np.array([0.6, 0.4])
    cov = np.array([[0.04, 0.01], [0.01, 0.09]])
    rc = analytics.risk_contributions(weights, cov)
    assert np.isclose(rc.sum(), 1.0)
