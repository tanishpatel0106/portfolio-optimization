from __future__ import annotations

import uuid
from datetime import datetime

from sqlalchemy import JSON, Column, Date, DateTime, Enum, Float, ForeignKey, String
from sqlalchemy.orm import relationship

from .database import Base


class Instrument(Base):
    __tablename__ = "instruments"

    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    ticker = Column(String, unique=True, nullable=False)
    name = Column(String, nullable=True)
    asset_class = Column(
        Enum("Equity", "ETF", "Bond", "FX", "Commodity", "Crypto", name="asset_class"),
        nullable=False,
    )
    listing_currency = Column(String, nullable=False)
    region = Column(
        Enum("US", "EU", "JP", "IN", "SG", "OTHER", name="region"),
        nullable=False,
    )
    tags = Column(JSON, nullable=False, default=list)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    weights = relationship("PortfolioWeight", back_populates="instrument")
    trades = relationship("Trade", back_populates="instrument")


class Portfolio(Base):
    __tablename__ = "portfolios"

    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    name = Column(String, nullable=False)
    mode = Column(Enum("WEIGHTS", "TRANSACTIONS", name="portfolio_mode"), nullable=False)
    benchmark_ticker = Column(String, nullable=True)
    base_currency_mode = Column(
        Enum("AUTO", "LOCKED", name="base_currency_mode"), nullable=False, default="AUTO"
    )
    locked_base_currency = Column(String, nullable=True)
    settings = Column(JSON, nullable=False, default=dict)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    weights = relationship("PortfolioWeight", back_populates="portfolio")
    trades = relationship("Trade", back_populates="portfolio")
    snapshots = relationship("Snapshot", back_populates="portfolio")


class PortfolioWeight(Base):
    __tablename__ = "portfolio_weights"

    portfolio_id = Column(String, ForeignKey("portfolios.id"), primary_key=True)
    instrument_id = Column(String, ForeignKey("instruments.id"), primary_key=True)
    target_weight = Column(Float, nullable=False)

    portfolio = relationship("Portfolio", back_populates="weights")
    instrument = relationship("Instrument", back_populates="weights")


class Trade(Base):
    __tablename__ = "trades"

    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    portfolio_id = Column(String, ForeignKey("portfolios.id"), nullable=False)
    instrument_id = Column(String, ForeignKey("instruments.id"), nullable=False)
    trade_date = Column(Date, nullable=False)
    quantity = Column(Float, nullable=False)
    price = Column(Float, nullable=False)
    fees = Column(Float, nullable=True)
    notes = Column(String, nullable=True)

    portfolio = relationship("Portfolio", back_populates="trades")
    instrument = relationship("Instrument", back_populates="trades")


class Snapshot(Base):
    __tablename__ = "snapshots"

    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    portfolio_id = Column(String, ForeignKey("portfolios.id"), nullable=False)
    timestamp = Column(DateTime, default=datetime.utcnow)
    config_json = Column(JSON, nullable=False, default=dict)
    results_summary_json = Column(JSON, nullable=False, default=dict)
    hash = Column(String, nullable=False)

    portfolio = relationship("Portfolio", back_populates="snapshots")
