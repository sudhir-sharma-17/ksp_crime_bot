# ============================================================
# Stage 1: Build Production React/Vite Frontend
# ============================================================
FROM node:20-alpine AS frontend-builder

WORKDIR /build/frontend

# Copy frontend package manifests for efficient layer caching
COPY frontend/package.json frontend/package-lock.json* ./

# Install frontend dependencies
RUN if [ -f package-lock.json ]; then npm ci; else npm install; fi

# Copy frontend source code
COPY frontend/ ./

# Build production bundle -> /build/frontend/dist
RUN npm run build


# ============================================================
# Stage 2: Unified Python Runtime (FastAPI + LangGraph + AppSail)
# ============================================================
FROM python:3.12-slim

# Set Python environment flags
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    X_ZOHO_CATALYST_LISTEN_PORT=9000 \
    PORT=9000 \
    FRONTEND_DIST_DIR=/app/frontend/dist

# Set root working directory
WORKDIR /app

# Install system build dependencies & curl for healthcheck
RUN apt-get update && apt-get install -y --no-install-recommends \
    gcc \
    default-libmysqlclient-dev \
    curl \
    && rm -rf /var/lib/apt/lists/*

# Copy backend requirements for layer caching
COPY backend/requirements.txt ./backend/

# Install Python dependencies in UTF-8
RUN pip install --no-cache-dir --upgrade pip && \
    pip install --no-cache-dir -r ./backend/requirements.txt

# Copy backend source code into /app/backend/
COPY backend/ ./backend/

# Copy compiled frontend assets from Stage 1 into /app/frontend/dist/
COPY --from=frontend-builder /build/frontend/dist ./frontend/dist/

# Set working directory to backend so `app.app:app` and module imports resolve cleanly
WORKDIR /app/backend

# Expose the default AppSail container port
EXPOSE 9000

# Docker Healthcheck
HEALTHCHECK --interval=30s --timeout=5s --start-period=10s --retries=3 \
    CMD curl -f http://localhost:${X_ZOHO_CATALYST_LISTEN_PORT:-9000}/api/health || exit 1

# Start Uvicorn dynamically bound to Catalyst AppSail port (or fallback PORT)
CMD ["sh", "-c", "uvicorn app.app:app --host 0.0.0.0 --port ${X_ZOHO_CATALYST_LISTEN_PORT:-${PORT:-9000}}"]
