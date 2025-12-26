from __future__ import annotations

import csv
from datetime import date
from io import StringIO
from typing import Annotated

import pandas as pd
from fastapi import Depends, FastAPI, HTTPException, Query
from fastapi.responses import StreamingResponse
from sqlalchemy.orm import Session

from app import crud, models, schemas
from app.db import Base, engine, get_db
from app.services import analytics, market_data, portfolio_engine

Base.metadata.create_all(bind=engine)

app = FastAPI(title="Global Regime-Adaptive Portfolio Risk API")


@app.get("/health")
async def health():
    return {"status": "ok"}


@app.get("/instruments", response_model=list[schemas.InstrumentOut])
async def get_instruments(db: Annotated[Session, Depends(get_db)]):
    return crud.get_instruments(db)


@app.post("/instruments", response_model=schemas.InstrumentOut)
async def create_instrument(payload: schemas.InstrumentCreate, db: Annotated[Session, Depends(get_db)]):
    return crud.create_instrument(db, payload)


@app.put("/instruments/{instrument_id}", response_model=schemas.InstrumentOut)
async def update_instrument(
    instrument_id: str, payload: schemas.InstrumentUpdate, db: Annotated[Session, Depends(get_db)]
):
    result = crud.update_instrument(db, instrument_id, payload)
    if not result:
        raise HTTPException(status_code=404, detail="Instrument not found")
    return result


@app.delete("/instruments/{instrument_id}")
async def delete_instrument(instrument_id: str, db: Annotated[Session, Depends(get_db)]):
    result = crud.delete_instrument(db, instrument_id)
    if not result:
        raise HTTPException(status_code=404, detail="Instrument not found")
    return {"status": "deleted"}


@app.post("/instruments/import_csv")
async def import_instruments(csv_text: str, db: Annotated[Session, Depends(get_db)]):
    reader = csv.DictReader(StringIO(csv_text))
    created = []
    for row in reader:
        payload = schemas.InstrumentCreate(
            ticker=row["ticker"],
            name=row.get("name"),
            asset_class=row["asset_class"],
            listing_currency=row["listing_currency"],
            region=row["region"],
            tags=(row.get("tags") or "").split("|") if row.get("tags") else [],
        )
        created.append(crud.create_instrument(db, payload))
    return {"count": len(created)}


@app.get("/instruments/export_csv")
async def export_instruments(db: Annotated[Session, Depends(get_db)]):
    output = StringIO()
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
    output.seek(0)
    return StreamingResponse(iter([output.getvalue()]), media_type="text/csv")


@app.get("/market/ohlcv")
async def get_market_ohlcv(
    tickers: str = Query(...),
    start: date = Query(...),
    end: date = Query(...),
):
    ticker_list = [ticker.strip() for ticker in tickers.split(",") if ticker.strip()]
    data = market_data.fetch_ohlcv(ticker_list, start, end)
    return {ticker: frame.reset_index().to_dict(orient="records") for ticker, frame in data.items()}


@app.get("/market/fx")
async def get_market_fx(
    pairs: str = Query(...),
    start: date = Query(...),
    end: date = Query(...),
):
    pair_list = [pair.strip() for pair in pairs.split(",") if pair.strip()]
    data = market_data.fetch_fx(pair_list, start, end)
    return {pair: frame.reset_index().to_dict(orient="records") for pair, frame in data.items()}


@app.get("/portfolios", response_model=list[schemas.PortfolioOut])
async def get_portfolios(db: Annotated[Session, Depends(get_db)]):
    return crud.get_portfolios(db)


@app.post("/portfolios", response_model=schemas.PortfolioOut)
async def create_portfolio(payload: schemas.PortfolioCreate, db: Annotated[Session, Depends(get_db)]):
    return crud.create_portfolio(db, payload)


@app.get("/portfolios/{portfolio_id}", response_model=schemas.PortfolioOut)
async def get_portfolio(portfolio_id: str, db: Annotated[Session, Depends(get_db)]):
    obj = db.query(models.Portfolio).filter(models.Portfolio.id == portfolio_id).first()
    if not obj:
        raise HTTPException(status_code=404, detail="Portfolio not found")
    return obj


@app.put("/portfolios/{portfolio_id}", response_model=schemas.PortfolioOut)
async def update_portfolio(
    portfolio_id: str, payload: schemas.PortfolioUpdate, db: Annotated[Session, Depends(get_db)]
):
    obj = crud.update_portfolio(db, portfolio_id, payload)
    if not obj:
        raise HTTPException(status_code=404, detail="Portfolio not found")
    return obj


@app.delete("/portfolios/{portfolio_id}")
async def delete_portfolio(portfolio_id: str, db: Annotated[Session, Depends(get_db)]):
    obj = crud.delete_portfolio(db, portfolio_id)
    if not obj:
        raise HTTPException(status_code=404, detail="Portfolio not found")
    return {"status": "deleted"}


@app.put("/portfolios/{portfolio_id}/weights")
async def set_weights(
    portfolio_id: str,
    payload: list[schemas.PortfolioWeightIn],
    db: Annotated[Session, Depends(get_db)],
):
    crud.set_weights(db, portfolio_id, payload)
    return {"status": "ok"}


