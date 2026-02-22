# ---------- Stage 1: build ----------
    FROM python:3.13-slim AS builder

    WORKDIR /app
    
    ENV PYTHONDONTWRITEBYTECODE=1
    ENV PYTHONUNBUFFERED=1
    
    RUN apt-get update && apt-get install -y \
        build-essential \
        libpq-dev \
        && rm -rf /var/lib/apt/lists/*
    
    COPY requirements.txt .
    RUN pip install --upgrade pip && pip wheel --no-cache-dir --no-deps -r requirements.txt
    
    
    # ---------- Stage 2: runtime ----------
    FROM python:3.13-slim
    
    WORKDIR /app
    
    RUN addgroup --system app && adduser --system --ingroup app app
    
    RUN apt-get update && apt-get install -y \
        libpq-dev \
        && rm -rf /var/lib/apt/lists/*
    
    COPY --from=builder /app /app
    COPY . .
    
    RUN pip install --no-cache-dir /app/*.whl
    
    USER app
    
    CMD ["gunicorn", "config.wsgi:application", "--bind", "0.0.0.0:8000"]