# Contributing to Loja App

Thank you for your interest in contributing to Loja App! This document provides guidelines and instructions for setting up the development environment and running the project.

---

## Table of Contents

- [Getting Started](#getting-started)
- [Development Setup](#development-setup)
- [Running the Project](#running-the-project)
- [Running Tests](#running-tests)
- [Code Style](#code-style)
- [Database Migrations](#database-migrations)
- [Common Issues](#common-issues)

---

## Getting Started

### Prerequisites

Before you begin, ensure you have the following installed:

- **Python 3.11+** (for backend)
- **Node.js 18+** with npm 9+ (for frontend)
- **PostgreSQL** (optional for development; tests use SQLite)
- **Git** (for version control)

### Clone the Repository

```bash
# Using HTTPS
git clone https://github.com/Argenis1412/Loja_app.git

# Or using SSH
git clone git@github.com:Argenis1412/Loja_app.git

# Or using GitHub CLI
gh repo clone Argenis1412/Loja_app

cd Loja_app
```

---

## Development Setup

### Quick Setup (Windows)

Use the provided PowerShell script to set up everything automatically:

```powershell
.\loja_cli.ps1 setup
```

This script will:
1. Create Python virtual environment
2. Install backend dependencies
3. Install frontend dependencies

### Manual Setup

#### Backend Setup

```bash
cd backend

# Create virtual environment
python -m venv venv

# Activate virtual environment
# Windows:
.\venv\Scripts\activate
# Linux/Mac:
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Run database migrations
alembic upgrade head
```

#### Frontend Setup

```bash
cd frontend

# Install dependencies
npm install
```

---

## Running the Project

### Using PowerShell Scripts (Windows)

The easiest way to run the project is using the provided scripts:

```powershell
# Terminal 1: Start backend
.\loja_cli.ps1 backend

# Terminal 2: Start frontend
.\loja_cli.ps1 frontend
```

### Manual Execution

#### Start Backend

```bash
cd backend

# Activate virtual environment first
.\venv\Scripts\activate  # Windows
# or
source venv/bin/activate  # Linux/Mac

# Run the server
uvicorn api.main:app --reload
```

✅ Backend runs at: `http://127.0.0.1:8000`  
✅ API docs at: `http://127.0.0.1:8000/docs`

#### Start Frontend

```bash
cd frontend

# Start development server
npm run dev
```

✅ Frontend runs at: `http://localhost:5173`

---

## Running Tests

### All Tests (Backend + Frontend)

```powershell
.\loja_cli.ps1 test
```

### Backend Tests

```bash
cd backend

# Activate virtual environment
.\venv\Scripts\activate  # Windows

# Run all tests
pytest -v

# Run tests with coverage
pytest -v --cov=. --cov-report=html

# Open coverage report
# Windows: start htmlcov/index.html
# Linux/Mac: open htmlcov/index.html
```

**Expected Results:**
- All 20+ tests should pass
- Coverage should be >95%

### Frontend Tests

```bash
cd frontend

# Run tests
npm test

# Run tests with UI
npm run test:ui

# Run tests with coverage
npm run test:coverage
```

**Expected Results:**
- All component tests should pass
- Coverage reports in `coverage/` directory

---

## Code Style

### Backend (Python)

We follow PEP 8 with some customizations:

```bash
# Format code (if black is installed)
black .

# Sort imports (if isort is installed)
isort .

# Type checking (if mypy is installed)
mypy .
```

**Key conventions:**
- 88 character line length (black default)
- Type hints encouraged but not required
- Docstrings for public functions
- Domain exceptions over generic exceptions

### Frontend (TypeScript)

We use ESLint and Prettier:

```bash
# Lint code
npm run lint

# Fix linting issues
npm run lint:fix

# Format code
npm run format

# Check formatting
npm run format:check

# Type check
npm run type-check
```

**Key conventions:**
- Use TypeScript strict mode
- Props interfaces for all components
- No `any` types except when necessary
- Use functional components with hooks

---

## Database Migrations

### Creating a New Migration

When you modify database models:

```bash
cd backend

# Activate virtual environment
.\venv\Scripts\activate

# Create migration (auto-generate from model changes)
alembic revision --autogenerate -m "description of change"

# Review the generated migration file in alembic/versions/

# Apply migration
alembic upgrade head
```

### Migration Commands

```bash
# Show current migration status
alembic current

# Show migration history
alembic history

# Upgrade to latest
alembic upgrade head

# Downgrade one version
alembic downgrade -1

# Downgrade to specific version
alembic downgrade <revision_id>
```

---

## Common Issues

### Issue: `ModuleNotFoundError: No module named 'backend'`

**Solution:** When running uvicorn from inside the `backend` directory, don't use the `backend.` prefix:

```bash
# ❌ Wrong (when inside backend/)
uvicorn backend.api.main:app --reload

# ✅ Correct (when inside backend/)
uvicorn api.main:app --reload

# ✅ Also correct (when at project root)
uvicorn backend.api.main:app --reload
```

### Issue: `pytest asyncio warning`

**Solution:** Already fixed in `pyproject.toml`:

```toml
[tool.pytest.ini_options]
asyncio_default_fixture_loop_scope = "function"
```

### Issue: Frontend can't connect to backend

**Solutions:**
1. Ensure backend is running at `http://127.0.0.1:8000`
2. Check CORS settings in `backend/api/main.py`
3. Verify API URL in `frontend/src/App.tsx` and `frontend/src/services/api.ts`

### Issue: Database errors

**Solutions:**
1. Run migrations: `alembic upgrade head`
2. Delete `loja.db` file and re-run migrations (development only)
3. Check database connection string in `backend/config/settings.py`

### Issue: Tests failing after changes

**Solutions:**
1. Update test assertions to match new behavior
2. Run tests in isolation: `pytest tests/path/to/test.py -v`
3. Check for leftover database state: delete `loja.db` between test runs

---

## Project Structure Reference

```
Loja_app/
├── backend/
│   ├── api/                 # REST API endpoints
│   ├── domain/              # Business logic (framework-agnostic)
│   ├── infrastructure/      # Database and persistence
│   ├── services/            # Use case orchestration
│   ├── tests/               # Test suite
│   └── alembic/             # Database migrations
│
├── frontend/
│   ├── src/
│   │   ├── components/      # React components
│   │   ├── services/        # API client functions
│   │   ├── types/           # TypeScript type definitions
│   │   └── tests/           # Component tests
│   └── coverage/            # Test coverage reports
│
├── loja_cli.ps1             # Unified management script
└── CHANGELOG.md             # Version history
```

---

## Questions or Problems?

If you encounter any issues:

1. Check the [README.md](README.md) for general documentation
2. Check the [Backend README](backend/README.md) for API details
3. Check the [Frontend README](frontend/README.md) for UI details
4. Check the [CHANGELOG.md](CHANGELOG.md) for recent changes
5. Open an issue on GitHub with detailed description

---

## License

By contributing to Loja App, you agree that your contributions will be licensed under the MIT License.

---

**Happy coding!** 🚀
