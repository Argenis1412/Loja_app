# Deployment Guide — Loja App

This document explains how to deploy the entire project (Frontend and Backend) using **Docker** or **Serverless** options, utilizing a cloud PostgreSQL database.

## Step 1: Database

Cloud providers usually don't persist local files (like SQLite's `test.db`), so we will use a cloud PostgreSQL database.

1.  Create a project on [Supabase](https://supabase.com/) or [Neon.tech](https://neon.tech).
2.  Get your **Connection String** (starting with `postgresql://`).
3.  **Save this URL** as `DATABASE_URL`.

---

## Step 2: Deployment Options

### Option A: Unified Docker Deployment (Recommended)

This project includes a multi-stage `Dockerfile` that builds the React frontend and serves it via the FastAPI backend.

#### 1. Hugging Face Spaces (Free & Reliable)
Hugging Face Spaces is excellent for persistent free hosting.
- **SDK**: Docker (Blank template).
- **Variables**: Add `DATABASE_URL` in Settings.

#### 2. Render (Free Tier)
Render offers a very easy setup for Docker services.
- **Source**: Connect GitHub.
- **Runtime**: Docker.
- **Plan**: Free.
- **Variables**: Add `DATABASE_URL`.
*Note: Spins down after 15m of inactivity.*

#### 3. Railway (Paid/Trial)
High performance and great DX.
- **Source**: Connect GitHub.
- **Variables**: Add `DATABASE_URL`.
- Railway automatically detects the root `Dockerfile`.

---

### Option B: Vercel (Frontend & Serverless)

1.  Connect repo to [Vercel](https://vercel.com/).
2.  **Variables**: Add `DATABASE_URL` and `APP_ENV=production`.
3.  **Important**: Ensure `VITE_API_URL` points to `/api/v1` if applicable.

---

## 🛠 Local CLI Utility

Use the PowerShell CLI for common tasks:
```powershell
.\loja_cli.ps1 setup    # Install all dependencies
.\loja_cli.ps1 backend  # Run backend locally
.\loja_cli.ps1 test     # Run all backend tests
```

---

## Troubleshooting

*   **API v1 Prefix**: The backend now uses `/api/v1/`. Ensure your calls reflect this.
*   **Healthcheck**: Verify deployment at `/api/v1/saude`.
*   **Cold Starts**: Free tiers on Render/Vercel have "cold starts". Hugging Face Spaces is more persistent.
*   **CORS**: Unified Docker images serve both frontend and backend from the same port, eliminating CORS issues.
