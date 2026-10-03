# syntax=docker/dockerfile:1

# --- Build stage: install the app and its dependencies into an isolated prefix ---
FROM python:3.11-slim AS builder

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1

WORKDIR /app

# Source is needed because setuptools discovers the `backend` package at build time.
COPY pyproject.toml ./
COPY backend/ ./backend/
RUN pip install --no-cache-dir --prefix=/install .

# --- Runtime stage: slim image with only what we need to run ---
FROM python:3.11-slim AS runtime

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1

WORKDIR /app

# Copy the installed dependencies (and the backend package) from the builder.
COPY --from=builder /install /usr/local
COPY backend/ ./backend/

# Migration config: the entrypoint runs `alembic upgrade head` before serving.
COPY alembic.ini ./
COPY alembic/ ./alembic/

EXPOSE 8000

ENTRYPOINT ["/app/backend/entrypoint.sh"]
CMD ["uvicorn", "backend.main:app", "--host", "0.0.0.0", "--port", "8000"]
