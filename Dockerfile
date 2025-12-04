FROM python:3.11-slim

# Set working directory
WORKDIR /app

# Don't write pyc files and buffer stdout/stderr
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# Install system dependencies needed to build some Python packages (e.g. psycopg2)
RUN apt-get update \
  && apt-get install -y --no-install-recommends \
  build-essential \
  gcc \
  libpq-dev \
  && rm -rf /var/lib/apt/lists/*

# Install Python dependencies first (cache layer)
COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt \
  # ensure gunicorn is available for production runs
  && pip install --no-cache-dir gunicorn

# Copy application code
COPY . .

# Create an unprivileged user and give ownership of the app directory
RUN useradd -m flaskuser \
  && chown -R flaskuser:flaskuser /app

USER flaskuser

# Expose port (Render will set PORT environment variable)
EXPOSE 10000

# Start the app with gunicorn. 
# Render sets PORT automatically, fallback to 5001 for local development
ENV GUNICORN_WORKERS=3
CMD ["sh", "-c", "exec gunicorn --bind 0.0.0.0:${PORT:-5001} --workers ${GUNICORN_WORKERS} run:app"]