@app.post("/portfolios/{portfolio_id}/trades", response_model=schemas.TradeOut)
async def add_trade(
    portfolio_id: str, payload: schemas.TradeIn, db: Annotated[Session, Depends(get_db)]
):
    return crud.add_trade(db, portfolio_id, payload)


@app.put("/portfolios/{portfolio_id}/trades/{trade_id}", response_model=schemas.TradeOut)
async def update_trade(
    portfolio_id: str,
    trade_id: str,
    payload: schemas.TradeIn,
    db: Annotated[Session, Depends(get_db)],
):
    trade = crud.update_trade(db, trade_id, payload)
    if not trade:
        raise HTTPException(status_code=404, detail="Trade not found")
    return trade


@app.delete("/portfolios/{portfolio_id}/trades/{trade_id}")
async def delete_trade(
    portfolio_id: str, trade_id: str, db: Annotated[Session, Depends(get_db)]
):
    trade = crud.delete_trade(db, trade_id)
    if not trade:
        raise HTTPException(status_code=404, detail="Trade not found")
    return {"status": "deleted"}


@app.post("/portfolios/{portfolio_id}/trades/import_csv")
async def import_trades(
    portfolio_id: str, csv_text: str, db: Annotated[Session, Depends(get_db)]
):
    reader = csv.DictReader(StringIO(csv_text))
    for row in reader:
        payload = schemas.TradeIn(
            instrument_id=row["instrument_id"],
            trade_date=date.fromisoformat(row["trade_date"]),
            quantity=float(row["quantity"]),
            price=float(row["price"]),
            fees=float(row["fees"]) if row.get("fees") else None,
            notes=row.get("notes"),
        )
        crud.add_trade(db, portfolio_id, payload)
    return {"status": "ok"}


@app.get("/portfolios/{portfolio_id}/base_currency", response_model=schemas.BaseCurrencyOut)
async def get_base_currency(
    portfolio_id: str,
    asof: date,
    db: Annotated[Session, Depends(get_db)],
):
    portfolio = db.query(models.Portfolio).filter(models.Portfolio.id == portfolio_id).first()
    if not portfolio:
        raise HTTPException(status_code=404, detail="Portfolio not found")
    positions, prices, currency_map = _build_positions_and_prices(db, portfolio_id, asof)
    fx_pairs = {f"{currency}USD=X" for currency in currency_map.values() if currency != "USD"}
    fx_frames = market_data.fetch_fx(fx_pairs, asof, asof)
    fx_series = {currency: frame["Close"] for currency, frame in _pair_to_currency(fx_frames).items()}
    result = portfolio_engine.detect_base_currency(
        positions,
        prices,
        currency_map,
        fx_series,
        locked_currency=portfolio.locked_base_currency,
    )
    return schemas.BaseCurrencyOut(
        base_currency=result.base_currency,
        share=result.share,
        fallback_reason=result.fallback_reason,
    )


@app.get("/portfolios/{portfolio_id}/positions", response_model=list[schemas.PositionOut])
async def get_positions(
    portfolio_id: str,
    asof: date,
    db: Annotated[Session, Depends(get_db)],
):
    positions, prices, currency_map = _build_positions_and_prices(db, portfolio_id, asof)
    asof_quantities = positions.iloc[-1]
    asof_prices = prices.iloc[-1]
    results = []
    for ticker, qty in asof_quantities.items():
        mv = qty * asof_prices[ticker]
        long_short = "FLAT"
        if qty > 0:
            long_short = "LONG"
        elif qty < 0:
            long_short = "SHORT"
        instrument = db.query(models.Instrument).filter(models.Instrument.ticker == ticker).first()
        results.append(
            schemas.PositionOut(
                instrument_id=instrument.id if instrument else "",
                ticker=ticker,
                quantity=qty,
                market_value=mv,
                listing_currency=currency_map.get(ticker, "USD"),
                long_short=long_short,
            )
        )
    return results


@app.get("/portfolios/{portfolio_id}/position_changes", response_model=list[schemas.PositionChangeOut])
async def get_position_changes(
    portfolio_id: str,
    start: date,
    end: date,
    db: Annotated[Session, Depends(get_db)],
):
    positions, prices, currency_map = _build_positions_and_prices(db, portfolio_id, end)
    positions = positions.loc[start:end]
    changes = portfolio_engine.classify_position_changes(positions)
    results = []
    for _, row in changes.iterrows():
        price = prices.loc[row["date"], row["ticker"]]
        results.append(
            schemas.PositionChangeOut(
                date=row["date"],
                ticker=row["ticker"],
                action=row["action"],
                delta_quantity=row["delta_quantity"],
                notional_change=row["delta_quantity"] * price,
            )
        )
    return results


