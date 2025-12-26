from __future__ import annotations

import csv
import io
from datetime import date, datetime, timedelta
from typing import Any

import pandas as pd
from fastapi import Depends, FastAPI, File, HTTPException, UploadFile
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session

from . import crud, models, schemas
from .database import Base, SessionLocal, engine
from .services import analytics, market_data, portfolio_engine

Base.metadata.create_all(bind=engine)

app = FastAPI(title="Global Regime-Adaptive Portfolio Studio")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"]
    ,
    allow_headers=["*"],
)


def get_db() -> Session:
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@app.get("/health")
async def health() -> dict[str, str]:
    return {"status": "ok"}


@app.get("/instruments", response_model=list[schemas.InstrumentOut])
async def list_instruments(db: Session = Depends(get_db)) -> list[models.Instrument]:
    return crud.get_instruments(db)


@app.post("/instruments", response_model=schemas.InstrumentOut)
async def create_instrument(
    instrument: schemas.InstrumentCreate, db: Session = Depends(get_db)
) -> models.Instrument:
    if crud.get_instrument_by_ticker(db, instrument.ticker):
        raise HTTPException(status_code=400, detail="Ticker already exists")
    return crud.create_instrument(db, instrument)


@app.put("/instruments/{instrument_id}", response_model=schemas.InstrumentOut)
async def update_instrument(
    instrument_id: str, instrument: schemas.InstrumentUpdate, db: Session = Depends(get_db)
) -> models.Instrument:
    db_instrument = crud.get_instrument(db, instrument_id)
    if not db_instrument:
        raise HTTPException(status_code=404, detail="Instrument not found")
    return crud.update_instrument(db, db_instrument, instrument)


@app.delete("/instruments/{instrument_id}")
async def delete_instrument(instrument_id: str, db: Session = Depends(get_db)) -> dict[str, str]:
    db_instrument = crud.get_instrument(db, instrument_id)
    if not db_instrument:
        raise HTTPException(status_code=404, detail="Instrument not found")
    crud.delete_instrument(db, db_instrument)
    return {"status": "deleted"}


@app.post("/instruments/import_csv", response_model=list[schemas.InstrumentOut])
async def import_instruments(
    file: UploadFile = File(...), db: Session = Depends(get_db)
) -> list[models.Instrument]:
    content = await file.read()
    reader = csv.DictReader(io.StringIO(content.decode("utf-8")))
    instruments = []
    for row in reader:
        instrument = schemas.InstrumentCreate(
            ticker=row["ticker"],
            name=row.get("name"),
            asset_class=row["asset_class"],
            listing_currency=row["listing_currency"],
            region=row["region"],
            tags=[tag.strip() for tag in row.get("tags", "").split("|") if tag.strip()],
        )
        instruments.append(crud.create_instrument(db, instrument))
    return instruments


@app.get("/instruments/export_csv")
async def export_instruments(db: Session = Depends(get_db)) -> dict[str, Any]:
    output = io.StringIO()
    writer = csv.writer(output)
    writer.writerow(["ticker", "name", "asset_class", "listing_currency", "region", "tags"])
    for instrument in crud.get_instruments(db):
        writer.writerow(
            [
                instrument.ticker,
                instrument.name or "",
                instrument.asset_class,
                instrument.listing_currency,
                instrument.region,
                "|".join(instrument.tags or []),
            ]
        )
    return {"csv": output.getvalue()}


@app.get("/market/ohlcv")
async def get_ohlcv(tickers: str, start: str | None = None, end: str | None = None) -> dict[str, Any]:
    ticker_list = [ticker.strip() for ticker in tickers.split(",") if ticker.strip()]
    frames = market_data.fetch_ohlcv(ticker_list, start, end)
    return {
        ticker: frame.reset_index().to_dict(orient="records") for ticker, frame in frames.items()
    }


@app.get("/market/fx")
async def get_fx(pairs: str, start: str | None = None, end: str | None = None) -> dict[str, Any]:
    pair_list = [pair.strip() for pair in pairs.split(",") if pair.strip()]
    frames = market_data.fetch_fx(pair_list, start, end)
    return {
        pair: frame.reset_index().to_dict(orient="records") for pair, frame in frames.items()
    }


@app.get("/portfolios", response_model=list[schemas.PortfolioOut])
async def list_portfolios(db: Session = Depends(get_db)) -> list[models.Portfolio]:
    return crud.get_portfolios(db)


