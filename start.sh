#!/bin/bash

# Start Django API in the background
echo "Starting Django API server..."
python manage.py migrate
gunicorn config.wsgi:application --bind 0.0.0.0:8000 --workers 2 &

# Wait for Django to start
sleep 5

# Start Streamlit UI
echo "Starting Streamlit UI..."
streamlit run streamlit_app.py --server.port=8501 --server.address=0.0.0.0
