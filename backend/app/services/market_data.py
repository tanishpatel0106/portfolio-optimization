from __future__ import annotations

from datetime import date
from typing import Iterable

import pandas as pd
import requests_cache
import yfinance as yf

from app.core.config import settings


requests_cache.install_cache(
    cache_name=f"{settings.cache_dir}/yfinance",
    backend="sqlite",
    expire_after=settings.cache_ttl_seconds,
)


def _to_iso(value: date | str) -> str:
    if isinstance(value, date):
        return value.isoformat()
    return value


def fetch_ohlcv(tickers: Iterable[str], start: date | str, end: date | str) -> dict[str, pd.DataFrame]:
    start_str = _to_iso(start)
    end_str = _to_iso(end)
    data = yf.download(list(tickers), start=start_str, end=end_str, group_by="ticker", auto_adjust=False)
    if data.empty:
        return {}
    result: dict[str, pd.DataFrame] = {}
    if isinstance(data.columns, pd.MultiIndex):
        for ticker in tickers:
            if ticker in data.columns.get_level_values(0):
                frame = data[ticker].dropna(how="all")
                frame.index = frame.index.tz_localize(None)
                result[ticker] = frame
    else:
        frame = data.dropna(how="all")
        frame.index = frame.index.tz_localize(None)
        result[list(tickers)[0]] = frame
    return result


def fetch_fx(pairs: Iterable[str], start: date | str, end: date | str) -> dict[str, pd.DataFrame]:
    return fetch_ohlcv(pairs, start, end)
