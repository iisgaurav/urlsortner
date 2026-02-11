#!/bin/bash

# Get port from environment (Render sets this)
PORT=${PORT:-8501}

# Start Django API in the background
echo "Starting Django API server..."
python manage.py migrate
gunicorn config.wsgi:application --bind 0.0.0.0:8000 --workers 2 &

# Wait for Django to start
sleep 5

# Start Streamlit UI on the PORT that Render expects
echo "Starting Streamlit UI on port $PORT..."
streamlit run streamlit_app.py --server.port=$PORT --server.address=0.0.0.0