@app.post("/portfolios", response_model=schemas.PortfolioOut)
async def create_portfolio(
    portfolio: schemas.PortfolioCreate, db: Session = Depends(get_db)
) -> models.Portfolio:
    return crud.create_portfolio(db, portfolio)


@app.get("/portfolios/{portfolio_id}", response_model=schemas.PortfolioOut)
async def get_portfolio(portfolio_id: str, db: Session = Depends(get_db)) -> models.Portfolio:
    db_portfolio = crud.get_portfolio(db, portfolio_id)
    if not db_portfolio:
        raise HTTPException(status_code=404, detail="Portfolio not found")
    return db_portfolio


@app.put("/portfolios/{portfolio_id}", response_model=schemas.PortfolioOut)
async def update_portfolio(
    portfolio_id: str, portfolio: schemas.PortfolioUpdate, db: Session = Depends(get_db)
) -> models.Portfolio:
    db_portfolio = crud.get_portfolio(db, portfolio_id)
    if not db_portfolio:
        raise HTTPException(status_code=404, detail="Portfolio not found")
    return crud.update_portfolio(db, db_portfolio, portfolio)


@app.delete("/portfolios/{portfolio_id}")
async def delete_portfolio(portfolio_id: str, db: Session = Depends(get_db)) -> dict[str, str]:
    db_portfolio = crud.get_portfolio(db, portfolio_id)
    if not db_portfolio:
        raise HTTPException(status_code=404, detail="Portfolio not found")
    crud.delete_portfolio(db, db_portfolio)
    return {"status": "deleted"}


@app.put("/portfolios/{portfolio_id}/weights", response_model=list[schemas.PortfolioWeightOut])
async def update_weights(
    portfolio_id: str, weights: list[schemas.PortfolioWeightIn], db: Session = Depends(get_db)
) -> list[models.PortfolioWeight]:
    db_portfolio = crud.get_portfolio(db, portfolio_id)
    if not db_portfolio:
        raise HTTPException(status_code=404, detail="Portfolio not found")
    return crud.replace_weights(db, portfolio_id, weights)


@app.post("/portfolios/{portfolio_id}/trades", response_model=schemas.TradeOut)
async def create_trade(
    portfolio_id: str, trade: schemas.TradeCreate, db: Session = Depends(get_db)
) -> models.Trade:
    db_portfolio = crud.get_portfolio(db, portfolio_id)
    if not db_portfolio:
        raise HTTPException(status_code=404, detail="Portfolio not found")
    return crud.add_trade(db, portfolio_id, trade)


@app.put("/portfolios/{portfolio_id}/trades/{trade_id}", response_model=schemas.TradeOut)
async def update_trade(
    portfolio_id: str, trade_id: str, trade: schemas.TradeUpdate, db: Session = Depends(get_db)
) -> models.Trade:
    db_trade = db.query(models.Trade).filter(
        models.Trade.id == trade_id, models.Trade.portfolio_id == portfolio_id
    ).first()
    if not db_trade:
        raise HTTPException(status_code=404, detail="Trade not found")
    return crud.update_trade(db, db_trade, trade)


@app.delete("/portfolios/{portfolio_id}/trades/{trade_id}")
async def delete_trade(
    portfolio_id: str, trade_id: str, db: Session = Depends(get_db)
) -> dict[str, str]:
    db_trade = db.query(models.Trade).filter(
        models.Trade.id == trade_id, models.Trade.portfolio_id == portfolio_id
    ).first()
    if not db_trade:
        raise HTTPException(status_code=404, detail="Trade not found")
    crud.delete_trade(db, db_trade)
    return {"status": "deleted"}


@app.post("/portfolios/{portfolio_id}/trades/import_csv", response_model=list[schemas.TradeOut])
async def import_trades(
    portfolio_id: str, file: UploadFile = File(...), db: Session = Depends(get_db)
) -> list[models.Trade]:
    db_portfolio = crud.get_portfolio(db, portfolio_id)
    if not db_portfolio:
        raise HTTPException(status_code=404, detail="Portfolio not found")
    content = await file.read()
    reader = csv.DictReader(io.StringIO(content.decode("utf-8")))
    trades = []
    for row in reader:
        trade = schemas.TradeCreate(
            instrument_id=row["instrument_id"],
            trade_date=datetime.fromisoformat(row["trade_date"]).date(),
            quantity=float(row["quantity"]),
            price=float(row["price"]),
            fees=float(row["fees"]) if row.get("fees") else None,
            notes=row.get("notes"),
        )
        trades.append(crud.add_trade(db, portfolio_id, trade))
    return trades


