# Loja App — Payment System

[![Backend CI](https://github.com/argenis972/Loja_app/actions/workflows/backend-ci.yml/badge.svg)](https://github.com/argenis972/Loja_app/actions/workflows/backend-ci.yml)
[![Frontend CI](https://github.com/argenis972/Loja_app/actions/workflows/frontend-ci.yml/badge.svg)](https://github.com/argenis972/Loja_app/actions/workflows/frontend-ci.yml)
[![Python 3.11+](https://img.shields.io/badge/python-3.11+-blue.svg)](https://www.python.org/downloads/)
[![TypeScript](https://img.shields.io/badge/typescript-5.0+-blue.svg)](https://www.typescriptlang.org/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE.txt)

---

## Project Overview

**Loja App** is a learning laboratory for backend-first architecture and payment logic. The project demonstrates how to design a payment system with explicit business rules, clear separation of concerns, and a frontend that acts purely as an API consumer.

### Educational Goals

- Understand how to isolate business rules from frameworks
- Practice layered architecture with domain, service, and infrastructure separation
- Integrate a React frontend with a FastAPI backend via REST
- Handle validation, error propagation, and receipts explicitly
- Write testable domain logic independent of persistence

### Backend-First Philosophy

The backend is the source of truth. All calculations, validations, and business decisions happen in the backend domain layer. The frontend collects input and displays results. It does not calculate totals, apply discounts, or validate payment rules.

---

## What This Project Is NOT

- **Not a SaaS product** — This is a learning exercise, not a deployable service.
- **Not production-ready** — No authentication, rate limiting, or security hardening.
- **Not an enterprise architecture** — No microservices, no message queues, no complex infrastructure.
- **Not feature-complete** — Intentionally minimal to preserve focus.
- **Not a UX showcase** — The frontend is functional, not polished.

---

## Technology Rationale

### Backend

| Technology | Purpose |
|------------|---------|
| **FastAPI** | Lightweight Python framework with automatic OpenAPI documentation and Pydantic integration. |
| **PostgreSQL** | Relational database for realistic persistence. Integration tests use SQLite in-memory databases to avoid requiring a running PostgreSQL instance. |
| **SQLAlchemy** | ORM with repository pattern for domain-infrastructure separation. |
| **Pydantic** | Request/response validation and settings management. |
| **Pytest** | Unit and integration testing with coverage reporting. |

### Frontend

| Technology | Purpose |
|------------|---------|
| **React** | Component-based UI for building the payment flow screens. |
| **TypeScript** | Static typing to catch errors early and document API contracts. |
| **Vite** | Fast development server with native ESM support. |
| **Tailwind CSS** | Utility-first styling without custom CSS files. |
| **Vitest** | Test runner with native Vite integration. |

---

## High-Level Architecture

```
┌─────────────────────────┐
│  Frontend (React + TS)  │
│  - Collects user input  │
│  - Displays API results │
│  - No business logic    │
└───────────┬─────────────┘
            │
            │ HTTP / JSON
            ▼
┌─────────────────────────┐
│   REST API (FastAPI)    │
│  - Route handlers       │
│  - Request validation   │
│  - Exception handling   │
└───────────┬─────────────┘
            │
            ▼
┌─────────────────────────┐
│   Service Layer         │
│  - Use case orchestration│
│  - Delegates business   │
│    rules to domain layer│
└───────────┬─────────────┘
            │
            ▼
┌─────────────────────────┐
│   Domain Layer          │
│  - Calculadora class    │
│  - Payment rules        │
│  - Domain exceptions    │
└───────────┬─────────────┘
            │
            ▼
┌─────────────────────────┐
│   PostgreSQL Database   │
│  - Receipt persistence  │
└─────────────────────────┘
```

### Backend Responsibilities

- **Business rules**: All payment calculations live in `domain/calculadora.py`.
- **Validation**: Domain exceptions enforce constraints (value > 0, valid option, installment ranges).
- **Calculations**: Discounts, interest, and installment amounts are computed server-side.
- **Persistence**: Receipts are stored via the repository pattern.
- **REST API**: Endpoints for creating, simulating, and listing payments.

### Frontend Responsibilities

- **API consumption**: Calls backend endpoints using native `fetch`.
- **Form flow**: Three screens — form, confirmation, receipt.
- **Display logic**: Renders backend responses without transformation.
- **No business rules**: Does not calculate totals or validate payment constraints.

---

## Business Domain Summary

The system models four payment options with explicit rules:

| Option | Mode | Installments | Rule |
|--------|------|--------------|------|
| 1 | Cash | 1x | 10% discount |
| 2 | Debit card | 1x | 5% discount |
| 3 | Credit card | 2-6x | No interest |
| 4 | Credit card | 12-24x | 10% interest |

**Key Features:**
- **Exact Total Calculation**: When payments are split into installments, the system automatically adjusts the last installment to ensure the total is exact (no rounding errors).
- **Smart Validation**: Domain exceptions ensure valid values (> 0) and proper installment ranges.
- **Backend-First**: All calculations happen server-side; frontend displays results.

Validation errors (invalid option, value ≤ 0, installments outside range) raise domain exceptions that the API converts to HTTP 400 responses.

For detailed business rules, see the [backend README](backend/README.md).

---

## Repository Structure

```
Loja_app/
├── backend/              # FastAPI REST API
│   ├── alembic/          # Database migrations
│   ├── api/              # Endpoints and DTOs
│   │   ├── dtos/         # Request/Response models
│   │   ├── deps.py       # Dependency injection
│   │   ├── main.py       # FastAPI app
│   │   └── pagamentos_api.py  # Payment routes
│   ├── config/           # Pydantic settings
│   │   ├── settings.py   # App configuration
│   │   └── taxas.json    # Tax rates config
│   ├── domain/           # Business rules and entities
│   │   ├── calculadora.py      # Payment calculator
│   │   ├── exceptions.py       # Domain exceptions
│   │   ├── recibo.py           # Receipt entity
│   │   └── recibo_repository.py # Repository interface
│   ├── infrastructure/   # Database and repositories
│   │   ├── db/           # Database models and mappers
│   │   ├── repositories/ # Repository implementations
│   │   └── database.py   # Database connection
│   ├── services/         # Use cases
│   │   └── pagamento_service.py
│   ├── tests/            # Unit and integration tests
│   │   ├── unit/         # Unit tests
│   │   └── services/     # Service tests
│   ├── requirements.txt  # Python dependencies
│   ├── pyproject.toml    # Python project config
│   └── README.md         # Backend documentation
│
├── frontend/             # React + TypeScript UI
│   ├── public/           # Static assets
│   ├── src/
│   │   ├── assets/       # Images and resources
│   │   ├── components/   # UI components
│   │   │   ├── PagamentoForm.tsx
│   │   │   ├── ConfirmacaoPagamento.tsx
│   │   │   └── Recibo.tsx
│   │   ├── services/     # API functions
│   │   │   └── pagamentoService.ts
│   │   ├── types/        # TypeScript interfaces
│   │   │   └── api.ts
│   │   ├── tests/        # Component tests
│   │   ├── App.tsx       # Main app component
│   │   └── main.tsx      # App entry point
│   ├── package.json      # Node dependencies
│   ├── vite.config.ts    # Vite configuration
│   ├── tailwind.config.js # Tailwind CSS config
│   └── README.md         # Frontend documentation
│
├── .github/              # GitHub Actions CI/CD
│   └── workflows/
│       ├── backend-ci.yml
│       └── frontend-ci.yml
├── CHANGELOG.md          # Version history
├── CONTRIBUTING.md       # Contribution guidelines
├── LICENSE.txt           # MIT License
├── Makefile              # Build automation
├── README.md             # This file
├── run_backend.ps1       # Start backend (Windows)
├── run_frontend.ps1      # Start frontend (Windows)
├── run_tests.ps1         # Run all tests (Windows)
├── setup.ps1             # Initial setup (Windows)
└── verificar_backend.ps1 # Backend verification script
```
---

## Getting Started

### Clone the Repository

First, clone the repository to your local machine:

```bash
git clone https://github.com/argenis972/Loja_app.git
cd Loja_app
```

### Prerequisites

- **Python 3.11+** (for backend)
- **Node.js 18+** with npm 9+ (for frontend)
- **PostgreSQL** (optional; tests use SQLite in-memory database)

### Quick Start (Windows)

The project includes PowerShell scripts for easy setup:

```powershell
# 1. Setup environment (creates venv, installs dependencies)
.\setup.ps1

# 2. Run backend (starts FastAPI server)
.\run_backend.ps1

# 3. Run frontend (in a new terminal)
.\run_frontend.ps1

# 4. Run all tests (backend + frontend)
.\run_tests.ps1
```

### Manual Setup

#### Backend

```bash
cd backend

# Create and activate virtual environment
python -m venv venv

# Activate (Windows)
.\venv\Scripts\activate

# Activate (Linux/Mac)
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Run database migrations
alembic upgrade head

# Run tests
pytest -v --cov=. --cov-report=html

# Start the server
uvicorn api.main:app --reload
```

✅ API documentation available at `http://127.0.0.1:8000/docs`  
✅ Interactive API testing at `http://127.0.0.1:8000/redoc`

#### Frontend

```bash
cd frontend

# Install dependencies
npm install

# Run tests
npm test

# Start development server
npm run dev
```

✅ Application runs at `http://localhost:5173`

### Testing

**Backend:**
```bash
cd backend
pytest -v                    # Run all tests
pytest --cov=.               # With coverage
pytest --cov-report=html     # Generate HTML coverage report
```

**Frontend:**
```bash
cd frontend
npm test                     # Run tests with Vitest
npm run test:ui              # Interactive test UI
npm run test:coverage        # Generate coverage report
```

### Database Migrations

When you make changes to database models:

```bash
cd backend

# Create a new migration
alembic revision --autogenerate -m "description of change"

# Apply migrations
alembic upgrade head

# Rollback last migration
alembic downgrade -1
```

---

## Deployment on Render

The project is configured for easy deployment on Render with PostgreSQL.

### Quick Backend Deployment

#### Prerequisites
- Account on [Render](https://render.com)
- Project repository on GitHub

#### Steps

1. **Create PostgreSQL Database on Render:**
   - Dashboard → New + → PostgreSQL
   - Name: `loja-db`
   - Region: choose closest region
   - Plan: Free or Starter
   - Copy the **Internal Database URL**

2. **Create Web Service on Render:**
   - Dashboard → New + → Web Service
   - Connect GitHub repository
   - Configuration:
     - **Root Directory**: `backend`
     - **Build Command**: `./build.sh`
     - **Start Command**: `gunicorn -w 4 -k uvicorn.workers.UvicornWorker api.main:app --bind 0.0.0.0:$PORT`

3. **Environment Variables:**
   ```
   DATABASE_URL=<Internal Database URL from step 1>
   ENVIRONMENT=production
   API_HOST=0.0.0.0
   ```

4. **Deploy:**
   - Click "Create Web Service"
   - Wait 2-5 minutes
   - Your API will be at: `https://your-service.onrender.com`

5. **Verify:**
   - Health: `https://your-service.onrender.com/saude`
   - Docs: `https://your-service.onrender.com/docs`

### Frontend Deployment

For the frontend (React + Vite):

**Option 1: Static Site on Render**
1. New + → Static Site
2. Build Command: `cd frontend && npm install && npm run build`
3. Publish Directory: `frontend/dist`
4. Environment variable:
   ```
   VITE_API_URL=https://your-backend.onrender.com
   ```

**Option 2: Vercel or Netlify**
- Deploy frontend on Vercel/Netlify
- Configure `VITE_API_URL` pointing to backend on Render

### Auto-Deployment

Render automatically redeploys when you push to the main branch:
```bash
git push origin main
```

📖 **Full documentation**: See [Backend README - Deployment Section](backend/README.md#deployment-on-render)

---

## Documentation Links

- **[Backend README](backend/README.md)** — API endpoints, domain rules, persistence layer, testing strategy.
- **[Frontend README](frontend/README.md)** — Component structure, API integration, intentional simplifications.

---

## Project Philosophy

### Clarity Over Complexity

Code is written to be read and understood. Clever abstractions are avoided in favor of explicit implementations.

### Backend as Source of Truth

The frontend never calculates business values. It sends input to the backend and displays the response.

### Intentional Minimal Frontend

No routing library, no state management library, no HTTP client library. These omissions are deliberate to demonstrate fundamentals.

### Testable Domain Logic

Domain layer contains no framework dependencies. Business rules are isolated in plain Python classes. They can be tested without spinning up a server or database.

---

## Current Status

This is an evolving learning laboratory. The current implementation covers:

- ✅ Backend API with four payment options
- ✅ Domain layer with unit-tested business rules
- ✅ Service layer with use case orchestration
- ✅ Repository pattern for persistence with PostgreSQL
- ✅ Frontend with form, confirmation, and receipt screens
- ✅ Component and integration tests with coverage reporting
- ✅ Database migrations with Alembic
- ✅ Exact total calculation with adjusted last installment
- ✅ Modern UI with Tailwind CSS and dark mode support
- ✅ Comprehensive error handling and validation

### Recent Updates (February 2026)

**Backend:**
- Updated Option 4 to support 12-24 installments (previously 2-12)
- Implemented exact total calculation by adjusting the last installment
- Added `valor_ultima_parcela` field to database model and DTOs
- Fixed pytest asyncio configuration warnings
- Enhanced validation messages for payment options

**Frontend:**
- Updated installment selector for Option 4 (12-24 installments)
- Added visual display for adjusted last installment
- Improved confirmation screen with detailed installment breakdown
- Added comprehensive tests for new features
- Enhanced UI with better visual feedback and animations

The project is stable for learning purposes but not intended for production deployment.

---

## Author

**Argenis López**

- [LinkedIn](https://www.linkedin.com/in/argenis972/)
- [GitHub](https://github.com/argenis972)
- [Email](mailto:argenislopez28708256@gmail.com)

---

## License

MIT License — See [LICENSE.txt](LICENSE.txt)

---

**⭐ If this project helps your learning journey, consider giving it a star!**