# Global Regime-Adaptive Portfolio Risk, Allocation & Position Studio

Institutional-grade portfolio analytics platform with a FastAPI backend and Next.js frontend.

## Stack
- **Frontend:** Next.js App Router + TypeScript + Tailwind + Plotly (react-plotly.js)
- **Backend:** FastAPI + SQLAlchemy + SQLite + yfinance + caching

## Project Layout
```
backend/   FastAPI app + analytics engine + tests
frontend/  Next.js dashboard
samples/   CSV templates
scripts/   Seed data helpers
```

## Quickstart (without Docker)
### Backend
```bash
cd backend
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
uvicorn app.main:app --reload
```

### Frontend
```bash
cd frontend
npm install
npm run dev
```

Set the backend base URL in `frontend/.env.local`:
```
NEXT_PUBLIC_API_BASE_URL=http://localhost:8000
```

## Docker
```bash
docker compose up --build
```

Frontend runs on http://localhost:3000 and backend on http://localhost:8000.

## Seed Data
```bash
cd backend
python ../scripts/seed_data.py
```

## Assumptions & Limitations
- **Market data:** yfinance daily bars; missing data is forward-filled when building synthetic OHLCV.
- **FX:** If a direct FX pair is missing, the backend attempts USD triangulation (local→USD→base).
- **Volume:** Portfolio volume is a proxy based on |quantity| × instrument volume.
- **Regimes:** KMeans clustering on rolling vol, rolling return, and drawdown level.
- **Data gaps:** If FX or ticker data is unavailable, responses are returned with warnings and skipped series.

## Samples
- `samples/instruments_template.csv`
- `samples/trades_template.csv`

## Testing
```bash
cd backend
pytest
```
