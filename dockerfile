# Stage 1: Builder

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



# Stage 2: Runtime

FROM python:3.13-slim

WORKDIR /app

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1
ENV DJANGO_SETTINGS_MODULE=config.settings.prod

# System deps
RUN apt-get update && apt-get install -y \
    libpq5 \
    netcat-openbsd \
    && rm -rf /var/lib/apt/lists/*

# Create non-root user
RUN addgroup --system app && adduser --system --ingroup app app

# Install python deps
COPY --from=builder /build /wheels
RUN pip install --no-cache-dir -r /wheels/requirements.txt \
    && rm -rf /wheels

# Copy project
COPY . .

# Prepare runtime dirs
RUN mkdir -p /app/staticfiles /app/media \
    && chown -R app:app /app

# Collect static as ROOT (important)
RUN DJANGO_SETTINGS_MODULE=config.settings.build \
    python manage.py collectstatic --noinput

# Entrypoint
COPY entrypoint.sh /entrypoint.sh
RUN chmod +x /entrypoint.sh
    
# Drop privileges
USER app

ENTRYPOINT ["/entrypoint.sh"]