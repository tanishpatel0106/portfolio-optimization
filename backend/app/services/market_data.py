from __future__ import annotations

from datetime import datetime
from typing import Iterable

import pandas as pd
import requests_cache
import yfinance as yf

SESSION = requests_cache.CachedSession(
    "market_data_cache",
    backend="sqlite",
    expire_after=60 * 60 * 24,
)


def _parse_date(value: str | None) -> str | None:
    if value is None:
        return None
    datetime.fromisoformat(value)
    return value


def fetch_ohlcv(tickers: Iterable[str], start: str | None, end: str | None) -> dict[str, pd.DataFrame]:
    tickers_list = list(tickers)
    if not tickers_list:
        return {}
    start = _parse_date(start)
    end = _parse_date(end)
    data = yf.download(
        tickers=tickers_list,
        start=start,
        end=end,
        group_by="ticker",
        auto_adjust=False,
        progress=False,
        session=SESSION,
    )
    frames: dict[str, pd.DataFrame] = {}
    if len(tickers_list) == 1:
        frames[tickers_list[0]] = data.rename(
            columns={
                "Open": "open",
                "High": "high",
                "Low": "low",
                "Close": "close",
                "Adj Close": "adj_close",
                "Volume": "volume",
            }
        )
        return frames
    for ticker in tickers_list:
        if ticker not in data.columns.get_level_values(0):
            continue
        frame = data[ticker].rename(
            columns={
                "Open": "open",
                "High": "high",
                "Low": "low",
                "Close": "close",
                "Adj Close": "adj_close",
                "Volume": "volume",
            }
        )
        frames[ticker] = frame
    return frames


def fetch_fx(pairs: Iterable[str], start: str | None, end: str | None) -> dict[str, pd.DataFrame]:
    return fetch_ohlcv(pairs, start, end)
