FROM python:3.11-slim

WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    gcc \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements and install dependencies
COPY pyproject.toml uv.lock ./
RUN pip install --no-cache-dir uv
RUN uv sync --frozen

# Copy ephemeris data files
COPY ephe/ ephe/

# Copy source code
COPY main.py .
COPY static/ static/

# Set environment variables for production
ENV ENVIRONMENT=production
ENV PORT=8080

# Create data directory for SQLite database
RUN mkdir -p /app/data
ENV DATA_DIR=/app/data

# Create non-root user
RUN useradd -m -u 1000 appuser && chown -R appuser:appuser /app
USER appuser

EXPOSE 8080

CMD ["uv", "run", "uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8080", "--workers", "1"]