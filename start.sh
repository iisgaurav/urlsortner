#!/bin/bash

# Get port from environment (Render sets this)
PORT=${PORT:-8501}

# Configure Nginx with the correct port
envsubst '${PORT}' < /etc/nginx/nginx.conf.template > /etc/nginx/sites-available/default
ln -sf /etc/nginx/sites-available/default /etc/nginx/sites-enabled/default

# Start Django API in the background
echo "Starting Django API server on port 8000..."
python manage.py migrate
gunicorn config.wsgi:application --bind 0.0.0.0:8000 --workers 2 &

# Start Streamlit UI in the background
echo "Starting Streamlit UI on port 8501..."
streamlit run streamlit_app.py --server.port=8501 --server.address=0.0.0.0 &

# Wait for services to start
sleep 5

# Start Nginx in foreground
echo "Starting Nginx reverse proxy on port $PORT..."
nginx -g 'daemon off;'
