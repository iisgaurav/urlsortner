# 🚀 How to Run the URL Shortener with Streamlit UI

## Quick Start

### 1. Start the Django Backend API

In one terminal:
```bash
python manage.py runserver
```

This starts the API server at `http://localhost:8000`

### 2. Launch the Streamlit UI

In another terminal:
```bash
streamlit run streamlit_app.py
```

The Streamlit UI will open automatically in your browser at `http://localhost:8501`

## Features

### 🔗 URL Shortener UI

- **Create Short URLs**: Enter any long URL and get a short link
- **Custom Codes**: Choose your own custom short code (e.g., `mylink`)
- **Set Expiry**: Make links expire after a specific date
- **Click Analytics**: View detailed statistics for each short URL
- **Click History**: Track IP addresses and user agents
- **URL History**: See all your created short URLs in one place

### 📊 Analytics Dashboard

- Total clicks per URL
- Active/Expired status
- Recent click events with timestamps
- IP addresses and user agents
- Creation and expiry dates

## Screenshots

The Streamlit UI includes:
- Beautiful, modern design with custom CSS
- Three-tab interface: Create URL | Analytics | History
- Real-time statistics in the sidebar
- One-click copy of short URLs
- Mobile-responsive layout

## API Compatibility

The Streamlit UI connects to your Django backend API at:
- POST `/api/shorten/` - Create short URLs
- GET `/api/analytics/{short_code}/` - Get analytics
- GET `/{short_code}/` - Redirect (happens automatically)

## Troubleshooting

**UI says "Connection Error"**:
- Make sure Django server is running on port 8000
- Check that your `.env` file has the correct settings

**Can't create URLs**:
- Verify the API is accessible at `http://localhost:8000/api/shorten/`
- Check Django server logs for errors

**Redis errors**:
- Ensure your Redis Cloud credentials are correct in `.env`
- The backend will work without Redis (with dummy cache)

## Customization

Edit `streamlit_app.py` to customize:
- API_BASE_URL (line 12) - Change if using different port
- Page styling (lines 16-42) - Modify CSS
- Colors and themes - Update st.markdown styles

Enjoy your URL Shortener! 🎉
