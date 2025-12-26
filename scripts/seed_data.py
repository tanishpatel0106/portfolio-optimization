from datetime import date
import sys
from pathlib import Path

from sqlalchemy.orm import Session

ROOT = Path(__file__).resolve().parents[1]
sys.path.append(str(ROOT / "backend"))

from app.db import Base, engine, SessionLocal
from app.models import Instrument, Portfolio, Trade


Base.metadata.create_all(bind=engine)


def seed(db: Session):
    instruments = [
        Instrument(
            ticker="AAPL",
            name="Apple Inc",
            asset_class="Equity",
            listing_currency="USD",
            region="US",
            tags=["tech", "large_cap"],
        ),
        Instrument(
            ticker="EWJ",
            name="iShares MSCI Japan ETF",
            asset_class="ETF",
            listing_currency="USD",
            region="JP",
            tags=["international"],
        ),
    ]
    db.add_all(instruments)
    db.commit()

    portfolio = Portfolio(name="Sample Portfolio", mode="TRANSACTIONS")
    db.add(portfolio)
    db.commit()
    db.refresh(portfolio)

    trades = [
        Trade(
            portfolio_id=portfolio.id,
            instrument_id=instruments[0].id,
            trade_date=date(2024, 1, 2),
            quantity=10,
            price=100,
            fees=1.0,
            notes="Initial buy",
        )
    ]
    db.add_all(trades)
    db.commit()


if __name__ == "__main__":
    db = SessionLocal()
    seed(db)
    db.close()
