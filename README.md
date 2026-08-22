# 🔗 URL Shortener Pro

![Python](https://img.shields.io/badge/Python-3.11-blue.svg)
![Django](https://img.shields.io/badge/Django-4.2-green.svg)
![Streamlit](https://img.shields.io/badge/Streamlit-1.29-red.svg)
![Redis](https://img.shields.io/badge/Redis-Cache-dc382d.svg)
![PostgreSQL](https://img.shields.io/badge/PostgreSQL-Database-336791.svg)
![Celery](https://img.shields.io/badge/Celery-Async-yellowgreen.svg)
![Docker](https://img.shields.io/badge/Docker-Ready-2496ed.svg)
![License](https://img.shields.io/badge/License-MIT-blue.svg)

A scalable, production-grade URL shortening service built with a powerful **Django REST API** backend and a sleek, interactive **Streamlit** dashboard. Designed for high performance, it features sub-millisecond redirects using Redis caching, asynchronous click tracking, and an intelligent Nginx reverse proxy routing system.

---

## 🌟 Key Features

* **⚡ Sub-Millisecond Redirects:** Cache-aside pattern using Redis ensures ultra-fast URL redirection.
* **📊 Real-Time Analytics:** Detailed click tracking including IP, User Agent, and geographic insights.
* **🎨 Interactive Dashboard:** Beautiful Streamlit-based UI for managing URLs and visualizing analytics via Plotly.
* **🔗 Custom Short Codes:** Generate automatic Base62 codes or define your own branded short links.
* **⏱️ URL Expiry:** Set custom expiration dates for temporary links, automatically cleaned up by Celery Beat.
* **📱 QR Code Generation:** Instantly generate and download QR codes for your short links.
* **🛡️ Rate Limiting:** Sliding window algorithm using Redis to prevent abuse (default 10 req/min per IP).
* **🐳 Dockerized:** Fully containerized with a multi-service setup (Django, Streamlit, Nginx) for easy deployment.

---

## 🏗️ Architecture

The system uses a modern, distributed architecture:

1. **Nginx Reverse Proxy:** Routes `/api/` and `/[code]` to Django, and `/` to Streamlit.
2. **Django Backend:** Handles core business logic, REST APIs, and database interactions.
3. **Streamlit Frontend:** Consumes the API and renders the interactive dashboard.
4. **PostgreSQL:** Primary persistent data store (URLs and Click Events).
5. **Redis:** In-memory store serving as the cache layer and Celery message broker.
6. **Celery Workers:** Asynchronously process click events to prevent redirect latency.

---

## 🛠️ Technology Stack

| Component | Technology |
| :--- | :--- |
| **Backend Framework** | Django 4.2 & Django REST Framework |
| **Frontend UI** | Streamlit, Plotly, Pandas |
| **Database** | PostgreSQL |
| **Caching & Message Broker**| Redis |
| **Task Queue** | Celery & Celery Beat |
| **Web Server / Proxy** | Gunicorn & Nginx |
| **Containerization** | Docker |

---

## 🚀 Quick Start (Local Development)

### Prerequisites
* Python 3.11+
* PostgreSQL
* Redis Server

### 1. Clone the Repository
```bash
git clone https://github.com/iisgaurav/urlsortner.git
cd urlsortner
```

### 2. Environment Setup
Create a virtual environment and install dependencies:
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
pip install -r requirements.txt
```

### 3. Environment Variables
Create a `.env` file in the root directory based on `.env.example`:
```bash
cp .env.example .env
```
Ensure you update the `DATABASE_URL` and `REDIS_HOST` with your local credentials.

### 4. Database Migrations
```bash
python manage.py migrate
```

### 5. Run the Application
You can run the full stack using the provided shell script:
```bash
chmod +x start.sh
./start.sh
```
This will start:
* **Django API** on port `8000`
* **Streamlit UI** on port `8501`
* **Nginx Proxy** (requires proper setup locally, or run services individually)

---

## 🌐 Deployment (Render / Cloud)

This project is optimized for deployment on Platforms as a Service (PaaS) like **Render**.

1. **Connect Repository:** Link your GitHub repository in the Render dashboard.
2. **Environment:** Choose the `Docker` environment.
3. **Environment Variables:** Provide all necessary keys (Database, Redis, `SECRET_KEY`, etc.).
4. **Deploy:** Render automatically builds the `Dockerfile` and runs `start.sh`.

See the dedicated deployment guides in the repository (`RENDER_DEPLOYMENT.md`, `KOYEB_DEPLOYMENT.md`, etc.) for more details.

---

## 📖 API Documentation

### Create Short URL
* **URL:** `/api/shorten/`
* **Method:** `POST`
* **Body:**
  ```json
  {
    "original_url": "https://example.com/very/long/path",
    "custom_code": "mycode", 
    "expiry_date": "2024-12-31T23:59:59Z"
  }
  ```

### Get URL Analytics
* **URL:** `/api/analytics/<short_code>/`
* **Method:** `GET`
* **Response:**
  ```json
  {
    "short_code": "mycode",
    "original_url": "https://example.com/...",
    "total_clicks": 150,
    "recent_clicks": [...]
  }
  ```

### Redirect
* **URL:** `/<short_code>/`
* **Method:** `GET`
* **Action:** Redirects to the original URL (HTTP 302) while tracking the click.

---

## 👨‍💻 Developer & Author

Designed and developed by **Gaurav Verma**.

Connect with me to discuss scalable system design, full-stack development, and cloud deployments!

---

## 📄 License

This project is licensed under the MIT License - see the LICENSE file for details.
