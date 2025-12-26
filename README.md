# Global Regime-Adaptive Portfolio Risk, Allocation & Position Studio

A multi-page platform for building global investable universes, constructing portfolios, and running institutional analytics across performance, risk, tail, optimization, and regime detection.

## Repository Structure

- `backend/`: FastAPI service, SQLite persistence, analytics engines, and REST endpoints.
- `frontend/`: Next.js App Router dashboard with Plotly charts and sidebar navigation.
- `sample_csv/`: CSV templates for instruments and trades.
- `scripts/seed_data.py`: Sample seed data loader.

## Local Development

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

Set the frontend backend URL via:

```bash
export NEXT_PUBLIC_BACKEND_URL=http://localhost:8000
```

### Seed Sample Data

```bash
python scripts/seed_data.py
```

## Docker

```bash
docker compose up --build
```

Frontend will be available at `http://localhost:3000`, backend at `http://localhost:8000`.

## Notes & Assumptions

- yfinance data coverage varies by ticker and FX pair; missing data is handled with warnings where possible.
- FX conversion uses direct pairs or USD triangulation when available.
- Portfolio volume uses absolute position sizes as a proxy.
- Missing OHLCV dates are aligned by date index when combining series.
