# Dockerfile for the FastAPI service

FROM python:3.10-slim

WORKDIR /app

# Install system dependencies
# libgomp1 is required for LightGBM
# curl is used for the healthcheck
RUN apt-get update && apt-get install -y --no-install-recommends \
    libgomp1 \
    curl \
    && rm -rf /var/lib/apt/lists/*

# Copy the lean requirements file
COPY requirements-api.txt .

# Upgrade pip and install dependencies with retries
RUN pip install --no-cache-dir --upgrade pip && \
    pip install \
        --no-cache-dir \
        --retries 3 \
        --timeout 30 \
        -r requirements-api.txt
# Copy the entire project
# This includes the models, data, and source code needed by the API
COPY . .

# Expose the port the API will run on
EXPOSE 8000

# Healthcheck to ensure the API is running and healthy
HEALTHCHECK --interval=30s --timeout=10s --start-period=15s --retries=3 \
  CMD curl -fsS http://localhost:8000/health || exit 1

# Command to run the Uvicorn server for FastAPI
CMD ["uvicorn", "api.app:app", "--host", "0.0.0.0", "--port", "8000"] 