def _latest_prices(tickers: list[str], asof: date) -> dict[str, float]:
    start = (asof - timedelta(days=10)).isoformat()
    end = (asof + timedelta(days=1)).isoformat()
    frames = market_data.fetch_ohlcv(tickers, start, end)
    prices = {}
    for ticker, frame in frames.items():
        if frame.empty:
            continue
        prices[ticker] = float(frame["close"].iloc[-1])
    return prices


def _fx_to_usd(currencies: list[str], asof: date) -> dict[str, float]:
    pairs = [f"{currency}USD=X" for currency in currencies if currency != "USD"]
    if not pairs:
        return {"USD": 1.0}
    frames = market_data.fetch_fx(pairs, (asof - timedelta(days=10)).isoformat(), (asof + timedelta(days=1)).isoformat())
    rates = {"USD": 1.0}
    for pair, frame in frames.items():
        if frame.empty:
            continue
        currency = pair.replace("USD=X", "")
        rates[currency] = float(frame["close"].iloc[-1])
    return rates


@app.get("/portfolios/{portfolio_id}/base_currency", response_model=schemas.BaseCurrencyOut)
async def base_currency(
    portfolio_id: str, asof: date, db: Session = Depends(get_db)
) -> schemas.BaseCurrencyOut:
    db_portfolio = crud.get_portfolio(db, portfolio_id)
    if not db_portfolio:
        raise HTTPException(status_code=404, detail="Portfolio not found")
    positions = await _positions_table(db_portfolio, asof, db)
    fx_rates = _fx_to_usd(list(positions["currency"].unique()), asof)
    result = portfolio_engine.detect_base_currency(
        positions,
        fx_rates,
        locked_currency=db_portfolio.locked_base_currency,
    )
    return schemas.BaseCurrencyOut(
        base_currency=result.base_currency, share=result.share, method=result.method
    )


async def _positions_table(
    db_portfolio: models.Portfolio, asof: date, db: Session
) -> pd.DataFrame:
    instruments = {ins.id: ins for ins in crud.get_instruments(db)}
    if db_portfolio.mode == "WEIGHTS":
        weights = db.query(models.PortfolioWeight).filter(
            models.PortfolioWeight.portfolio_id == db_portfolio.id
        ).all()
        tickers = [instruments[w.instrument_id].ticker for w in weights]
        prices = _latest_prices(tickers, asof)
        data = []
        for weight in weights:
            instrument = instruments[weight.instrument_id]
            price = prices.get(instrument.ticker, 0.0)
            data.append(
                {
                    "instrument_id": instrument.id,
                    "ticker": instrument.ticker,
                    "quantity": weight.target_weight,
                    "price": price,
                    "currency": instrument.listing_currency,
                }
            )
        return portfolio_engine.compute_position_table(
            [row["ticker"] for row in data],
            [row["quantity"] for row in data],
            [row["price"] for row in data],
            [row["currency"] for row in data],
        )
    trades = db.query(models.Trade).filter(
        models.Trade.portfolio_id == db_portfolio.id,
        models.Trade.trade_date <= asof,
    ).all()
    tickers = [instruments[t.instrument_id].ticker for t in trades]
    prices = _latest_prices(list(set(tickers)), asof)
    data = []
    for trade in trades:
        instrument = instruments[trade.instrument_id]
        data.append(
            {
                "ticker": instrument.ticker,
                "quantity": trade.quantity,
                "price": trade.price,
                "currency": instrument.listing_currency,
            }
        )
    trades_df = pd.DataFrame(data)
    if trades_df.empty:
        return pd.DataFrame(columns=["ticker", "quantity", "price", "currency", "market_value"])
    positions = trades_df.groupby("ticker").agg(
        quantity=("quantity", "sum"),
        price=("price", "last"),
        currency=("currency", "last"),
    )
    positions = positions.reset_index()
    positions["price"] = positions["ticker"].map(prices).fillna(positions["price"])
    return portfolio_engine.compute_position_table(
        positions["ticker"],
        positions["quantity"],
        positions["price"],
        positions["currency"],
    )


@app.get("/portfolios/{portfolio_id}/positions", response_model=list[schemas.PositionOut])
async def positions(
    portfolio_id: str, asof: date, db: Session = Depends(get_db)
) -> list[schemas.PositionOut]:
    db_portfolio = crud.get_portfolio(db, portfolio_id)
    if not db_portfolio:
        raise HTTPException(status_code=404, detail="Portfolio not found")
    positions_df = await _positions_table(db_portfolio, asof, db)
    return [
        schemas.PositionOut(
            instrument_id="",
            ticker=row["ticker"],
            quantity=float(row["quantity"]),
            price=float(row["price"]),
            currency=row["currency"],
            market_value=float(row["market_value"]),
            long_short=row["long_short"],
        )
        for _, row in positions_df.iterrows()
    ]


