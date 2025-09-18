# Multi-stage Dockerfile for Vedic Astrology Calculator
# Optimized for both development and production use

# Base stage - common dependencies
FROM python:3.11-slim as base

# Install system dependencies
RUN apt-get update && apt-get install -y \
    gcc \
    curl \
    && rm -rf /var/lib/apt/lists/*

# Install uv for fast package management
RUN pip install uv

# Set working directory
WORKDIR /app

# Set UV environment path for consistency
ENV UV_PROJECT_ENVIRONMENT=/app/.venv

# Copy dependency files
COPY pyproject.toml uv.lock* ./

# Development stage
FROM base as development

# Install development dependencies
RUN uv sync --all-extras

# Copy application code
COPY . .

# Create directories and set permissions
RUN mkdir -p ephe data logs

# Expose port
EXPOSE 5000

# Development startup with hot reload
CMD ["/app/.venv/bin/python", "-m", "uvicorn", "main:app", "--host", "0.0.0.0", "--port", "5000", "--reload"]

# Production builder stage
FROM base as builder

# Install dependencies (no dev dependencies)
RUN uv sync --frozen --no-dev --no-cache

# Production stage
FROM python:3.11-slim as production

# Install runtime dependencies only
RUN apt-get update && apt-get install -y \
    ca-certificates \
    curl \
    && rm -rf /var/lib/apt/lists/*

# Create non-root user for security
RUN useradd --create-home --shell /bin/bash --uid 1000 app

# Set working directory
WORKDIR /app

# Copy virtual environment from builder stage
COPY --from=builder /app/.venv /app/.venv

# Copy application code
COPY --chown=app:app . .

# Create directories and set permissions
RUN mkdir -p ephe data logs && chown -R app:app /app

# Switch to non-root user
USER app

# Expose port
EXPOSE 5000

# Health check
HEALTHCHECK --interval=30s --timeout=10s --start-period=15s --retries=3 \
    CMD curl -f http://localhost:5000/ || exit 1

# Production startup (single worker for SQLite compatibility)
CMD ["/app/.venv/bin/python", "-m", "uvicorn", "main:app", "--host", "0.0.0.0", "--port", "5000", "--workers", "1"]