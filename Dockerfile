# THE DOME — production-ready container image
#
# Build:  docker build -t dome .
# Run:    docker run -p 8000:8000 dome

FROM python:3.12-slim

# Prevent Python from writing .pyc files and enable unbuffered stdout/stderr
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1

WORKDIR /app

# Install system dependencies required by asyncpg
RUN apt-get update && \
    apt-get install -y --no-install-recommends gcc libpq-dev && \
    rm -rf /var/lib/apt/lists/*

# Copy project files
COPY pyproject.toml ./
COPY dome/ ./dome/
COPY alembic/ ./alembic/

# Install the project and its dependencies
RUN pip install --no-cache-dir --upgrade pip && \
    pip install --no-cache-dir .

# Expose the application port
EXPOSE 8000

# Start the ASGI server
CMD ["uvicorn", "dome.main:app", "--host", "0.0.0.0", "--port", "8000"]
