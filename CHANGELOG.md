# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to semantic versioning principles.

---

## [Unreleased]

### Added
- Comprehensive tests for ConfirmacaoPagamento component
- Visual display of adjusted last installment in UI
- Detailed installment breakdown in receipt and confirmation screens
- Coverage reports for frontend tests
- Database migration for `valor_ultima_parcela` column
- Documentation updates in all README files

### Changed
- **BREAKING**: Option 4 now requires 12-24 installments (previously 2-12)
  - This maintains clear separation between short-term (option 3: 2-6) and long-term (option 4: 12-24) installment plans
- Exact total calculation algorithm to adjust last installment
- Enhanced validation error messages for payment options
- Improved UI animations and visual feedback
- Updated tests to reflect new installment ranges

### Fixed
- Pytest asyncio configuration warning
- Rounding errors in installment calculations
- Total amount discrepancies when splitting into installments
- Uvicorn module path issue when running from backend directory

---

## [0.2.0] - 2026-02-14

### Added
- Exact total calculation with adjusted last installment
- `valor_ultima_parcela` field in database model
- `valor_ultima_parcela` field in API DTO responses
- Smart UI display for equal vs. adjusted installments
- Comprehensive frontend tests for new features

### Changed
- Option 4 installment range from 2-12 to 12-24
- Recibo entity to calculate and store adjusted last installment
- ConfirmacaoPagamento component to show installment details
- Recibo component to display installment breakdown
- PagamentoForm to enforce new installment limits

### Backend Changes
- Updated `Calculadora` class with new validation for option 4
- Enhanced `Recibo` entity with `valor_ultima_parcela` calculation
- Modified `PostgresReciboRepository` to persist adjusted last installment
- Updated `PagamentoResponse` DTO to include `valor_ultima_parcela`
- Added database migration for new column

### Frontend Changes
- Updated `PagamentoForm` with new installment limits (12-24 for option 4)
- Enhanced `ConfirmacaoPagamento` to display adjusted installments
- Improved `Recibo` component with detailed installment breakdown
- Updated type definitions for `valor_ultima_parcela` field
- Added new test cases for adjusted installments

---

## [0.1.0] - Initial Release

### Added
- FastAPI backend with payment calculation engine
- React + TypeScript frontend
- Four payment options:
  - Option 1: Cash with 10% discount
  - Option 2: Debit card with 5% discount
  - Option 3: Installments without interest (2-6x)
  - Option 4: Installments with interest (2-12x)
- Domain-driven design architecture
- Repository pattern with PostgreSQL
- Comprehensive test suite (backend and frontend)
- API documentation with OpenAPI/Swagger
- Dark mode support (prepared, not toggled)
- Tailwind CSS styling
- Database migrations with Alembic
- CI/CD workflows (prepared)

### Backend
- Domain layer with `Calculadora` class
- Service layer with `PagamentoService`
- Infrastructure layer with PostgreSQL repository
- API layer with FastAPI endpoints
- Exception handling and validation
- Unit and integration tests with pytest

### Frontend
- React components for payment flow
- TypeScript type definitions
- API integration with fetch
- Component tests with Vitest
- Responsive design with Tailwind CSS
- Form validation and error handling

---

## Legend

- **Added**: New features
- **Changed**: Changes in existing functionality
- **Deprecated**: Soon-to-be removed features
- **Removed**: Removed features
- **Fixed**: Bug fixes
- **Security**: Security improvements

---

## Notes

### Version 0.2.0 Highlights

The main focus of this release is ensuring exact total calculations when splitting payments into installments. Previously, rounding errors could cause the total to be slightly off (e.g., R$ 100.02 instead of R$ 100.00). Now, the system automatically adjusts the last installment to guarantee the total is exact.

**Example:**
- **Before**: 6x R$ 16.67 = R$ 100.02 ❌
- **After**: 5x R$ 16.67 + 1x R$ 16.65 = R$ 100.00 ✅

Additionally, option 4 now clearly differentiates itself from option 3 by requiring a minimum of 12 installments, making it suitable for long-term financing with interest.

---

**For detailed instructions on running the project, see the main [README.md](README.md).**
