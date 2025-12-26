from __future__ import annotations

from datetime import date

from sqlalchemy.orm import Session

from backend.app import models
from backend.app.database import Base, SessionLocal, engine


SAMPLE_INSTRUMENTS = [
    {
        "ticker": "AAPL",
        "name": "Apple Inc.",
        "asset_class": "Equity",
        "listing_currency": "USD",
        "region": "US",
        "tags": ["Tech", "Large Cap"],
    },
    {
        "ticker": "IEFA",
        "name": "iShares Core MSCI EAFE",
        "asset_class": "ETF",
        "listing_currency": "USD",
        "region": "US",
        "tags": ["Equity", "International"],
    },
    {
        "ticker": "EWJ",
        "name": "iShares MSCI Japan",
        "asset_class": "ETF",
        "listing_currency": "USD",
        "region": "US",
        "tags": ["Equity", "Japan"],
    },
]


SAMPLE_TRADES = [
    {"ticker": "AAPL", "trade_date": date(2024, 1, 2), "quantity": 10, "price": 180},
    {"ticker": "IEFA", "trade_date": date(2024, 1, 3), "quantity": 20, "price": 70},
    {"ticker": "EWJ", "trade_date": date(2024, 1, 5), "quantity": 15, "price": 65},
]


def seed() -> None:
    Base.metadata.create_all(bind=engine)
    db: Session = SessionLocal()
    try:
        instruments = {}
        for instrument in SAMPLE_INSTRUMENTS:
            obj = models.Instrument(**instrument)
            db.add(obj)
            db.flush()
            instruments[instrument["ticker"]] = obj

        portfolio = models.Portfolio(
            name="Global Macro", mode="TRANSACTIONS", base_currency_mode="AUTO"
        )
        db.add(portfolio)
        db.flush()

        for trade in SAMPLE_TRADES:
            db.add(
                models.Trade(
                    portfolio_id=portfolio.id,
                    instrument_id=instruments[trade["ticker"]].id,
                    trade_date=trade["trade_date"],
                    quantity=trade["quantity"],
                    price=trade["price"],
                )
            )
        db.commit()
    finally:
        db.close()


if __name__ == "__main__":
    seed()
