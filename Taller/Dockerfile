FROM python:3.12-slim

# Install system dependencies required for mysqlclient compilation
RUN apt-get update && apt-get install -y \
    default-libmysqlclient-dev \
    pkg-config \
    build-essential \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app

# Install Python dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy application source
COPY . .

# Collect static files at build time
RUN python manage.py collectstatic --noinput

# Run migrations then start gunicorn
CMD python manage.py migrate && gunicorn config.wsgi --bind 0.0.0.0:$PORT --log-file -
