from __future__ import annotations

from dataclasses import dataclass
from datetime import date
from typing import Iterable

import numpy as np
import pandas as pd


@dataclass
class FXResult:
    base_currency: str
    share: float
    fallback_reason: str | None = None


def compute_positions_from_weights(weights: pd.DataFrame, prices: pd.DataFrame) -> pd.Series:
    aligned = weights.reindex(prices.index).fillna(method="ffill").fillna(0)
    returns = prices.pct_change().fillna(0)
    portfolio_value = (aligned.shift().fillna(aligned.iloc[0]) * (1 + returns)).sum(axis=1)
    positions_value = aligned.mul(portfolio_value, axis=0)
    quantity = positions_value / prices
    return quantity


def compute_positions_from_trades(trades: pd.DataFrame, prices: pd.DataFrame) -> pd.DataFrame:
    trades = trades.sort_values("trade_date")
    trades_by_ticker = trades.groupby("ticker")
    positions = pd.DataFrame(index=prices.index, columns=prices.columns, data=0.0)
    for ticker, group in trades_by_ticker:
        series = pd.Series(index=prices.index, data=0.0)
        for _, row in group.iterrows():
            series.loc[series.index >= row["trade_date"]] += row["quantity"]
        positions[ticker] = series
    return positions


def detect_base_currency(
    positions: pd.DataFrame,
    prices: pd.DataFrame,
    currency_map: dict[str, str],
    fx_to_usd: dict[str, pd.Series],
    locked_currency: str | None = None,
) -> FXResult:
    asof_prices = prices.iloc[-1]
    quantities = positions.iloc[-1]
    mv_local = quantities * asof_prices
    totals: dict[str, float] = {}
    for ticker, mv in mv_local.items():
        currency = currency_map.get(ticker, "USD")
        fx_series = fx_to_usd.get(currency)
        if fx_series is None and currency != "USD":
            continue
        fx_rate = 1.0 if currency == "USD" else fx_series.iloc[-1]
        totals[currency] = totals.get(currency, 0.0) + mv * fx_rate
    total_value = sum(totals.values())
    if total_value <= 0:
        fallback = locked_currency or "USD"
        return FXResult(base_currency=fallback, share=1.0, fallback_reason="no_market_value")
    base_currency = max(totals, key=totals.get)
    share = totals[base_currency] / total_value
    if not totals and locked_currency:
        return FXResult(base_currency=locked_currency, share=1.0, fallback_reason="locked_currency")
    if not totals:
        return FXResult(base_currency="USD", share=1.0, fallback_reason="fallback_usd")
    return FXResult(base_currency=base_currency, share=share)


def build_fx_matrix(
    tickers: Iterable[str],
    currency_map: dict[str, str],
    base_currency: str,
    fx_rates: dict[str, pd.Series],
) -> pd.DataFrame:
    index = next(iter(fx_rates.values())).index if fx_rates else None
    fx_matrix = pd.DataFrame(index=index, columns=list(tickers), data=1.0)
    for ticker in tickers:
        currency = currency_map.get(ticker, base_currency)
        if currency == base_currency:
            fx_matrix[ticker] = 1.0
            continue
        direct_pair = f"{currency}{base_currency}=X"
        if direct_pair in fx_rates:
            fx_matrix[ticker] = fx_rates[direct_pair]
            continue
        if currency != "USD" and base_currency != "USD":
            to_usd = fx_rates.get(f"{currency}USD=X")
            usd_to_base = fx_rates.get(f"USD{base_currency}=X")
            if to_usd is not None and usd_to_base is not None:
                fx_matrix[ticker] = to_usd * usd_to_base
                continue
        fx_matrix[ticker] = np.nan
    return fx_matrix


def synthesize_portfolio_ohlcv(
    positions: pd.DataFrame,
    ohlcv: dict[str, pd.DataFrame],
    fx_matrix: pd.DataFrame,
) -> pd.DataFrame:
    columns = ["Open", "High", "Low", "Close", "Volume"]
    index = positions.index
    portfolio = pd.DataFrame(index=index, columns=columns, data=0.0)
    for ticker, qty in positions.items():
        frame = ohlcv.get(ticker)
        if frame is None:
            continue
        aligned = frame.reindex(index).fillna(method="ffill")
        fx = fx_matrix[ticker].reindex(index).fillna(method="ffill")
        portfolio["Open"] += qty * aligned["Open"] * fx
        portfolio["High"] += qty * aligned["High"] * fx
        portfolio["Low"] += qty * aligned["Low"] * fx
        portfolio["Close"] += qty * aligned["Close"] * fx
        portfolio["Volume"] += qty.abs() * aligned["Volume"].fillna(0)
    return portfolio


def classify_position_changes(positions: pd.DataFrame) -> pd.DataFrame:
    changes = []
    tickers = positions.columns
    for ticker in tickers:
        series = positions[ticker]
        prev = series.shift(1).fillna(0)
        delta = series - prev
        for dt, q_prev, q_now, d in zip(series.index, prev, series, delta):
            action = None
            if q_prev == 0 and q_now != 0:
                action = "Opened new position"
            elif q_prev != 0 and q_now == 0:
                action = "Closed position"
            elif q_prev > 0 and d > 0:
                action = "Added to long"
            elif q_prev > 0 and d < 0 and q_now > 0:
                action = "Reduced long"
            elif q_prev < 0 and d < 0:
                action = "Added to short"
            elif q_prev < 0 and d > 0 and q_now < 0:
                action = "Covered short"
            elif np.sign(q_prev) != np.sign(q_now) and q_prev != 0 and q_now != 0:
                action = "Flip"
            if action:
                changes.append(
                    {
                        "date": dt,
                        "ticker": ticker,
                        "action": action,
                        "delta_quantity": d,
                    }
                )
    return pd.DataFrame(changes)
