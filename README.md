# Loja App

A learning project for simulating payment options and saving receipts. It does not process real charges. The interface and API field names are in Portuguese.

## How it works

The React interface follows a form → simulation → confirmation → receipt flow. FastAPI calculates the amounts and saves confirmed payments through SQLAlchemy.

| Option (`opcao`) | Method | Installments | Rule |
| --- | --- | --- | --- |
| 1 | Cash | 1 | 10% discount |
| 2 | Debit | 1 | 5% discount |
| 3 | Credit, without interest | 2–6 | Original amount |
| 4 | Credit, with interest | 12–24 | 10% added to the total |

Amounts are rounded to two decimal places. The last installment is adjusted to account for rounding. These are the current API defaults; `backend/config/taxas.json` is not loaded by the payment flow.

## Structure

- `frontend/`: React, TypeScript, Vite and Tailwind CSS; forms, API calls, receipts and theme toggle.
- `backend/api/`: FastAPI routes and request/response models.
- `backend/services/`: payment creation, idempotency lookup and listing.
- `backend/domain/`: payment calculations, receipts and repository interface.
- `backend/infrastructure/`: SQLAlchemy models, database sessions and repositories.
- `backend/alembic/`: database migrations.

## Run locally

Use Python 3.11, Node.js 22.12+ and npm. Run the backend and frontend in separate terminals, starting from the repository root.

### Backend

```sh
cd backend
python -m venv .venv
```

Activate the environment:

```sh
# Bash
source .venv/bin/activate
```

```powershell
# PowerShell
.\.venv\Scripts\Activate.ps1
```

Install dependencies, then create `.env` in the current `backend/` directory:

```sh
python -m pip install -r requirements.txt
```

```dotenv
DATABASE_URL=sqlite:///./loja_app.db
```

Start the API:

```sh
python -m uvicorn api.main:app --reload
```

The API runs at [localhost:8000](http://localhost:8000), with [Swagger UI](http://localhost:8000/docs) and a [health endpoint](http://localhost:8000/api/v1/saude). Startup creates missing tables, but does not migrate existing ones. Alembic migrations are included for schema changes.

### Frontend

```sh
cd frontend
npm ci
npm run dev
```

Open [localhost:5173](http://localhost:5173). Development requests default to `http://127.0.0.1:8000/api/v1`.

## Configuration

- `DATABASE_URL`: database connection string, read from the environment or `backend/.env`. Use the explicit SQLite URL above for local setup, or `postgresql+psycopg2://USER:PASSWORD@HOST:5432/DB_NAME` for PostgreSQL.
- `ENVIRONMENT`: when `DATABASE_URL` is absent, `development` selects `sqlite:///./test.db`; other values use the `DB_USER`, `DB_PASSWORD`, `DB_HOST`, `DB_PORT` and `DB_NAME` settings. That fallback selects the `psycopg` driver, while the included requirements install `psycopg2`; set `DATABASE_URL` explicitly.
- `APP_ENV`: label returned by the health endpoint and included in startup logs. Set it in the process environment; it does not select the database.
- `VITE_API_URL`: optional frontend override in `frontend/.env.local`, for example `VITE_API_URL=http://localhost:8000`. The frontend normalizes the API prefix to `/api/v1`. Production builds default to the same origin. Set this before building when hosting the frontend separately.

## API

| Method | Path | Behavior |
| --- | --- | --- |
| POST | `/api/v1/pagamentos/simular` | Calculate a receipt without saving |
| POST | `/api/v1/pagamentos/` | Calculate and save a payment |
| GET | `/api/v1/pagamentos/` | List saved payments, newest first |
| GET | `/api/v1/saude` | Return status, application version and environment label |

Example simulation:

```sh
curl -X POST http://localhost:8000/api/v1/pagamentos/simular \
  -H "Content-Type: application/json" \
  -d '{"opcao":3,"valor":100,"parcelas":3}'
```

Requests use `opcao`, `valor` and `parcelas`. Options 1 and 2 force one installment; options 3 and 4 require their respective installment ranges. See Swagger UI for response fields.

Creation accepts an optional `Idempotency-Key` header. Reusing a saved key returns the existing receipt, without comparing the new payload. The frontend does not send this header.

Listing accepts `limit` and `offset`, defaulting to 20 and 0. It returns a JSON array; the endpoint does not enforce a maximum limit.

Domain and request validation errors include `error.code`, `error.message` and `error.trace_id`; other errors can have different formats. Responses include an `X-Trace-Id` header.

## Tests and build

With the backend virtual environment active, run from `backend/`:

```sh
python -m pytest
```

The backend test setup uses SQLite in memory.

Run from `frontend/`:

```sh
npm test -- --run
npm run build
```

## Docker

The root Dockerfile builds the frontend and serves it through FastAPI on port 7860. Run from the repository root:

```sh
docker build -t loja-app .
docker volume create loja-data
docker run --rm -p 7860:7860 \
  -e DATABASE_URL=sqlite:////data/loja_app.db \
  -e APP_ENV=production \
  -v loja-data:/data loja-app
```

Open [localhost:7860](http://localhost:7860). The named volume keeps the SQLite database between container runs.

## Author and license

Argenis Mauricio López Salazar ([GitHub](https://github.com/Argenis1412)).

[MIT license](LICENSE.txt).
