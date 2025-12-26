import uuid
from datetime import datetime, date

from sqlalchemy import Date, DateTime, Enum, Float, ForeignKey, String, Text, JSON
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db import Base


class Instrument(Base):
    __tablename__ = "instruments"

    id: Mapped[str] = mapped_column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    ticker: Mapped[str] = mapped_column(String, unique=True, index=True)
    name: Mapped[str | None] = mapped_column(String, nullable=True)
    asset_class: Mapped[str] = mapped_column(
        Enum("Equity", "ETF", "Bond", "FX", "Commodity", "Crypto", name="asset_class")
    )
    listing_currency: Mapped[str] = mapped_column(String)
    region: Mapped[str] = mapped_column(
        Enum("US", "EU", "JP", "IN", "SG", "OTHER", name="region")
    )
    tags: Mapped[list[str]] = mapped_column(JSON, default=list)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)
    updated_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)


class Portfolio(Base):
    __tablename__ = "portfolios"

    id: Mapped[str] = mapped_column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    name: Mapped[str] = mapped_column(String)
    mode: Mapped[str] = mapped_column(Enum("WEIGHTS", "TRANSACTIONS", name="portfolio_mode"))
    benchmark_ticker: Mapped[str | None] = mapped_column(String, nullable=True)
    base_currency_mode: Mapped[str] = mapped_column(
        Enum("AUTO", "LOCKED", name="base_currency_mode"), default="AUTO"
    )
    locked_base_currency: Mapped[str | None] = mapped_column(String, nullable=True)
    settings: Mapped[dict] = mapped_column(JSON, default=dict)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)
    updated_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)

    weights = relationship("PortfolioWeight", back_populates="portfolio", cascade="all, delete-orphan")
    trades = relationship("Trade", back_populates="portfolio", cascade="all, delete-orphan")


class PortfolioWeight(Base):
    __tablename__ = "portfolio_weights"

    portfolio_id: Mapped[str] = mapped_column(ForeignKey("portfolios.id"), primary_key=True)
    instrument_id: Mapped[str] = mapped_column(ForeignKey("instruments.id"), primary_key=True)
    target_weight: Mapped[float] = mapped_column(Float)

    portfolio = relationship("Portfolio", back_populates="weights")
    instrument = relationship("Instrument")


class Trade(Base):
    __tablename__ = "trades"

    id: Mapped[str] = mapped_column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    portfolio_id: Mapped[str] = mapped_column(ForeignKey("portfolios.id"))
    instrument_id: Mapped[str] = mapped_column(ForeignKey("instruments.id"))
    trade_date: Mapped[date] = mapped_column(Date)
    quantity: Mapped[float] = mapped_column(Float)
    price: Mapped[float] = mapped_column(Float)
    fees: Mapped[float | None] = mapped_column(Float, nullable=True)
    notes: Mapped[str | None] = mapped_column(Text, nullable=True)

    portfolio = relationship("Portfolio", back_populates="trades")
    instrument = relationship("Instrument")


class Snapshot(Base):
    __tablename__ = "snapshots"

    id: Mapped[str] = mapped_column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    portfolio_id: Mapped[str] = mapped_column(ForeignKey("portfolios.id"))
    timestamp: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)
    config_json: Mapped[dict] = mapped_column(JSON)
    results_summary_json: Mapped[dict] = mapped_column(JSON)
    hash: Mapped[str] = mapped_column(String)
