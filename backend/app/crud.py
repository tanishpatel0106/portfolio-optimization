from __future__ import annotations

from sqlalchemy.orm import Session

from . import models, schemas


def get_instruments(db: Session) -> list[models.Instrument]:
    return db.query(models.Instrument).order_by(models.Instrument.ticker).all()


def get_instrument(db: Session, instrument_id: str) -> models.Instrument | None:
    return db.query(models.Instrument).filter(models.Instrument.id == instrument_id).first()


def get_instrument_by_ticker(db: Session, ticker: str) -> models.Instrument | None:
    return db.query(models.Instrument).filter(models.Instrument.ticker == ticker).first()


def create_instrument(db: Session, instrument: schemas.InstrumentCreate) -> models.Instrument:
    db_instrument = models.Instrument(**instrument.model_dump())
    db.add(db_instrument)
    db.commit()
    db.refresh(db_instrument)
    return db_instrument


def update_instrument(
    db: Session, db_instrument: models.Instrument, instrument: schemas.InstrumentUpdate
) -> models.Instrument:
    for key, value in instrument.model_dump(exclude_unset=True).items():
        setattr(db_instrument, key, value)
    db.commit()
    db.refresh(db_instrument)
    return db_instrument


def delete_instrument(db: Session, db_instrument: models.Instrument) -> None:
    db.delete(db_instrument)
    db.commit()


def get_portfolios(db: Session) -> list[models.Portfolio]:
    return db.query(models.Portfolio).order_by(models.Portfolio.created_at.desc()).all()


def get_portfolio(db: Session, portfolio_id: str) -> models.Portfolio | None:
    return db.query(models.Portfolio).filter(models.Portfolio.id == portfolio_id).first()


def create_portfolio(db: Session, portfolio: schemas.PortfolioCreate) -> models.Portfolio:
    db_portfolio = models.Portfolio(**portfolio.model_dump())
    db.add(db_portfolio)
    db.commit()
    db.refresh(db_portfolio)
    return db_portfolio


def update_portfolio(
    db: Session, db_portfolio: models.Portfolio, portfolio: schemas.PortfolioUpdate
) -> models.Portfolio:
    for key, value in portfolio.model_dump(exclude_unset=True).items():
        setattr(db_portfolio, key, value)
    db.commit()
    db.refresh(db_portfolio)
    return db_portfolio


def delete_portfolio(db: Session, db_portfolio: models.Portfolio) -> None:
    db.delete(db_portfolio)
    db.commit()


def replace_weights(
    db: Session, portfolio_id: str, weights: list[schemas.PortfolioWeightIn]
) -> list[models.PortfolioWeight]:
    db.query(models.PortfolioWeight).filter(
        models.PortfolioWeight.portfolio_id == portfolio_id
    ).delete()
    db_weights = [
        models.PortfolioWeight(
            portfolio_id=portfolio_id,
            instrument_id=weight.instrument_id,
            target_weight=weight.target_weight,
        )
        for weight in weights
    ]
    db.add_all(db_weights)
    db.commit()
    return db_weights


def add_trade(db: Session, portfolio_id: str, trade: schemas.TradeCreate) -> models.Trade:
    db_trade = models.Trade(portfolio_id=portfolio_id, **trade.model_dump())
    db.add(db_trade)
    db.commit()
    db.refresh(db_trade)
    return db_trade


def update_trade(db: Session, db_trade: models.Trade, trade: schemas.TradeUpdate) -> models.Trade:
    for key, value in trade.model_dump(exclude_unset=True).items():
        setattr(db_trade, key, value)
    db.commit()
    db.refresh(db_trade)
    return db_trade


def delete_trade(db: Session, db_trade: models.Trade) -> None:
    db.delete(db_trade)
    db.commit()