@app.get("/portfolios/{portfolio_id}/portfolio_ohlcv")
async def get_portfolio_ohlcv(
    portfolio_id: str,
    start: date,
    end: date,
    db: Annotated[Session, Depends(get_db)],
):
    positions, prices, currency_map = _build_positions_and_prices(db, portfolio_id, end)
    positions = positions.loc[start:end]
    ohlcv = _fetch_ohlcv_for_prices(prices, start, end)
    fx_matrix = portfolio_engine.build_fx_matrix(prices.columns, currency_map, "USD", {})
    portfolio = portfolio_engine.synthesize_portfolio_ohlcv(positions, ohlcv, fx_matrix)
    return portfolio.reset_index().to_dict(orient="records")


@app.get("/portfolios/{portfolio_id}/analytics", response_model=schemas.AnalyticsOut)
async def get_analytics(
    portfolio_id: str,
    start: date,
    end: date,
    db: Annotated[Session, Depends(get_db)],
):
    positions, prices, _ = _build_positions_and_prices(db, portfolio_id, end)
    positions = positions.loc[start:end]
    prices = prices.loc[start:end]
    portfolio_value = (positions * prices).sum(axis=1)
    returns = analytics.compute_returns(portfolio_value)
    summary = analytics.performance_summary(returns)
    monthly = returns.resample("M").apply(lambda x: (1 + x).prod() - 1).reset_index()
    rolling = returns.rolling(63).mean().reset_index()
    return schemas.AnalyticsOut(
        summary=summary,
        monthly_returns=monthly.rename(columns={0: "return"}).to_dict(orient="records"),
        rolling_metrics=rolling.rename(columns={0: "rolling_return"}).to_dict(orient="records"),
    )


@app.get("/portfolios/{portfolio_id}/risk", response_model=schemas.RiskOut)
async def get_risk(
    portfolio_id: str,
    start: date,
    end: date,
    db: Annotated[Session, Depends(get_db)],
):
    positions, prices, _ = _build_positions_and_prices(db, portfolio_id, end)
    returns = prices.pct_change().dropna()
    cov = returns.cov()
    weights = positions.iloc[-1].values
    rc = analytics.risk_contributions(weights, cov.values)
    rc_payload = [
        {"ticker": ticker, "risk_contribution": float(val)}
        for ticker, val in zip(prices.columns, rc)
    ]
    corr = returns.corr().to_dict()
    return schemas.RiskOut(correlation=corr, risk_contributions=rc_payload)


@app.get("/portfolios/{portfolio_id}/tail", response_model=schemas.TailOut)
async def get_tail(
    portfolio_id: str,
    start: date,
    end: date,
    db: Annotated[Session, Depends(get_db)],
):
    positions, prices, _ = _build_positions_and_prices(db, portfolio_id, end)
    portfolio_value = (positions * prices).sum(axis=1)
    returns = analytics.compute_returns(portfolio_value)
    var = analytics.var_cvar(returns)
    worst = returns.rolling(21).sum().nsmallest(5).reset_index()
    return schemas.TailOut(
        var_cvar=var,
        worst_windows=worst.rename(columns={0: "rolling_loss"}).to_dict(orient="records"),
    )


def _build_positions_and_prices(db: Session, portfolio_id: str, end: date):
    portfolio = db.query(models.Portfolio).filter(models.Portfolio.id == portfolio_id).first()
    if not portfolio:
        raise HTTPException(status_code=404, detail="Portfolio not found")
    instruments = db.query(models.Instrument).all()
    tickers = [instrument.ticker for instrument in instruments]
    if not tickers:
        raise HTTPException(status_code=400, detail="No instruments defined")
    prices = _fetch_close_prices(tickers, end)
    currency_map = {instrument.ticker: instrument.listing_currency for instrument in instruments}
    if portfolio.mode == "WEIGHTS":
        weights = pd.Series({w.instrument_id: w.target_weight for w in portfolio.weights})
        weight_map = {
            instrument.ticker: weights.get(instrument.id, 0.0) for instrument in instruments
        }
        weights_df = pd.DataFrame([weight_map], index=[prices.index[0]])
        positions = portfolio_engine.compute_positions_from_weights(weights_df, prices)
    else:
        trades = [
            {
                "ticker": trade.instrument.ticker,
                "trade_date": trade.trade_date,
                "quantity": trade.quantity,
            }
            for trade in portfolio.trades
        ]
        trades_df = pd.DataFrame(trades)
        positions = portfolio_engine.compute_positions_from_trades(trades_df, prices)
    return positions, prices, currency_map


def _fetch_close_prices(tickers: list[str], end: date):
    start = date(end.year - 1, end.month, end.day)
    frames = market_data.fetch_ohlcv(tickers, start, end)
    if not frames:
        raise HTTPException(status_code=400, detail="No price data available")
    closes = {}
    for ticker, frame in frames.items():
        closes[ticker] = frame["Close"]
    prices = pd.DataFrame(closes).dropna(how="all")
    return prices


def _fetch_ohlcv_for_prices(prices: pd.DataFrame, start: date, end: date):
    frames = market_data.fetch_ohlcv(prices.columns, start, end)
    return frames


def _pair_to_currency(frames: dict[str, pd.DataFrame]) -> dict[str, pd.DataFrame]:
    mapping = {}
    for pair, frame in frames.items():
        currency = pair.replace("USD=X", "")
        mapping[currency] = frame
    return mapping
