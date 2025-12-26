from sqlalchemy.orm import Session

from app import models, schemas


def get_instruments(db: Session):
    return db.query(models.Instrument).all()


def create_instrument(db: Session, instrument: schemas.InstrumentCreate):
    db_obj = models.Instrument(**instrument.model_dump())
    db.add(db_obj)
    db.commit()
    db.refresh(db_obj)
    return db_obj


def update_instrument(db: Session, instrument_id: str, payload: schemas.InstrumentUpdate):
    db_obj = db.query(models.Instrument).filter(models.Instrument.id == instrument_id).first()
    if not db_obj:
        return None
    for key, value in payload.model_dump(exclude_unset=True).items():
        setattr(db_obj, key, value)
    db.commit()
    db.refresh(db_obj)
    return db_obj


def delete_instrument(db: Session, instrument_id: str):
    db_obj = db.query(models.Instrument).filter(models.Instrument.id == instrument_id).first()
    if not db_obj:
        return None
    db.delete(db_obj)
    db.commit()
    return db_obj


def get_portfolios(db: Session):
    return db.query(models.Portfolio).all()


def create_portfolio(db: Session, payload: schemas.PortfolioCreate):
    db_obj = models.Portfolio(**payload.model_dump())
    db.add(db_obj)
    db.commit()
    db.refresh(db_obj)
    return db_obj


def update_portfolio(db: Session, portfolio_id: str, payload: schemas.PortfolioUpdate):
    db_obj = db.query(models.Portfolio).filter(models.Portfolio.id == portfolio_id).first()
    if not db_obj:
        return None
    for key, value in payload.model_dump(exclude_unset=True).items():
        setattr(db_obj, key, value)
    db.commit()
    db.refresh(db_obj)
    return db_obj


def delete_portfolio(db: Session, portfolio_id: str):
    db_obj = db.query(models.Portfolio).filter(models.Portfolio.id == portfolio_id).first()
    if not db_obj:
        return None
    db.delete(db_obj)
    db.commit()
    return db_obj


def set_weights(db: Session, portfolio_id: str, weights: list[schemas.PortfolioWeightIn]):
    db.query(models.PortfolioWeight).filter(models.PortfolioWeight.portfolio_id == portfolio_id).delete()
    db.bulk_save_objects([
        models.PortfolioWeight(portfolio_id=portfolio_id, **weight.model_dump())
        for weight in weights
    ])
    db.commit()


def add_trade(db: Session, portfolio_id: str, trade: schemas.TradeIn):
    db_obj = models.Trade(portfolio_id=portfolio_id, **trade.model_dump())
    db.add(db_obj)
    db.commit()
    db.refresh(db_obj)
    return db_obj


def update_trade(db: Session, trade_id: str, trade: schemas.TradeIn):
    db_obj = db.query(models.Trade).filter(models.Trade.id == trade_id).first()
    if not db_obj:
        return None
    for key, value in trade.model_dump().items():
        setattr(db_obj, key, value)
    db.commit()
    db.refresh(db_obj)
    return db_obj


def delete_trade(db: Session, trade_id: str):
    db_obj = db.query(models.Trade).filter(models.Trade.id == trade_id).first()
    if not db_obj:
        return None
    db.delete(db_obj)
    db.commit()
    return db_obj
