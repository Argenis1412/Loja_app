# Deployment Guide — Loja App

This document provides detailed instructions for deploying the Loja App to production environments using **Render** (for the Backend and Database) and **Vercel** (for the Frontend).

---

## Backend & Database Deployment (Render)

### 1. Create PostgreSQL Database
1. Go to your [Render Dashboard](https://dashboard.render.com/).
2. Click **New +** → **PostgreSQL**.
3. **Name**: `loja-db`.
4. **Region**: Choose the one closest to you.
5. **Plan**: Free or Starter.
6. Once created, copy the **Internal Database URL**.

### 2. Create Web Service
1. Click **New +** → **Web Service**.
2. Connect your GitHub repository.
3. **Root Directory**: `backend`.
4. **Runtime**: `Python 3`.
5. **Build Command**: `./build.sh` (ensure it has execute permissions: `chmod +x build.sh`).
6. **Start Command**: `gunicorn -w 4 -k uvicorn.workers.UvicornWorker api.main:app --bind 0.0.0.0:$PORT`.

### 3. Environment Variables
In the **Environment** tab of your Web Service, add:
- `DATABASE_URL`: The URL copied from step 1.
- `ENVIRONMENT`: `production`.
- `API_HOST`: `0.0.0.0`.

---

## Frontend Deployment (Vercel)

### 1. Quick Deploy via Dashboard
1. Go to [vercel.com](https://vercel.com).
2. Click **Import Project** → Connect GitHub.
3. **Framework Preset**: `Vite`.
4. **Root Directory**: `frontend`.
5. **Build Command**: `npm run build`.
6. **Output Directory**: `dist`.

### 2. API Configuration
By default, the frontend points to `https://loja-app.onrender.com`. To override this, set the following Environment Variable in Vercel:
- `VITE_API_URL`: `https://your-backend-url.onrender.com`.

---

## Local Development with Cloud Backend
To test your local frontend against the production backend:
1. Create `frontend/.env.local`.
2. Add: `VITE_API_URL=https://your-backend-url.onrender.com`.
3. Run `npm run dev` in the `frontend` directory.

---

## Maintenance

### Database Migrations
Migrations run automatically during the build process on Render via the `build.sh` script.

### Troubleshooting
- **CORS Errors**: The backend is configured to allow all origins (`*`) by default for this lab. For production use, restrict this in `api/main.py`.
- **Port Issues**: Render provides the `$PORT` variable; ensure your start command uses it.
