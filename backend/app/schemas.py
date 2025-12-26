from __future__ import annotations

from datetime import date, datetime
from typing import Any, Optional

from pydantic import BaseModel, Field


class InstrumentBase(BaseModel):
    ticker: str
    name: Optional[str] = None
    asset_class: str
    listing_currency: str
    region: str
    tags: list[str] = Field(default_factory=list)


class InstrumentCreate(InstrumentBase):
    pass


class InstrumentUpdate(BaseModel):
    name: Optional[str] = None
    asset_class: Optional[str] = None
    listing_currency: Optional[str] = None
    region: Optional[str] = None
    tags: Optional[list[str]] = None


class InstrumentOut(InstrumentBase):
    id: str
    created_at: datetime
    updated_at: datetime

    model_config = {"from_attributes": True}


class PortfolioBase(BaseModel):
    name: str
    mode: str
    benchmark_ticker: Optional[str] = None
    base_currency_mode: str = "AUTO"
    locked_base_currency: Optional[str] = None
    settings: dict[str, Any] = Field(default_factory=dict)


class PortfolioCreate(PortfolioBase):
    pass


class PortfolioUpdate(BaseModel):
    name: Optional[str] = None
    mode: Optional[str] = None
    benchmark_ticker: Optional[str] = None
    base_currency_mode: Optional[str] = None
    locked_base_currency: Optional[str] = None
    settings: Optional[dict[str, Any]] = None


class PortfolioOut(PortfolioBase):
    id: str
    created_at: datetime
    updated_at: datetime

    model_config = {"from_attributes": True}


class PortfolioWeightIn(BaseModel):
    instrument_id: str
    target_weight: float


class PortfolioWeightOut(PortfolioWeightIn):
    portfolio_id: str

    model_config = {"from_attributes": True}


class TradeBase(BaseModel):
    instrument_id: str
    trade_date: date
    quantity: float
    price: float
    fees: Optional[float] = None
    notes: Optional[str] = None


class TradeCreate(TradeBase):
    pass


class TradeUpdate(BaseModel):
    trade_date: Optional[date] = None
    quantity: Optional[float] = None
    price: Optional[float] = None
    fees: Optional[float] = None
    notes: Optional[str] = None


class TradeOut(TradeBase):
    id: str
    portfolio_id: str

    model_config = {"from_attributes": True}


class BaseCurrencyOut(BaseModel):
    base_currency: str
    share: float
    method: str


class PositionOut(BaseModel):
    instrument_id: str
    ticker: str
    quantity: float
    price: float
    currency: str
    market_value: float
    long_short: str


class PositionChangeOut(BaseModel):
    date: date
    ticker: str
    action: str
    delta_quantity: float
    notional_change: float


class AnalyticsOut(BaseModel):
    performance: dict[str, Any]
    risk: dict[str, Any]
    tail: dict[str, Any]
