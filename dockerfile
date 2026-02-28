# ---------- Stage 1: build ----------
    FROM python:3.13-slim AS builder

    WORKDIR /build
    
    ENV PYTHONDONTWRITEBYTECODE=1
    ENV PYTHONUNBUFFERED=1
    
    RUN apt-get update && apt-get install -y \
        build-essential \
        libpq-dev \
        && rm -rf /var/lib/apt/lists/*
    
    COPY requirements.txt .
    
    RUN pip install --upgrade pip \
        && pip wheel --no-cache-dir --no-deps -r requirements.txt
    
    
    # ---------- Stage 2: runtime ----------
    FROM python:3.13-slim
    
    WORKDIR /app
    
    ENV PYTHONDONTWRITEBYTECODE=1
    ENV PYTHONUNBUFFERED=1
    
    # Only runtime dependency
    RUN apt-get update && apt-get install -y \
        libpq5 \
        && rm -rf /var/lib/apt/lists/*
    
    # Create non-root user
    RUN addgroup --system app && adduser --system --ingroup app app
    
    # Copy wheels only
    COPY --from=builder /build/*.whl /wheels/
    
    # Install dependencies from wheels
    RUN pip install --no-cache-dir /wheels/* \
        && rm -rf /wheels
    
    # Copy project source
    COPY . .
    
    # Create runtime dirs
    RUN mkdir -p /app/staticfiles /app/media \
        && chown -R app:app /app
    
    USER app
    
    CMD ["gunicorn", "config.wsgi:application", "--bind", "0.0.0.0:8000"]