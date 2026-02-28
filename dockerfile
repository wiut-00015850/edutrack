# ---------- Stage 1: builder ----------
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
        && pip wheel --no-cache-dir -r requirements.txt
    
    
    # ---------- Stage 2: runtime ----------
    FROM python:3.13-slim
    
    WORKDIR /app
    
    ENV PYTHONDONTWRITEBYTECODE=1
    ENV PYTHONUNBUFFERED=1
    
    RUN apt-get update && apt-get install -y \
        libpq5 \
        && rm -rf /var/lib/apt/lists/*
    
    RUN addgroup --system app && adduser --system --ingroup app app
    
    COPY --from=builder /build/*.whl /wheels/
    RUN pip install --no-cache-dir /wheels/* && rm -rf /wheels
    
    COPY . .
    
    RUN mkdir -p /app/staticfiles /app/media
    
    RUN python manage.py collectstatic --noinput
    
    RUN chown -R app:app /app
    
    USER app
    
    CMD ["gunicorn", "config.wsgi:application", "--bind", "0.0.0.0:8000"]