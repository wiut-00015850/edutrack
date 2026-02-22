# ---------- Stage 1: build ----------
    FROM python:3.13-slim AS builder

    WORKDIR /app
    
    ENV PYTHONDONTWRITEBYTECODE=1
    ENV PYTHONUNBUFFERED=1
    
    # System deps needed to build wheels
    RUN apt-get update && apt-get install -y \
        build-essential \
        libpq-dev \
        && rm -rf /var/lib/apt/lists/*
    
    # Install Python deps as wheels
    COPY requirements.txt .
    RUN pip install --upgrade pip \
        && pip wheel --no-cache-dir --no-deps -r requirements.txt
    
    
    # ---------- Stage 2: runtime ----------
    FROM python:3.13-slim
    
    WORKDIR /app
    
    ENV PYTHONDONTWRITEBYTECODE=1
    ENV PYTHONUNBUFFERED=1
    
    # Create non-root user
    RUN addgroup --system app && adduser --system --ingroup app app
    
    # Runtime system deps
    RUN apt-get update && apt-get install -y \
        libpq-dev \
        && rm -rf /var/lib/apt/lists/*
    
    # Copy built wheels from builder
    COPY --from=builder /app /app
    
    # Copy project source
    COPY . .
    
    # Install Python packages from wheels
    RUN pip install --no-cache-dir /app/*.whl
    
    # ✅ FIX: create & own static/media directories BEFORE switching user
    RUN mkdir -p /app/staticfiles /app/media \
        && chown -R app:app /app
    
    # Drop privileges
    USER app
    
    # Run Django via Gunicorn (NOT runserver)
    CMD ["gunicorn", "config.wsgi:application", "--bind", "0.0.0.0:8000"]