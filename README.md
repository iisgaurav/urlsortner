# 🔗 URL Shortener

A production-grade URL shortening service built with Django REST Framework and Streamlit. Transform long URLs into short, trackable links with advanced analytics, QR code generation, and a beautiful user interface.

[![Python](https://img.shields.io/badge/python-3.11-blue.svg)](https://www.python.org/)
[![Django](https://img.shields.io/badge/django-4.2-green.svg)](https://www.djangoproject.com/)
[![License](https://img.shields.io/badge/license-MIT-blue.svg)](LICENSE)

## ✨ Features

### Core Functionality
- **URL Shortening** - Convert long URLs into short, memorable links
- **Custom Short Codes** - Choose your own custom aliases
- **QR Code Generation** - Auto-generate QR codes for any short URL
- **Expiry Dates** - Set automatic expiration for temporary links
- **Click Analytics** - Track clicks with IP address and user agent
- **Rate Limiting** - Protect against abuse (10 requests/minute per IP)

### User Interface
- **Modern Streamlit UI** - Clean, professional web interface
- **Real-time Analytics Dashboard** - Interactive charts and metrics
- **URL History** - Track all your created short URLs
- **Insights & Trends** - Visualize click patterns
- **Mobile Responsive** - Works on all devices

### Backend Features
- **Redis Caching** - Lightning-fast redirects with cache-aside pattern
- **Celery Background Jobs** - Async click tracking and cleanup
- **RESTful API** - Full-featured API for programmatic access
- **PostgreSQL Database** - Reliable cloud-hosted storage (Supabase)
- **Docker Support** - Ready for containerized deployment

## 🚀 Quick Start

### Prerequisites

- Python 3.11+
- PostgreSQL (or Supabase account)
- Redis (or Redis Cloud account)

### Installation

1. **Clone the repository**
   ```bash
   git clone https://github.com/yourusername/url-shortener.git
   cd url-shortener
   ```

2. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

3. **Configure environment variables**
   ```bash
   cp .env.example .env
   # Edit .env with your database and Redis credentials
   ```

4. **Run migrations**
   ```bash
   python manage.py migrate
   ```

5. **Start the application**
   ```bash
   # Terminal 1: Django API
   python manage.py runserver
   
   # Terminal 2: Streamlit UI
   streamlit run streamlit_app.py
   ```

6. **Access the application**
   - Streamlit UI: http://localhost:8501
   - Django API: http://localhost:8000
   - Admin Panel: http://localhost:8000/admin

## 📚 API Documentation

### Endpoints

#### Create Short URL
```http
POST /api/shorten/
Content-Type: application/json

{
  "original_url": "https://example.com/very/long/url",
  "custom_code": "mylink",  // optional
  "expiry_date": "2024-12-31T23:59:59Z"  // optional
}
```

**Response:**
```json
{
  "short_url": "http://localhost:8000/abc123",
  "short_code": "abc123",
  "original_url": "https://example.com/very/long/url",
  "created_at": "2024-02-11T10:00:00Z"
}
```

#### Redirect to Original URL
```http
GET /{short_code}/
```
Returns: 302 redirect to original URL

#### Get Analytics
```http
GET /api/analytics/{short_code}/
```

**Response:**
```json
{
  "short_code": "abc123",
  "original_url": "https://example.com",
  "total_clicks": 42,
  "created_at": "2024-02-11T10:00:00Z",
  "is_active": true,
  "recent_clicks": [...]
}
```

#### Delete URL
```http
DELETE /api/urls/{short_code}/
```

## 🛠️ Tech Stack

### Backend
- **Django 4.2** - Web framework
- **Django REST Framework** - API development
- **PostgreSQL** - Database (Supabase)
- **Redis** - Caching and message broker
- **Celery** - Background task processing
- **Gunicorn** - Production WSGI server

### Frontend
- **Streamlit** - Web UI framework
- **Plotly** - Interactive charts
- **Pandas** - Data manipulation

### DevOps
- **Docker** - Containerization
- **Docker Compose** - Multi-container orchestration
- **GitHub Actions** - CI/CD (optional)

## 🌐 Deployment

This application is ready to deploy to various platforms:

### Quick Deploy (Recommended)

**Koyeb** (Free tier, fastest)
```bash
# See KOYEB_DEPLOYMENT.md for detailed instructions
1. Push to GitHub
2. Connect to Koyeb
3. Configure environment variables
4. Deploy!
```

**Other Platforms:**
- [Railway](DEPLOY_SINGLE_SERVICE.md) - Easy deployment
- [Render](DEPLOY_SINGLE_SERVICE.md) - Free tier available
- [Heroku](DEPLOYMENT_GUIDE.md) - Reliable platform
- [VPS/Docker](DEPLOYMENT_GUIDE.md) - Full control

**Deployment Guides:**
- 📖 [Koyeb Deployment](KOYEB_DEPLOYMENT.md) - Recommended
- 📖 [Single Service Deployment](DEPLOY_SINGLE_SERVICE.md) - Railway/Render
- 📖 [Full Deployment Guide](DEPLOYMENT_GUIDE.md) - All options

## 📁 Project Structure

```
url-shortener/
├── config/                 # Django project settings
│   ├── settings.py        # Main configuration
│   ├── urls.py            # URL routing
│   └── celery.py          # Celery configuration
├── shortener/             # Main application
│   ├── models.py          # Database models
│   ├── views.py           # API endpoints
│   ├── serializers.py     # DRF serializers
│   ├── tasks.py           # Celery tasks
│   ├── middleware.py      # Rate limiting
│   └── utils.py           # Helper functions
├── streamlit_app.py       # Streamlit UI
├── requirements.txt       # Python dependencies
├── Dockerfile             # Container configuration
├── docker-compose.yml     # Multi-service setup
├── start.sh               # Single-service startup script
└── README.md              # This file
```

## ⚙️ Configuration

### Environment Variables

Create a `.env` file based on `.env.example`:

```bash
# Database (Supabase)
DATABASE_URL=postgresql://user:pass@host:port/db

# Redis Cloud
REDIS_HOST=your-redis-host
REDIS_PORT=17479
REDIS_PASSWORD=your-password

# Django
SECRET_KEY=your-secret-key
DEBUG=False
ALLOWED_HOSTS=.yourdomain.com

# Application
SHORT_URL_DOMAIN=https://yourdomain.com
USE_DUMMY_CACHE=False
RATE_LIMIT_REQUESTS=10
RATE_LIMIT_WINDOW=60
```

## 🔧 Development

### Running Tests
```bash
python manage.py test
```

### API Testing
```bash
python test_api.py
```

### Code Quality
```bash
# Format code
black .

# Lint
flake8 .
```

### Docker Development
```bash
docker-compose up --build
```

## 📊 Features in Detail

### Caching Strategy
- **Cache-aside pattern** with Redis
- 1-hour TTL for cached URLs
- Automatic cache invalidation on updates
- Sub-millisecond redirect times

### Rate Limiting
- **Sliding window algorithm**
- IP-based tracking
- Configurable limits via environment variables
- Returns 429 status when exceeded

### Background Jobs
- **Async click logging** - Non-blocking analytics
- **Periodic cleanup** - Removes expired URLs daily
- **Celery Beat** - Scheduled task execution

### Analytics
- Total click count per URL
- Individual click events with timestamps
- IP address and user agent tracking
- Recent activity visualization

## 🤝 Contributing

Contributions are welcome! Please follow these steps:

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## 📝 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgments

- Django REST Framework for the excellent API toolkit
- Streamlit for the beautiful UI framework
- Supabase for reliable PostgreSQL hosting
- Redis Cloud for fast caching

## 📧 Contact

For questions or support, please open an issue on GitHub.

---

**Built with ❤️ using Django, Streamlit, Redis, and PostgreSQL**

⭐ Star this repo if you find it helpful!
