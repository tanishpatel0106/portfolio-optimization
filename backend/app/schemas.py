from datetime import date, datetime
from typing import Any, Literal

from pydantic import BaseModel, Field


class InstrumentBase(BaseModel):
    ticker: str
    name: str | None = None
    asset_class: Literal["Equity", "ETF", "Bond", "FX", "Commodity", "Crypto"]
    listing_currency: str
    region: Literal["US", "EU", "JP", "IN", "SG", "OTHER"]
    tags: list[str] = Field(default_factory=list)


class InstrumentCreate(InstrumentBase):
    pass


class InstrumentUpdate(BaseModel):
    name: str | None = None
    asset_class: Literal["Equity", "ETF", "Bond", "FX", "Commodity", "Crypto"] | None = None
    listing_currency: str | None = None
    region: Literal["US", "EU", "JP", "IN", "SG", "OTHER"] | None = None
    tags: list[str] | None = None


class InstrumentOut(InstrumentBase):
    id: str
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True


class PortfolioBase(BaseModel):
    name: str
    mode: Literal["WEIGHTS", "TRANSACTIONS"]
    benchmark_ticker: str | None = None
    base_currency_mode: Literal["AUTO", "LOCKED"] = "AUTO"
    locked_base_currency: str | None = None
    settings: dict[str, Any] = Field(default_factory=dict)


class PortfolioCreate(PortfolioBase):
    pass


class PortfolioUpdate(BaseModel):
    name: str | None = None
    benchmark_ticker: str | None = None
    base_currency_mode: Literal["AUTO", "LOCKED"] | None = None
    locked_base_currency: str | None = None
    settings: dict[str, Any] | None = None


class PortfolioOut(PortfolioBase):
    id: str
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True


class PortfolioWeightIn(BaseModel):
    instrument_id: str
    target_weight: float


class TradeIn(BaseModel):
    instrument_id: str
    trade_date: date
    quantity: float
    price: float
    fees: float | None = None
    notes: str | None = None


class TradeOut(TradeIn):
    id: str
    portfolio_id: str

    class Config:
        from_attributes = True


class PositionOut(BaseModel):
    instrument_id: str
    ticker: str
    quantity: float
    market_value: float
    listing_currency: str
    long_short: Literal["LONG", "SHORT", "FLAT"]


class PositionChangeOut(BaseModel):
    date: date
    ticker: str
    action: str
    delta_quantity: float
    notional_change: float


class BaseCurrencyOut(BaseModel):
    base_currency: str
    share: float
    fallback_reason: str | None = None


class AnalyticsOut(BaseModel):
    summary: dict[str, Any]
    monthly_returns: list[dict[str, Any]]
    rolling_metrics: list[dict[str, Any]]


class RiskOut(BaseModel):
    correlation: dict[str, Any]
    risk_contributions: list[dict[str, Any]]
    tracking_error: float | None = None
    information_ratio: float | None = None


class TailOut(BaseModel):
    var_cvar: dict[str, Any]
    worst_windows: list[dict[str, Any]]


class OptimizationRequest(BaseModel):
    long_only: bool = True
    max_weight: float = 0.2
    gross_exposure_cap: float | None = None
    turnover_cap: float | None = None


class OptimizationOut(BaseModel):
    frontier: list[dict[str, float]]
    recommended_weights: list[dict[str, float]]
