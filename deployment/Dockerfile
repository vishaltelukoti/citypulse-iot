# -------- Stage 1: Builder --------
FROM python:3.11-slim AS builder

WORKDIR /build

# Install build dependencies
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements and build wheels
COPY requirements.txt .
RUN pip install --upgrade pip \
    && pip wheel --no-cache-dir --wheel-dir /wheels -r requirements.txt


# -------- Stage 2: Runtime --------
FROM python:3.11-slim

WORKDIR /app

# Copy prebuilt wheels from builder
COPY --from=builder /wheels /wheels

# Install only runtime deps (no compiler here)
RUN pip install --no-cache-dir /wheels/* \
    && rm -rf /wheels

# Copy project code
COPY . .

# Create logs directory
RUN mkdir -p /app/var/logs

# Environment
ENV PYTHONUNBUFFERED=1

# Default command
CMD ["python", "main.py"]
