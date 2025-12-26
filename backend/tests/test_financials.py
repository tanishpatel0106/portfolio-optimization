import numpy as np
import pandas as pd

from app.services import analytics, portfolio_engine


def test_base_currency_detection_prefers_highest_share():
    positions = pd.DataFrame(
        {
            "ticker": ["AAA", "BBB"],
            "quantity": [10, 5],
            "price": [100, 200],
            "currency": ["EUR", "JPY"],
        }
    )
    positions["market_value"] = positions["quantity"] * positions["price"]
    fx_rates = {"EUR": 1.2, "JPY": 0.009}
    result = portfolio_engine.detect_base_currency(positions, fx_rates)
    assert result.base_currency == "EUR"
    assert result.share > 0.5


def test_fx_triangulation():
    dates = pd.date_range("2024-01-01", periods=3, freq="D")
    fx_pairs = {
        "EURUSD=X": pd.Series([1.1, 1.2, 1.3], index=dates),
        "USDJPY=X": pd.Series([100, 101, 102], index=dates),
    }
    series = portfolio_engine.resolve_fx_series("EUR", "JPY", fx_pairs)
    expected = fx_pairs["EURUSD=X"] * fx_pairs["USDJPY=X"]
    pd.testing.assert_series_equal(series, expected)


def test_portfolio_ohlcv_construction():
    dates = pd.date_range("2024-01-01", periods=2, freq="D")
    ohlcv = {
        "AAA": pd.DataFrame(
            {
                "open": [10, 11],
                "high": [12, 13],
                "low": [9, 10],
                "close": [11, 12],
                "volume": [100, 110],
            },
            index=dates,
        )
    }
    fx_series = {"AAA": pd.Series([1.0, 1.0], index=dates)}
    positions = pd.DataFrame({"ticker": ["AAA"], "quantity": [2]})
    portfolio = portfolio_engine.build_portfolio_ohlcv(positions, ohlcv, fx_series)
    assert portfolio.loc[dates[0], "close"] == 22
    assert portfolio.loc[dates[1], "volume"] == 220


def test_returns_var_cvar():
    prices = pd.Series([100, 105, 103, 106])
    returns = analytics.compute_returns(prices)
    var_hist, cvar_hist = analytics.historical_var_cvar(returns, level=0.95)
    var_param, cvar_param = analytics.parametric_var_cvar(returns, level=0.95)
    assert isinstance(var_hist, float)
    assert isinstance(cvar_hist, float)
    assert isinstance(var_param, float)
    assert isinstance(cvar_param, float)


def test_risk_contributions_sum_to_one():
    weights = np.array([0.6, 0.4])
    cov = np.array([[0.04, 0.01], [0.01, 0.09]])
    contributions = analytics.risk_contributions(weights, cov)
    assert np.isclose(contributions.sum(), 1.0)


def test_position_change_classification():
    history = pd.DataFrame(
        {
            "date": ["2024-01-01", "2024-01-02", "2024-01-03"],
            "ticker": ["AAA", "AAA", "AAA"],
            "quantity": [0, 10, 5],
            "price": [10, 11, 12],
        }
    )
    changes = portfolio_engine.classify_position_changes(history)
    actions = changes["action"].tolist()
    assert "Opened" in actions
    assert "Reduced long" in actions
