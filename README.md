﻿# Loja App — Payment System

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

| Option | Mode | Rule |
|--------|------|------|
| 1 | Cash | 10% discount |
| 2 | Debit card | 5% discount |
| 3 | Installments (2-6x) | No interest |
| 4 | Installments (2-12x) | 10% interest |

Validation errors (invalid option, value ≤ 0, installments outside range) raise domain exceptions that the API converts to HTTP 400 responses.

For detailed business rules, see the [backend README](backend/README.md).

---

## Repository Structure

```
Loja_app/
├── backend/              # FastAPI REST API
│   ├── api/              # Endpoints and DTOs
│   ├── config/           # Pydantic settings
│   ├── domain/           # Business rules and entities
│   ├── infrastructure/   # Database and repositories
│   ├── services/         # Use cases
│   ├── tests/            # Unit and integration tests
│   └── README.md
│
├── frontend/             # React + TypeScript UI
│   ├── src/
│   │   ├── components/   # UI components
│   │   ├── services/     # API functions
│   │   ├── types/        # TypeScript interfaces
│   │   └── tests/        # Component tests
│   └── README.md
│
├── Makefile
├── README.md             # This file
├── run_backend.ps1
├── run_frontend.ps1
└── run_tests.ps1
```
---

## Getting Started

### Prerequisites

- Python 3.11+
- Node.js 18+ (npm >= 9)
- PostgreSQL (optional for development; tests use SQLite)

### Backend

```bash
cd backend

# Create and activate virtual environment
python -m venv venv
source venv/bin/activate  # Linux/Mac
# or .\venv\Scripts\activate  # Windows

# Install dependencies
pip install -r requirements.txt

# Run the server
uvicorn api.main:app --reload
```

API documentation available at `http://127.0.0.1:8000/docs`.

### Frontend

```bash
cd frontend

# Install dependencies
npm install

# Start development server
npm run dev
```

Application runs at `http://localhost:5173`.

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

- Backend API with four payment options
- Domain layer with unit-tested business rules
- Service layer with use case orchestration
- Repository pattern for persistence
- Frontend with form, confirmation, and receipt screens
- Component and integration tests

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