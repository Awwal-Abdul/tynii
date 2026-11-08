FROM python:3.13-slim

LABEL project="tynii"

# Install redis-server and clean up apt cache
RUN apt-get update && \
    apt-get install -y --no-install-recommends redis-server && \
    rm -rf /var/lib/apt/lists/*

# Install uv using the official Astral binary
COPY --from=ghcr.io/astral-sh/uv:latest /uv /uvx /bin/

WORKDIR /app

# Configure Python and add the virtualenv to PATH
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PATH="/app/.venv/bin:$PATH"

# Copy dependency specifications first to leverage Docker layer caching
COPY pyproject.toml uv.lock README.md ./

# Install project dependencies
RUN uv sync --frozen --no-install-project

# Copy application source code and install the project
COPY src ./src
RUN uv sync --frozen

EXPOSE 80

# Start redis-server in daemon mode and run gunicorn bound to 0.0.0.0:8000
CMD ["sh", "-c", "redis-server --daemonize yes && exec gunicorn --chdir src --bind 0.0.0.0:8000 tynii.app:app"]
