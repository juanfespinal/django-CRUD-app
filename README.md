# CleanRecruit - Recruitment Management System 🚀

**CleanRecruit** is a modern, high-performance recruitment management system designed for cleaning companies. It streamlines the hiring process by tracking candidates through every stage of the pipeline, managing job positions, and scheduling interviews with a slick, responsive interface.

Built with **Django**, **HTMX**, and **Alpine.js**, it provides a seamless single-page application (SPA) experience without the complexity of a heavy frontend framework.

---

## ✨ Features

- **📊 Analytics Dashboard**: Real-time overview of recruitment metrics, candidate status distribution, and hiring trends.
- **👥 Candidate Tracking**: Complete CRUD for candidates with advanced search, status-based filtering, and staging.
- **💼 Position Management**: Manage job openings across different departments with salary tracking.
- **📅 Interview Scheduling**: Schedule and track interviews with automated status updates.
- **⚡ HTMX Powered**: No-refresh interactions for modals, filtering, and form submission.
- **📱 Responsive Design**: Fully optimized for Desktop, Tablet, and Mobile.
- **🎨 Premium UI**: Modern aesthetic using a professional Teal color palette and IBM Plex Sans typography.

---

## 🛠️ Tech Stack

- **Backend**: Python 3.10+ & Django 4.2+
- **Frontend**: HTMX, Alpine.js, Vanilla CSS
- **Interactions**: HTMX (AJAX-based page updates)
- **Charts**: Chart.js
- **Database**: SQLite3 (Development) / PostgreSQL (Production ready)

---

## 🚀 Getting Started

Follow these steps to set up the project locally for development.

### 1. Prerequisites
- Python 3.10 or higher
- `pip` (Python package manager)

### 2. Installation

Clone the repository and navigate to the project directory:
```bash
git clone <repository-url>
cd django-CRUD-app
```

### 3. Setup Virtual Environment
```bash
# Create venv
python -m venv venv

# Activate venv
# On macOS/Linux:
source venv/bin/activate
# On Windows:
venv\Scripts\activate
```

### 4. Install Dependencies
```bash
pip install -r requirements.txt
```

### 5. Database Migrations
```bash
python manage.py migrate
```

### 6. Create a Superuser
```bash
python manage.py createsuperuser
```

### 7. Run the Development Server
```bash
python manage.py runserver
```

Open [http://127.0.0.1:8000](http://127.0.0.1:8000) in your browser to see the app in action!

---

## 🏗️ Project Structure

```text
django-CRUD-app/
├── cleanrecruit/       # Project configuration (settings, urls, wsgi)
├── recruits/           # Core app (models, views, logic)
├── templates/          # Global templates (base, dashboard, etc.)
├── static/             # Static files (CSS, JS, Images)
├── db.sqlite3          # Local database
├── manage.py           # Django CLI
└── requirements.txt    # dependencies
```

---

## 🌐 Deployment (Railway)

This project is configured to deploy to Railway with:
- **Django + Gunicorn** via `Procfile`
- **PostgreSQL** via Railway `DATABASE_URL`
- **WhiteNoise** for static files

### 1. Create Railway Services
- Create a new Railway project.
- Add a **PostgreSQL** service.
- Add a **GitHub Deploy** service for this repo.

### 2. Set Environment Variables (Web Service)
- `SECRET_KEY` = strong random value
- `DEBUG` = `False`
- `ALLOWED_HOSTS` = `your-app-domain.up.railway.app`
- `CSRF_TRUSTED_ORIGINS` = `https://your-app-domain.up.railway.app`
- `SECURE_SSL_REDIRECT` = `True`

`DATABASE_URL` is injected automatically by Railway PostgreSQL when linked.

### 3. Run Migrations and Collect Static
After first deploy, run:
```bash
python manage.py migrate
python manage.py collectstatic --noinput
```

### 4. Generate Public Domain
In Railway service networking, generate a domain and put it in:
- `ALLOWED_HOSTS`
- `CSRF_TRUSTED_ORIGINS` (with `https://`)

---

## 📝 License

This project is licensed under the MIT License - see the LICENSE file for details.

Developed with ❤️ for the recruitment industry.
