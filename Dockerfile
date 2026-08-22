# Dockerfile for Render - Runs Django, Streamlit, and Nginx
FROM python:3.11-slim

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1

WORKDIR /app

# Install system dependencies including Nginx
RUN apt-get update && apt-get install -y \
    gcc \
    postgresql-client \
    nginx \
    gettext-base \
    && rm -rf /var/lib/apt/lists/*

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

# Copy Nginx config template
COPY nginx.conf.template /etc/nginx/nginx.conf.template

# Make start script executable
RUN chmod +x start.sh

CMD ["sh", "start.sh"]
