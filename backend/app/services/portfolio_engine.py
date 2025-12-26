from __future__ import annotations

from dataclasses import dataclass
from typing import Iterable

import numpy as np
import pandas as pd


@dataclass
class BaseCurrencyResult:
    base_currency: str
    share: float
    method: str


def detect_base_currency(
    positions: pd.DataFrame,
    fx_to_usd: dict[str, float],
    locked_currency: str | None = None,
) -> BaseCurrencyResult:
    if positions.empty:
        return BaseCurrencyResult(base_currency=locked_currency or "USD", share=1.0, method="fallback")
    positions = positions.copy()
    positions["fx_to_usd"] = positions["currency"].map(lambda c: fx_to_usd.get(c, np.nan))
    positions["fx_to_usd"] = positions["fx_to_usd"].fillna(1.0)
    positions["mv_usd"] = positions["market_value"] * positions["fx_to_usd"]
    totals = positions.groupby("currency")["mv_usd"].sum()
    if totals.sum() == 0:
        fallback = locked_currency or positions["currency"].mode().iloc[0]
        return BaseCurrencyResult(base_currency=fallback, share=1.0, method="fallback")
    base_currency = totals.idxmax()
    share = float(totals.max() / totals.sum())
    return BaseCurrencyResult(base_currency=base_currency, share=share, method="auto")


def resolve_fx_series(
    local_currency: str,
    base_currency: str,
    fx_pairs: dict[str, pd.Series],
) -> pd.Series:
    if local_currency == base_currency:
        return pd.Series(1.0, index=next(iter(fx_pairs.values())).index)

    direct_pair = f"{local_currency}{base_currency}=X"
    inverse_pair = f"{base_currency}{local_currency}=X"
    if direct_pair in fx_pairs:
        return fx_pairs[direct_pair]
    if inverse_pair in fx_pairs:
        return 1 / fx_pairs[inverse_pair]

    local_usd = f"{local_currency}USD=X"
    usd_base = f"USD{base_currency}=X"
    if local_usd in fx_pairs and usd_base in fx_pairs:
        return fx_pairs[local_usd] * fx_pairs[usd_base]
    raise ValueError(f"Missing FX pair for {local_currency}->{base_currency}")


def build_portfolio_ohlcv(
    positions: pd.DataFrame,
    ohlcv: dict[str, pd.DataFrame],
    fx_series: dict[str, pd.Series],
) -> pd.DataFrame:
    if not positions.size:
        return pd.DataFrame()
    frames = []
    for _, row in positions.iterrows():
        ticker = row["ticker"]
        quantity = row["quantity"]
        if ticker not in ohlcv:
            continue
        data = ohlcv[ticker].copy()
        fx = fx_series.get(ticker)
        if fx is None:
            continue
        data = data.join(fx.rename("fx"), how="inner")
        for col in ["open", "high", "low", "close"]:
            data[col] = data[col] * data["fx"] * quantity
        data["volume"] = data["volume"].fillna(0) * abs(quantity)
        frames.append(data[["open", "high", "low", "close", "volume"]])
    if not frames:
        return pd.DataFrame()
    combined = pd.concat(frames).groupby(level=0).sum().sort_index()
    return combined


def classify_position_changes(position_history: pd.DataFrame) -> pd.DataFrame:
    records = []
    for ticker, group in position_history.groupby("ticker"):
        group = group.sort_values("date")
        prev_qty = 0.0
        for _, row in group.iterrows():
            qty = row["quantity"]
            delta = qty - prev_qty
            action = None
            if prev_qty == 0 and qty != 0:
                action = "Opened"
            elif prev_qty != 0 and qty == 0:
                action = "Closed"
            elif prev_qty > 0 and delta > 0:
                action = "Added to long"
            elif prev_qty > 0 and delta < 0:
                action = "Reduced long"
            elif prev_qty < 0 and delta < 0:
                action = "Added to short"
            elif prev_qty < 0 and delta > 0:
                action = "Covered short"
            if prev_qty != 0 and qty != 0 and np.sign(prev_qty) != np.sign(qty):
                action = "Flip"
            if action:
                records.append(
                    {
                        "date": row["date"],
                        "ticker": ticker,
                        "action": action,
                        "delta_quantity": float(delta),
                        "notional_change": float(delta * row.get("price", 0)),
                    }
                )
            prev_qty = qty
    return pd.DataFrame(records)


def build_position_history_from_trades(trades: pd.DataFrame) -> pd.DataFrame:
    if trades.empty:
        return pd.DataFrame(columns=["date", "ticker", "quantity", "price"])
    trades = trades.sort_values("trade_date")
    history = []
    for ticker, group in trades.groupby("ticker"):
        qty = 0.0
        for _, row in group.iterrows():
            qty += row["quantity"]
            history.append(
                {
                    "date": row["trade_date"],
                    "ticker": ticker,
                    "quantity": qty,
                    "price": row["price"],
                }
            )
    return pd.DataFrame(history)


def compute_position_table(
    tickers: Iterable[str],
    quantities: Iterable[float],
    prices: Iterable[float],
    currencies: Iterable[str],
) -> pd.DataFrame:
    data = pd.DataFrame(
        {
            "ticker": list(tickers),
            "quantity": list(quantities),
            "price": list(prices),
            "currency": list(currencies),
        }
    )
    data["market_value"] = data["quantity"] * data["price"]
    data["long_short"] = data["quantity"].apply(lambda q: "Long" if q >= 0 else "Short")
    return data
