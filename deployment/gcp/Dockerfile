FROM python:3.11-slim

WORKDIR /app

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

# Create non-root user for security
RUN useradd -m -u 1000 appuser && chown -R appuser:appuser /app
USER appuser

EXPOSE $PORT

CMD ["sh", "-c", "uv run uvicorn main:app --host 0.0.0.0 --port $PORT --workers 1"]