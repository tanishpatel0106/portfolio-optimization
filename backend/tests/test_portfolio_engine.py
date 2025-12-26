import pandas as pd
import pytest

from app.services import portfolio_engine


def test_base_currency_detection():
    positions = pd.DataFrame({"AAA": [10], "BBB": [5]}, index=[pd.Timestamp("2024-01-02")])
    prices = pd.DataFrame({"AAA": [100], "BBB": [200]}, index=positions.index)
    currency_map = {"AAA": "USD", "BBB": "EUR"}
    fx_to_usd = {"EUR": pd.Series([1.1], index=positions.index)}
    result = portfolio_engine.detect_base_currency(
        positions, prices, currency_map, fx_to_usd, locked_currency=None
    )
    assert result.base_currency == "USD"
    assert 0 < result.share <= 1


def test_fx_matrix_triangulation():
    dates = pd.date_range("2024-01-01", periods=2)
    fx_rates = {
        "EURUSD=X": pd.Series([1.1, 1.2], index=dates),
        "USDJPY=X": pd.Series([150, 151], index=dates),
    }
    currency_map = {"AAA": "EUR"}
    fx_matrix = portfolio_engine.build_fx_matrix(["AAA"], currency_map, "JPY", fx_rates)
    assert fx_matrix["AAA"].iloc[0] == pytest.approx(1.1 * 150)


def test_synthetic_ohlcv():
    dates = pd.date_range("2024-01-01", periods=2)
    positions = pd.DataFrame({"AAA": [1, 1]}, index=dates)
    ohlcv = {
        "AAA": pd.DataFrame(
            {
                "Open": [100, 101],
                "High": [105, 106],
                "Low": [95, 96],
                "Close": [102, 103],
                "Volume": [1000, 1100],
            },
            index=dates,
        )
    }
    fx_matrix = pd.DataFrame({"AAA": [1, 1]}, index=dates)
    portfolio = portfolio_engine.synthesize_portfolio_ohlcv(positions, ohlcv, fx_matrix)
    assert portfolio["Close"].iloc[-1] == 103


def test_position_change_classification():
    dates = pd.date_range("2024-01-01", periods=3)
    positions = pd.DataFrame({"AAA": [0, 1, -1]}, index=dates)
    changes = portfolio_engine.classify_position_changes(positions)
    actions = changes["action"].tolist()
    assert "Opened new position" in actions
    assert "Flip" in actions
