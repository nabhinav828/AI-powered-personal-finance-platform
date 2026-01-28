# AI-powered Personal Finance Platform (SmartFinance)

This repository contains a simple **personal finance dashboard** with:

- A **React + TypeScript + Vite** frontend
- A **FastAPI Core service** that stores users/transactions in Postgres
- A **FastAPI AI service** that generates short financial advice using Google Gemini via LangChain

Code lives under `smart-finance-monorepo/`.

---

## Project structure

```text
smart-finance-monorepo/
  frontend/                 # React (Vite) web app
  backend/
    core_service/           # FastAPI CRUD API (users, transactions)
    ai_service/             # FastAPI AI advisor (/analyze)
  shared/                   # Shared SQLAlchemy DB models + DB session
```

---

## Prerequisites

- **Python 3.11+**
- **Node.js 18+** (recommended 18/20)
- **PostgreSQL** (local or cloud)

---

## Environment variables

Create a file at:

- `smart-finance-monorepo/.env`

With:

```bash
# Postgres connection string used by both backend services
DATABASE_URL="postgresql+psycopg2://USER:PASSWORD@HOST:5432/DBNAME"

# Required for AI service (Gemini)
GOOGLE_API_KEY="your_google_api_key"
```

Notes:
- The DB connection is loaded in `smart-finance-monorepo/shared/database/database.py` via `python-dotenv`.
- If `DATABASE_URL` is missing, the backend will error at startup.

---

## Run locally (recommended: 3 terminals)

### 1) Start the Core API (port 8000)

```bash
cd smart-finance-monorepo/backend/core_service
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
uvicorn app.main:app --reload --port 8000
```

Verify:

- `http://127.0.0.1:8000/` returns: `SmartFinance Core Service is Running!`

### 2) Start the AI API (port 8001)

```bash
cd smart-finance-monorepo/backend/ai_service
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
uvicorn app.main:app --reload --port 8001
```

### 3) Start the frontend (port 5173)

```bash
cd smart-finance-monorepo/frontend
npm install
npm run dev
```

Open:

- `http://localhost:5173`

---

## How the services connect

The frontend calls:

- **Core API**: `http://127.0.0.1:8000`
- **AI API**: `http://127.0.0.1:8001`

These are currently hard-coded in:

- `smart-finance-monorepo/frontend/src/api/client.ts`

The backend enables CORS for:

- `http://localhost:5173` (Vite default)
- `http://localhost:3000`

---

## Main API endpoints

### Core service (port 8000)

- `POST /users/` → create a user (by email)
- `POST /transactions/?user_id=<uuid>` → add a transaction
- `GET /transactions/<user_id>` → list transactions

### AI service (port 8001)

- `POST /analyze` with JSON:

```json
{ "user_id": "uuid-here" }
```

Returns:

```json
{ "advice": "..." }
```

---

## Database notes

- Tables are created automatically on Core service startup via SQLAlchemy:
  - `users`
  - `transactions`
  - `debts`
  - `categories`

---

## Troubleshooting

- **CORS errors in the browser**
  - Make sure the frontend runs on `http://localhost:5173` (or add your origin in the backend CORS list).

- **`ValueError: DATABASE_URL is not set...`**
  - Ensure `smart-finance-monorepo/.env` exists and contains `DATABASE_URL`.

- **AI service returns 500**
  - Ensure `GOOGLE_API_KEY` is set in `smart-finance-monorepo/.env`.
  - Confirm the AI service is running on port `8001`.

---

## Dev notes / cleanup (recommended)

This repo currently includes a committed `smart-finance-monorepo/venv/` directory. In most projects you should:

- add `venv/`, `.venv/` to `.gitignore`
- remove the committed virtualenv from git history

---

## License

Add a license if you plan to open-source this project.

