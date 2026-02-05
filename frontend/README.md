# Loja App — Frontend

![Node.js](https://img.shields.io/badge/Node-%3E%3D18-brightgreen?style=flat&logo=node.js&logoColor=white)
![React](https://img.shields.io/badge/React-19+-blue?style=flat&logo=react&logoColor=white)
![Vite](https://img.shields.io/badge/Vite-7+-646cff?style=flat&logo=vite)
![TypeScript](https://img.shields.io/badge/TypeScript-5+-3178c6?style=flat&logo=typescript&logoColor=white)
![Tailwind CSS](https://img.shields.io/badge/TailwindCSS-3+-06B6D4?style=flat&logo=tailwind-css)
![License](https://img.shields.io/badge/License-MIT-green)

This is the frontend component of Loja App, a learning laboratory focused on API consumption and React integration with a backend payment system.

---

## Purpose of the Frontend

This frontend serves as:

- A consumer of the backend REST API
- A demonstration of React + TypeScript integration
- A UI layer for the payment flow (form, confirmation, receipt)
- A testing surface for component behavior

The frontend does not implement business rules. All payment calculations happen in the backend. The frontend only displays data and collects user input.

This is not a scalable enterprise frontend architecture. It is intentionally minimal to keep focus on backend integration and API consumption.

---

## Technology Choices

| Technology | Minimum Version | Purpose |
|------------|-----------------|---------|
| React | 18+ | Component-based UI library |
| Vite | 7+ | Fast development server and build tool |
| TypeScript | 5+ | Static typing for reliability |
| Tailwind CSS | 3+ | Utility-first CSS framework |
| Vitest | 4+ | Unit and component testing |
| Testing Library | 16+ | React component testing utilities |

**Why these choices:**

- **React**: Industry standard, component model aligns with learning goals
- **Vite**: Fast HMR, native ESM support, simple configuration
- **TypeScript**: Catches errors early, documents API contracts
- **Tailwind CSS**: Rapid styling without custom CSS files, dark mode support via `class` strategy
- **Vitest**: Native Vite integration, fast execution, compatible with Testing Library

---

## Architecture Overview

The frontend uses a simple component-based architecture with no external state management library. No client-side caching or data synchronization layer is implemented. State is managed via React `useState` hooks in `App.tsx`.

### Application Flow

```
App.tsx (state machine)
    ├── form → PagamentoForm
    ├── confirmacao → ConfirmacaoPagamento
    └── recibo → Recibo
```

The app uses a `tela` state variable to switch between three screens:
1. **form**: User enters payment details
2. **confirmacao**: Shows simulation results before confirmation
3. **recibo**: Displays the receipt after successful payment

### API Communication

API calls are made directly using `fetch()` in `App.tsx` and in `services/api.ts`. There is no axios or centralized HTTP client.

---

## Backend Integration

### API Base URL

The backend URL is hardcoded in two locations:

- `App.tsx`: `http://localhost:8000/pagamentos/`
- `services/api.ts`: `http://127.0.0.1:8000/pagamentos/`

> **Note:** API URLs are intentionally hardcoded for learning simplicity. In production scenarios, environment variables should be used.

### Endpoints Consumed

| Endpoint | Method | Description |
|----------|--------|-------------|
| `/pagamentos/simular` | POST | Simulates payment without persistence |
| `/pagamentos/` | POST | Creates and persists a payment |
| `/pagamentos/` | GET | Lists all payments |

### Request Mapping

The frontend maps user-friendly method names to backend `opcao` integers:

| Frontend Method | Backend `opcao` |
|-----------------|-----------------|
| `avista` | 1 |
| `debito` | 2 |
| `parcelado_sem_juros` | 3 |
| `cartao_com_juros` | 4 |

This mapping is implemented in `converterMetodoParaOpcao()` in `PagamentoForm.tsx` and `metodoParaOpcao()` in `services/api.ts`.

### DTO Synchronization

The frontend depends on backend DTO stability. Breaking backend API changes will require TypeScript type updates in `types/api.ts`.

### Error Handling

Errors from the API are caught and displayed via the `ErrorBanner` component. The error message is extracted from the response `detail` field when available.

---

## Features Implemented

### Payment Form

- Value input with validation
- Payment method selection (radio buttons)
- Dynamic installment selector (appears for installment methods)
- Configurable installment limits per method

### Payment Simulation

- Calls `/pagamentos/simular` before confirmation
- Displays calculated total, installments, and rate information
- Shows rate type (discount/interest) based on backend response

### Payment Confirmation

- Shows payment summary with simulation data
- Loading state during API calls
- Back button to return to form

### Receipt Display

- Shows transaction ID, date, total, method, and installments
- Formatted date display
- Button to start a new payment

### Dark Mode Support

Dark mode styles exist but no runtime theme switcher is implemented. Tailwind is configured with `darkMode: 'class'` and components include dark mode variants (e.g., `dark:bg-zinc-900`).

---

## Intentional Simplifications

This frontend intentionally does not include:

| Feature | Reason |
|---------|--------|
| Router (React Router) | Single-page flow managed by state |
| State manager (Redux, Zustand) | useState is sufficient for this scope |
| HTTP client (axios) | Native fetch demonstrates basics |
| Environment variables for API URL | Learning simplicity |
| Authentication | Out of scope |
| Dark mode toggle | Styles prepared, toggle not implemented |
| Error boundaries | Basic error handling via state |
| Internationalization (i18n) | Single language (Portuguese) |

These are acknowledged as necessary in production but excluded to preserve focus and learning depth.

---

## Project Structure

```
frontend/
├── src/
│   ├── components/
│   │   ├── ConfirmacaoPagamento.tsx
│   │   ├── ErrorBanner.tsx
│   │   ├── PagamentoForm.tsx
│   │   ├── Recibo.tsx
│   │   └── ReciboPagamento.tsx
│   ├── hooks/
│   │   └── usePagamentos.ts
│   ├── pages/
│   │   ├── Home.tsx
│   │   └── StepPagamento.tsx
│   ├── services/
│   │   └── api.ts
│   ├── tests/
│   │   ├── setup.ts
│   │   ├── App.test.tsx
│   │   └── components/
│   │       ├── PagamentoForm.test.tsx
│   │       └── Recibo.test.tsx
│   ├── types/
│   │   └── api.ts
│   ├── assets/
│   ├── App.tsx
│   ├── App.css
│   ├── main.tsx
│   └── index.css
├── tailwind.config.js
├── postcss.config.js
├── vite.config.ts
├── tsconfig.json
├── package.json
└── README.md
```

### Key Files

| File | Description |
|------|-------------|
| `App.tsx` | Main component, manages screen state and API calls |
| `types/api.ts` | TypeScript interfaces for API request/response |
| `services/api.ts` | API functions (`criarPagamento`, `listarPagamentos`) |
| `hooks/usePagamentos.ts` | Custom hook for fetching payments list |
| `vite.config.ts` | Vite and Vitest configuration |
| `tailwind.config.js` | Tailwind CSS configuration with dark mode |

---

## Running the Frontend

### Requirements

- Node.js >= 18
- npm >= 9

### Install Dependencies

```bash
cd frontend
npm install
```

### Development Server

```bash
npm run dev
```

The app runs at `http://localhost:5173` by default.

### Build for Production

```bash
npm run build
```

Output is generated in the `dist/` folder.

### Preview Production Build

```bash
npm run preview
```

### Available Scripts

| Script | Description |
|--------|-------------|
| `npm run dev` | Start development server |
| `npm run build` | TypeScript check + production build |
| `npm run preview` | Preview production build |
| `npm run lint` | Run ESLint |
| `npm run lint:fix` | Run ESLint with auto-fix |
| `npm run format` | Format code with Prettier |
| `npm run format:check` | Check formatting |
| `npm run type-check` | TypeScript type checking |
| `npm run test` | Run tests with Vitest |
| `npm run test:ui` | Run tests with Vitest UI |
| `npm run test:coverage` | Run tests with coverage report |

---

## Testing

Tests are written with Vitest and Testing Library.

### Test Configuration

Configured in `vite.config.ts`:
- Environment: jsdom
- Setup file: `./src/tests/setup.ts`
- Global test timeout: 60000ms

### Test Files

| File | Description |
|------|-------------|
| `App.test.tsx` | Integration test for full payment flow |
| `PagamentoForm.test.tsx` | Unit tests for form component |
| `Recibo.test.tsx` | Unit tests for receipt component |

### Running Tests

```bash
npm run test
```

---

## Learning Goals

This frontend demonstrates:

- React component composition
- TypeScript integration with React
- API consumption with native `fetch`
- Simple state management with `useState`
- Form handling and validation
- Component testing with Vitest and Testing Library
- Tailwind CSS utility-first approach
- Dark mode CSS preparation

---

## Relation with Backend

This README is complementary to the backend README. The frontend consumes the API documented in the backend. The TypeScript types in `types/api.ts` should remain synchronized with the backend DTOs.

For business rules and API contract details, refer to the [backend README](../backend/README.md).

---

<!-- Author and License are declared in the repository root README -->