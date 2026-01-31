# 🛍️ Loja App — Frontend (React + Vite + TypeScript)

![Node.js](https://img.shields.io/badge/Node-%3E%3D18-brightgreen?style=flat&logo=node.js&logoColor=white)
![React](https://img.shields.io/badge/React-%3E=18-blue?style=flat&logo=react&logoColor=white)
![Vite](https://img.shields.io/badge/Vite-^7.2.4-646cff?style=flat&logo=vite)
![TypeScript](https://img.shields.io/badge/TypeScript-5.9.3-3178c6?style=flat&logo=typescript&logoColor=white)
![Tailwind CSS](https://img.shields.io/badge/TailwindCSS-3.4.19-06B6D4?style=flat&logo=tailwind-css)
![License](https://img.shields.io/badge/License-MIT-green)

This frontend is a thin, performance-focused consumer of the Payments API. It demonstrates clean frontend architecture, TypeScript typing, and correct API consumption — it intentionally does not duplicate business logic.

> **Note:** React 19 is currently used, but the codebase relies only on React 18-compatible APIs.

## 🎯 Purpose

The frontend exists to consume the backend-first Payments API and present a simple, well-typed UI. All calculations and business rules are performed by the backend.

## 🧰 Tech Stack

- React 19 (see `package.json`)
- Vite (dev server and build)
- TypeScript 5.9 (strict)
- Tailwind CSS
- Fetch API (no extra HTTP wrappers)

## 📁 Project Structure

Simplified developer view (folders shown; only key files listed):

```
frontend/
├── public/
├── src/
|   ├── assets/
|   ├── components/
|   |   ├── ConfirmacaoPagamento.tsx
|   |   ├── PagamentoForm.tsx
|   |   └── Recibo.tsx
|   ├── hooks/                  # custom hooks for UI state/orchestration only
|   ├── tests/                  # unit and integration tests
|   ├── pages/
|   |   ├── Home.tsx
|   |   └── StepPagamento.tsx
|   ├── services/
|   |   └── api.ts              # central API client and mapping
|   ├── types/
|   |   ├── api.ts
|   |   └── fluxoPagamento.ts
|   ├── App.tsx
|   └── main.tsx
├── index.html
├── vite.config.ts
├── package.json
├── tsconfig.json
└── tailwind.config.js
```

> **Note:** Custom hooks are limited to UI state and orchestration, never business logic.

## 🔌 API Integration

All HTTP calls live in `src/services` (see `frontend/src/services/api.ts`). The frontend sends explicit payloads and handles errors defensively.

Request example:

```json
{
  "opcao": 3,
  "valor": 100.00,
  "parcelas": 6
}
```

Expected response example:

```json
{
  "total": 100.00,
  "valor_parcela": 16.67,
  "parcelas": 6,
  "taxas": "0% (Sem juros)",
  "status": "aprovado"
}
```

### `opcao` mapping

The frontend converts user-facing `metodo` values into the internal `opcao` integer before calling the API.

| `opcao` | Frontend `metodo` | Meaning |
|--------:|-------------------|---------|
| 1 | `avista` | Cash / À vista (10% discount) |
| 2 | `debito` | Debit card (5% discount) |
| 3 | `parcelado_sem_juros` | Short installments (2–6x, no interest) |
| 4 | `cartao_com_juros` | Long installments (12–24x, fixed increase) |

> The `opcao` mapping mirrors the backend contract and must be updated only when the API changes.

## 🚀 Running the Frontend

### Requirements

- Node.js 18+

### Install & Run
```bash
cd frontend
npm install
npm run dev
```

## ▶️ Execution

To start the development server:
```bash
npm run dev
```

The application will be available at `http://localhost:5173`.

## 🧪 Automated Testing

The project has a robust test suite configured with **Vitest**.

To run all tests:
```bash
npm test
```

### Test Coverage

Tests are located in `src/tests` and cover:

- **Unit Tests**: Isolated verification of components like `PagamentoForm` and `Recibo`.
- **Integration Tests**: Complete user flow testing in `App.test.tsx`, simulating everything from form filling, API value simulation, to confirmation and receipt display.

## 📁 Structure

- `src/components`: Reusable UI components.
- `src/tests`: Test files and configuration (`setup.ts`).
- `src/types`: Shared TypeScript type definitions.