@app.get("/portfolios/{portfolio_id}/position_changes", response_model=list[schemas.PositionChangeOut])
async def position_changes(
    portfolio_id: str, start: date, end: date, db: Session = Depends(get_db)
) -> list[schemas.PositionChangeOut]:
    db_portfolio = crud.get_portfolio(db, portfolio_id)
    if not db_portfolio:
        raise HTTPException(status_code=404, detail="Portfolio not found")
    trades = db.query(models.Trade).filter(
        models.Trade.portfolio_id == db_portfolio.id,
        models.Trade.trade_date >= start,
        models.Trade.trade_date <= end,
    ).all()
    if not trades:
        return []
    instruments = {ins.id: ins for ins in crud.get_instruments(db)}
    trades_df = pd.DataFrame(
        [
            {
                "trade_date": trade.trade_date,
                "ticker": instruments[trade.instrument_id].ticker,
                "quantity": trade.quantity,
                "price": trade.price,
            }
            for trade in trades
        ]
    )
    history = portfolio_engine.build_position_history_from_trades(trades_df)
    changes = portfolio_engine.classify_position_changes(history)
    return [
        schemas.PositionChangeOut(
            date=row["date"],
            ticker=row["ticker"],
            action=row["action"],
            delta_quantity=float(row["delta_quantity"]),
            notional_change=float(row["notional_change"]),
        )
        for _, row in changes.iterrows()
    ]


@app.get("/portfolios/{portfolio_id}/portfolio_ohlcv")
async def portfolio_ohlcv(
    portfolio_id: str, start: str, end: str, db: Session = Depends(get_db)
) -> dict[str, Any]:
    db_portfolio = crud.get_portfolio(db, portfolio_id)
    if not db_portfolio:
        raise HTTPException(status_code=404, detail="Portfolio not found")
    asof = datetime.fromisoformat(end).date()
    positions_df = await _positions_table(db_portfolio, asof, db)
    tickers = positions_df["ticker"].tolist()
    ohlcv = market_data.fetch_ohlcv(tickers, start, end)
    currencies = positions_df.set_index("ticker")["currency"].to_dict()
    fx_pairs = {}
    for currency in set(currencies.values()):
        if currency == "USD":
            continue
        pair = f"{currency}USD=X"
        frames = market_data.fetch_fx([pair], start, end)
        if pair in frames:
            fx_pairs[pair] = frames[pair]["close"]
    fx_series = {}
    for ticker in tickers:
        currency = currencies[ticker]
        if currency == "USD":
            fx_series[ticker] = ohlcv[ticker]["close"].copy().rename("fx")
            fx_series[ticker].loc[:] = 1.0
        else:
            pair = f"{currency}USD=X"
            if pair in fx_pairs:
                fx_series[ticker] = fx_pairs[pair]
    portfolio = portfolio_engine.build_portfolio_ohlcv(positions_df, ohlcv, fx_series)
    if portfolio.empty:
        return {"ohlcv": []}
    return {"ohlcv": portfolio.reset_index().to_dict(orient="records")}


@app.get("/portfolios/{portfolio_id}/analytics", response_model=schemas.AnalyticsOut)
async def portfolio_analytics(
    portfolio_id: str, start: str, end: str, db: Session = Depends(get_db)
) -> schemas.AnalyticsOut:
    portfolio_data = await portfolio_ohlcv(portfolio_id, start, end, db)
    if not portfolio_data["ohlcv"]:
        return schemas.AnalyticsOut(performance={}, risk={}, tail={})
    frame = pd.DataFrame(portfolio_data["ohlcv"])
    frame = frame.set_index("Date") if "Date" in frame.columns else frame.set_index("index")
    returns = analytics.compute_returns(frame["close"])
    var_hist, cvar_hist = analytics.historical_var_cvar(returns)
    var_param, cvar_param = analytics.parametric_var_cvar(returns)
    perf = {
        "cumulative_return": float((1 + returns).prod() - 1),
        "annualized_vol": float(returns.std() * (252**0.5)),
    }
    risk = {}
    tail = {
        "var_hist": var_hist,
        "cvar_hist": cvar_hist,
        "var_param": var_param,
        "cvar_param": cvar_param,
    }
    return schemas.AnalyticsOut(performance=perf, risk=risk, tail=tail)
