# Partito Politico — website-wag (Django + Wagtail)

Unified web runtime for the project.

## Current state

This app is launched locally from this folder only:

```bash
cd website-wag
python manage.py runserver
```

The project is no longer organized as separate backend/frontend runtime folders.
Public pages are served by Django/Wagtail templates and static assets.

## Tech stack

- Django 4.2
- Django REST Framework
- Wagtail CMS
- django-allauth
- WhiteNoise
- SQLite by default (`DATABASE_URL` supported via `dj-database-url`)

## Main structure

```text
website-wag/
├── config/              # Django settings + urls + utility views
├── core/                # Domain models + DRF serializers/views/urls
├── website/             # Wagtail page models
├── members/             # Placeholder app
├── projects/            # Placeholder app
├── donations/           # Placeholder app
├── templates/           # Site templates (site/, cms/)
├── static/              # CSS/JS/images
├── manage.py
└── requirements.txt
```

## Active endpoints

- `GET /api/sectors/`
- `GET /api/regions/`
- `GET /api/projects/`
- `GET /api/projects/{id}/`
- `GET /api/projects/featured/`
- `GET /api/projects/active/`
- `GET /api/members/` (read-only)
- `GET/POST /api/donations/`
- `GET /api/donations/statistics/`
- `GET /api/pages/`
- `GET /api-status/`

Auth/admin routes:
- `/admin/` (Django admin)
- `/cms/` (Wagtail admin)
- `/api/auth/` (DRF session auth)
- `/accounts/` (allauth)

## Quick start

```bash
cd website-wag
python -m venv venv
# Windows: venv\Scripts\activate
# Linux/macOS: source venv/bin/activate
pip install -r requirements.txt
cp .env.example .env
python manage.py migrate
python manage.py createsuperuser
python manage.py runserver
```

## Notes

- Core business logic currently lives in `core`.
- `members/projects/donations` are mostly placeholders.
- Production hardening and broader automated tests are still pending.
