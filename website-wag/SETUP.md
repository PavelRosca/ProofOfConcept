# Setup Guide — website-wag

## 1) Prerequisites

- Python 3.10+
- pip

## 2) Local install

```bash
cd website-wag
python -m venv venv
# Windows
venv\Scripts\activate
# Linux/macOS
# source venv/bin/activate

pip install -r requirements.txt
cp .env.example .env
python manage.py migrate
python manage.py createsuperuser
```

## 3) Run

```bash
python manage.py runserver
```

Open:
- Site: http://127.0.0.1:8000/
- Django admin: http://127.0.0.1:8000/admin/
- Wagtail admin: http://127.0.0.1:8000/cms/
- API status: http://127.0.0.1:8000/api-status/

## 4) Environment variables (.env)

Minimum recommended local values:

```bash
DEBUG=True
SECRET_KEY=change-me-local
ALLOWED_HOSTS=localhost,127.0.0.1
DATABASE_URL=sqlite:///db.sqlite3
```

Optional:

```bash
CORS_ALLOWED_ORIGINS=http://localhost:3000,http://127.0.0.1:3000
WAGTAILADMIN_BASE_URL=http://127.0.0.1:8000
```

## 5) Useful commands

```bash
python manage.py check
python manage.py test
python manage.py makemigrations
python manage.py migrate
python manage.py collectstatic --noinput
```

## 6) Current implementation notes

- API endpoints in `core` are already active (not "phase 2 pending").
- Public pages are served by templates in `templates/site/`.
- Legacy `*.html` routes are redirected to clean paths.
- Core domain remains centralized in `core`; app split is pending architectural decision.

## 7) Production checklist (high level)

- Set `DEBUG=False`
- Set strong `SECRET_KEY`
- Set strict `ALLOWED_HOSTS`
- Enable HTTPS hardening (`SECURE_SSL_REDIRECT`, secure cookies, HSTS)
- Use managed PostgreSQL in `DATABASE_URL`
- Add CI and deployment pipeline
