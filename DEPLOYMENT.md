# Deployment Guide — Loja App

This document explains how to deploy the entire project (Frontend and Backend) using either **Vercel** or **Docker** (for Hugging Face Spaces, Northflank, Koyeb, etc.), utilizing **Supabase** or **Neon** as a high-performance database.

## Step 1: Database

Cloud providers usually don't persist local files (like SQLite's `test.db`), so we will use a cloud PostgreSQL database.

1.  Create a project on [Supabase](https://supabase.com/) or [Neon.tech](https://neon.tech).
2.  Go to **Settings** → **Database** → **Connection String**.
3.  Copy the connection string (starting with `postgresql://`).
4.  Replace `[YOUR-PASSWORD]` with the actual password.
5.  **Save this URL**, you will need it for the next step as `DATABASE_URL`.

---

## Step 2: Deployment Options

### Option A: unified Docker Deployment (Recommended)

This project includes a multi-stage `Dockerfile` that builds the React frontend and serves it via the FastAPI backend. This is the fastest and most portable way to deploy.

1. **Hugging Face Spaces / Northflank / Koyeb**: Create a new application and select "Docker" or connect your GitHub repository.
2. Ensure the build context is the repository root `/`.
3. Set the following environment variable:
   - `DATABASE_URL`: Your PostgreSQL connection string.
4. Deploy! A single container will serve both the API (at `/api/...`) and the web interface (at `/`).

### Option B: Vercel (Frontend & Serverless Functions)

Vercel will build the Frontend (Vite) and deploy the Backend (FastAPI) as serverless functions.

1.  Go to your [Vercel](https://vercel.com/) dashboard and click **"Add New"** → **"Project"**.
2.  Import this repository from GitHub.
3.  **Project Configuration**: Vercel will detect Vite. Leave the `Root Directory` as `/`.
4.  **Environment Variables**:
    Add the following variables before clicking "Deploy":

    | Key | Value |
    | :--- | :--- |
    | `DATABASE_URL` | The database URL from Step 1 |
    | `ENVIRONMENT` | `production` |

5.  Click **"Deploy"**.

*Note: In Vercel, requests to `/api/*` are routed to the Python backend automatically. Everything else serves the frontend.*

---

## Local Development with Cloud Database

If you want to test your code locally using a cloud database instead of SQLite:

1.  Create a `.env` file in the `backend/` folder.
2.  Add `DATABASE_URL=your_connection_string`.
3.  Run the application normally.

---

## Troubleshooting

*   **Cold Starts (Vercel)**: Serverless functions may take 2-5 seconds to respond on the first request after being idle. The Docker method does not suffer from this issue.
*   **CORS**: The system is configured to allow requests from any origin. If using Vercel or the single-container Docker image, both frontend and backend share the same domain, preventing CORS errors.
*   **Timeout**: Vercel free tier limits function execution to 10 seconds.
