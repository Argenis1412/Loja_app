# 🧪 Loja App — Payments Architecture Lab

## 📌 Overview

**Loja App** is a technical learning laboratory focused on designing and evolving a realistic payment system. Built with clear separation between backend and frontend, it follows clean architecture principles, explicit business rules, and an incremental user experience.

**This project is not a full e-commerce platform.** Its purpose is to serve as a controlled environment to:

- Model real-world payment rules
- Practice clean architecture and separation of concerns
- Integrate a frontend with an API-first backend
- Explore validation, error handling, and receipts
- Support technical discussions and interviews

**This repository prioritizes learning clarity over completeness.**

---

## 🎯 Learning Goals

- Design an API-first payment system
- Isolate business rules from frameworks
- Work with PostgreSQL and schema migrations
- Integrate React + TypeScript with a real backend
- Handle validation, errors, and confirmations explicitly

---

## 🧱 Repository Structure

```
.
├── backend/        # REST API (FastAPI + Clean Architecture)
│   ├── api/
│   ├── config/
│   ├── domain/
│   ├── infrastructure/
│   ├── tests/
│   └── README.md
│
├── frontend/       # Web app (React + Vite + TypeScript)
│   ├── src/
│   ├── public/
│   └── README.md
│
├── README.md       # Project overview (this file)
├── requirements.txt
└── run.ps1 / run-tests.ps1
```

Each main folder contains its own **README**, explaining:

- Internal structure and organization
- Design decisions and architectural patterns
- Component responsibilities
- Trade-offs and rationale

---

## 🧮 Business Rules (Domain)

The system simulates multiple payment modes with **explicit, testable rules**:

| Payment Mode | Condition | Applied Rule |
|---------------------|---------------------|---------------------|
| Cash (upfront) | Immediate payment | **10% discount** |
| Card (upfront) | Immediate payment | **5% discount** |
| Short installments | 2x to 6x | **0% interest** |
| Long installments | 12x to 24x | **Fixed 10% increase** |

### ⚠️ Important Constraints

- Installment counts **outside allowed ranges** (e.g., 7x, 11x, 25x) must raise a **domain validation error**, not a technical error
- All business logic is centralized in the domain layer
- Rules are framework-agnostic and fully unit-tested

---

## 🧠 Project Philosophy

This repository intentionally prioritizes:

✅ **Readable code** over clever code  
✅ **Explicit business rules** over implicit behavior  
✅ **Minimal dependencies** to reduce complexity  
✅ **Clear error handling** with meaningful messages  
✅ **Strict separation of concerns** (domain, application, infrastructure)  
✅ **Practical, explainable learning** over theoretical abstraction

### Why This Approach?

Everything here is designed so you can **confidently answer** questions like:

- *"Why did you design it this way?"*
- *"Where are the business rules defined?"*
- *"What would change for a production system?"*
- *"How do you handle errors and edge cases?"*
- *"What is intentionally out of scope?"*

---

## 🗄️ Persistence (PostgreSQL)

The backend uses **PostgreSQL** with **Alembic migrations** to:

- Simulate a real production environment
- Track schema evolution over time
- Support reliable automated tests
- Avoid unrealistic in-memory mocks

### Database Setup

Two databases are used:

- **loja_db** → Development environment
- **loja_test_db** → Automated testing (isolated)

Full setup details and migration instructions are in the **backend README**.

---

## 🌐 High-Level Architecture

```
┌─────────────────────────┐
│  Frontend (React + TS)  │
│  - User Interface       │
│  - API Integration      │
└───────────┬─────────────┘
            │
            │ HTTP / JSON
            ▼
┌─────────────────────────┐
│   REST API (FastAPI)    │
│  - Route Handlers       │
│  - Request Validation   │
└───────────┬─────────────┘
            │
            ▼
┌─────────────────────────┐
│ Domain & Business Rules │
│  - Payment Calculation  │
│  - Validation Logic     │
└───────────┬─────────────┘
            │
            ▼
┌─────────────────────────┐
│   PostgreSQL Database   │
│  - Transactions         │
│  - Persistence          │
└─────────────────────────┘
```

### Key Principles

- ✅ The **frontend does not know business rules** — it only displays and collects data
- ✅ The **backend does not depend on the frontend** — it's API-first
- ✅ The **domain layer is pure** — no framework dependencies

---

## 🚫 Non-Goals (Explicitly Out of Scope)

This project intentionally **does not** aim to be:

❌ A production payment gateway  
❌ A complete e-commerce system  
❌ A security-hardened financial product  
❌ A UX/UI showcase  
❌ A microservices architecture

These topics are acknowledged but excluded to preserve **focus and learning depth**.

---

## 🚧 Current Project Status

| Area | Status |
|-------------------------------|-----------------|
| Backend (rules + API) | ✅ Stable |
| Persistence (Postgres + Alembic) | ✅ Stable |
| Automated tests | ✅ Stable |
| Frontend (React flow) | ✅ Functional |
| UX improvements | 🔄 Ongoing |

---

## 🚀 Getting Started

### Prerequisites

- **Python 3.11+** — backend dependencies are listed in `requirements.txt`
- **Node.js 18+** (and npm >= 9) — frontend engines are declared in `frontend/package.json`
- **PostgreSQL 14+**
- Docker (optional, for containerized setup)

### Quick Start

1. **Clone the repository**

```bash
git clone https://github.com/argenis972/Loja_app.git
cd Loja_app
```

2. **Backend setup**

```bash
cd backend
# Follow instructions in backend/README.md
```

3. **Frontend setup**

```bash
cd frontend
# Follow instructions in frontend/README.md
```

---

## 🧪 Running Tests

```bash
# Backend tests
cd backend
pytest
```

---

## 📚 Documentation

- **[Backend README](backend/README.md)** — API design, domain model, database setup
- **[Frontend README](frontend/README.md)** — Component structure, state management, API integration

---

## 🤝 Contributing

This is a learning project, but contributions are welcome! Please:

1. Fork the repository
2. Create a feature branch
3. Follow the existing code style
4. Add tests for new features
5. Submit a pull request

---

## 👤 Author

**Argenis López**

- 💼 [LinkedIn](https://www.linkedin.com/in/argenis972/)
- 💻 [GitHub](https://github.com/argenis972)
- 📧 [Email](mailto:argenislopez28708256@gmail.com)

---

## 📜 License

**MIT License** — Feel free to study, adapt, and evolve this project for your own learning.

---

## 🙏 Acknowledgments

This project was built as a practical exercise in:

- Clean Architecture (Robert C. Martin)
- Domain-Driven Design principles
- API-first development
- Test-Driven Development

---

## 📝 Final Note

**This repository is best evaluated as a thinking exercise:**

- How responsibilities are separated
- How rules are modeled
- How interfaces are respected

**Not by feature count or visual polish.**

---

**⭐ If this project helps your learning journey, consider giving it a star!**