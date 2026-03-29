# Deployment Guide — Loja App

This document provides step-by-step instructions to deploy the Loja App using a high-performance, free-tier stack:

| Layer    | Platform    | Why                                              |
|----------|-------------|--------------------------------------------------|
| Frontend | **Vercel**  | Instant global CDN, perfect for Vite/React       |
| Backend  | **Koyeb**   | Persistent containers = zero cold starts         |
| Database | **Supabase**| Managed PostgreSQL, free tier, easy setup        |

---

## Step 1: Database — Supabase (PostgreSQL)

1. Create a free account at [supabase.com](https://supabase.com/).
2. Click **New Project** → Give it a name (e.g., `loja-db`) and a strong password.
3. Once ready, go to **Settings** → **Database**.
4. Under **Connection String** → **URI**, copy the full string:
   ```
   postgresql://postgres:[YOUR-PASSWORD]@db.<ref>.supabase.co:5432/postgres
   ```
5. Replace `[YOUR-PASSWORD]` with the password you defined. **Save this URL**, you'll need it for Koyeb.

> **Note**: Migrations are run automatically during the Koyeb build step via `alembic upgrade head`.

---

## Step 2: Backend — Koyeb

Koyeb runs your FastAPI app in a **persistent Docker container**, ensuring instant responses with no cold starts.

### 2.1 Connect your repository

1. Create a free account at [koyeb.com](https://koyeb.com/).
2. Click **Create App** → **GitHub**.
3. Select your `Loja_app` repository.
4. Set **Root Directory** to `backend`.

### 2.2 Configure the build

| Setting         | Value                                                                 |
|-----------------|-----------------------------------------------------------------------|
| Builder         | `Dockerfile` (Koyeb auto-detects `backend/Dockerfile`)               |
| Run Command     | *(leave empty, defined in Dockerfile)*                                |
| Port            | `8000`                                                                |

### 2.3 Environment Variables

In the **Environment variables** section, add:

| Key              | Value                                      |
|------------------|--------------------------------------------|
| `DATABASE_URL`   | The Supabase URI from Step 1               |
| `ENVIRONMENT`    | `production`                               |

> **Tip**: Add `DATABASE_URL` as a **Secret** for better security.

### 2.4 Deploy

Click **Deploy**. Koyeb will build the Docker image and run `alembic upgrade head` automatically via the `build.sh` entrypoint.

Once deployed, copy your Koyeb URL (e.g., `https://loja-app-youruser.koyeb.app`).

---

## Step 3: Frontend — Vercel

1. Go to [vercel.com](https://vercel.com/) and click **Import Project**.
2. Connect your GitHub repository.
3. Configure the project:

| Setting           | Value           |
|-------------------|-----------------|
| Framework Preset  | `Vite`          |
| Root Directory    | `frontend`      |
| Build Command     | `npm run build` |
| Output Directory  | `dist`          |

4. Add the following **Environment Variable** in Vercel:

| Key             | Value                                           |
|-----------------|-------------------------------------------------|
| `VITE_API_URL`  | Your Koyeb URL (e.g., `https://loja-app-youruser.koyeb.app`) |

5. Click **Deploy**. Your frontend will be live in ~1 minute.

---

## Step 4: Connect Frontend to Backend

Update `frontend/.env.production` with your actual Koyeb URL:

```env
VITE_API_URL=https://loja-app-youruser.koyeb.app
```

Commit and push — Vercel will automatically redeploy.

---

## Local Development with Cloud Backend

To test your local frontend against the production backend:

1. Create or edit `frontend/.env.local`:
   ```env
   VITE_API_URL=https://loja-app-youruser.koyeb.app
   ```
2. Run the dev server:
   ```bash
   cd frontend && npm run dev
   ```

---

## Architecture Overview

```
Browser
  │
  ├──► Vercel (Frontend — React/Vite)
  │         │
  │         └──► Koyeb (Backend — FastAPI)
  │                    │
  │                    └──► Supabase (PostgreSQL)
```

---

## Maintenance

### Database Migrations

Migrations run automatically on every Koyeb deployment via the `build.sh` script:

```bash
alembic upgrade head
```

To run manually, use the Koyeb console or SSH into a running instance:

```bash
PYTHONPATH=. alembic upgrade head
```

### Troubleshooting

| Issue                  | Solution                                                                             |
|------------------------|--------------------------------------------------------------------------------------|
| CORS Errors            | Verify `CORS_ORIGINS` in `api/main.py` includes your Vercel domain                  |
| DB Connection Error    | Double-check `DATABASE_URL` in Koyeb secrets; ensure Supabase allows connections    |
| Slow first response    | Should not happen with Koyeb — if it does, check the container health in Koyeb logs |
| Build fails (Koyeb)    | Check that `backend/Dockerfile` is present and `requirements.txt` is up to date      |
