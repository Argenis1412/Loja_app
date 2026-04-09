# Stage 1: Build Frontend
FROM node:20-slim AS frontend-builder
WORKDIR /app/frontend
COPY frontend/package*.json ./
RUN npm install
COPY frontend/ ./
RUN npm run build

# Stage 2: Backend & Final Image
FROM python:3.11-slim
WORKDIR /app

# Install system dependencies for psycopg2
RUN apt-get update && apt-get install -y \
    libpq-dev \
    gcc \
    && rm -rf /var/lib/apt/lists/*

# Install Python dependencies
COPY backend/requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

# Copy backend code
COPY backend/ ./backend

# Copy built frontend from Stage 1
COPY --from=frontend-builder /app/frontend/dist ./static

# Set PYTHONPATH to include the backend directory
ENV PYTHONPATH=/app/backend

# Command to run the application
# We use backends/api/main.py:app
CMD ["uvicorn", "api.main:app", "--host", "0.0.0.0", "--port", "7860"]
