# ============================================================
# Zoho Catalyst AppSail — Custom OCI Runtime Dockerfile
# Backend: FastAPI + LangGraph + Zoho Catalyst SDK
# ============================================================

FROM python:3.10-slim

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# Default port for Catalyst AppSail (overridden by X_ZOHO_CATALYST_LISTEN_PORT at runtime)
ENV X_ZOHO_CATALYST_LISTEN_PORT=9000

# Set working directory
WORKDIR /app

# Install system dependencies required by PyMySQL / SQLAlchemy
RUN apt-get update && apt-get install -y --no-install-recommends \
    gcc \
    default-libmysqlclient-dev \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements first for Docker layer caching
COPY requirements.txt .

# Install Python dependencies
RUN pip install --no-cache-dir --upgrade pip && \
    pip install --no-cache-dir -r requirements.txt && \
    pip install --no-cache-dir zcatalyst-sdk langchain-ollama

# Copy the entire backend application
COPY . .

# Expose the default port (informational only)
EXPOSE 9000

# Start Uvicorn, dynamically binding to the Catalyst-provided port
CMD ["sh", "-c", "uvicorn app.app:app --host 0.0.0.0 --port ${X_ZOHO_CATALYST_LISTEN_PORT:-9000}"]
