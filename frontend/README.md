# Loja App — Frontend

![CI](https://github.com/Argenis1412/Loja_app/actions/workflows/frontend-ci.yml/badge.svg)
![React](https://img.shields.io/badge/React-19+-blue?style=flat&logo=react&logoColor=white)
![TypeScript](https://img.shields.io/badge/TypeScript-5+-3178c6?style=flat&logo=typescript&logoColor=white)
![Tailwind](https://img.shields.io/badge/TailwindCSS-3+-06B6D4?style=flat&logo=tailwind-css)

This is the frontend component of Loja App, a React-based UI designed to interact with the Payments API. It focuses on a clean payment flow and explicit feedback for the user.

---

## 🎨 UI & Features

- **Technologies**: React, Vite, TypeScript, Tailwind CSS.
- **Payment Flow**: Multi-step process (Form → Confirmation → Receipt).
- **Exact Display**: Intelligent display of installments, showing adjusted last installment values.
- **Dark Mode**: Prepared with Tailwind CSS variants for professional aesthetics.

---

## 🚀 Getting Started

### Prerequisites
- Node.js 18+
- npm 9+

### Setup
1.  **Install**: `npm install`
2.  **Run**: `npm run dev`
3.  **URL**: `http://localhost:5173`

---

## 📂 Project Structure

```text
frontend/
├── src/
│   ├── components/ # Screen-specific UI components
│   ├── services/   # API communication (fetch)
│   ├── types/      # TypeScript DTOs (aligned with Backend)
│   ├── tests/      # Vitest component & integration tests
│   └── App.tsx     # Main state machine & routing
```

---

## 🧪 Testing

The frontend uses **Vitest** and **React Testing Library** to ensure reliable user flows.

```bash
# Run all tests
npm test

# Generate coverage report
npm run test:coverage
```

---

## 🔌 API Integration

The frontend consumes the `/pagamentos` endpoints. The API URL is centralized in `src/config/api.ts` and defaults to production:

- **Development**: Set `VITE_API_URL` in `.env.local` to point to `localhost:8000`.

---

## 📄 License
Licensed under the **MIT License**.