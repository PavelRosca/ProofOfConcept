# Partito Politico - Backend (Django)

Italian Political Party Website - Django Backend

## 📋 Project Structure

```
back-end/
├── config/              # Django project settings
│   ├── settings.py      # Main configuration
│   ├── urls.py          # URL routing
│   └── wsgi.py          # WSGI application
├── core/                # Core app - Models & Admin
│   ├── models.py        # Database models
│   └── admin.py         # Django Admin configuration
├── members/             # Members/Authentication app
├── projects/            # Projects app
├── donations/           # Donations app
├── manage.py            # Django management script
└── requirements.txt     # Python dependencies
```

## 🎯 Models Overview

- **Sector**: Political sectors (Nord, Centro, Sud)
- **Region**: Regions within sectors (e.g., NORD-01 to NORD-08)
- **Project**: Political party projects (1-8)
- **Member**: Party members with membership cards (Tessera)
- **Donation**: Donations from supporters
- **StaticPage**: Organization pages (Statute, Privacy, etc.)

## 🚀 Quick Start

### 1. Create `.env` file

```bash
cp .env.example .env
```

Edit `.env` with your settings:

```bash
DEBUG=True
SECRET_KEY=your-secret-key-here
ALLOWED_HOSTS=localhost,127.0.0.1,localhost:3000
DATABASE_URL=sqlite:///db.sqlite3
```

### 2. Run migrations

```bash
python manage.py migrate
```

### 3. Create superuser (admin)

```bash
python manage.py createsuperuser
```

Example:
```
Username: admin
Email: admin@example.com
Password: ****
```

### 4. Start development server

```bash
python manage.py runserver
```

Server runs at: **http://localhost:8000**

Admin panel: **http://localhost:8000/admin**

## 📱 API Endpoints (Phase 2)

*To be implemented:*

```
GET    /api/sectors/           - List all sectors
GET    /api/regions/           - List all regions
GET    /api/projects/          - List all projects
GET    /api/projects/{id}/     - Project detail
POST   /api/members/register   - Register member
POST   /api/donations/         - Make donation
GET    /api/pages/{slug}/      - Static pages
```

## 🔐 Django Admin Features

Access at `/admin/`:

- **Sectors Management**: Add, edit, and organize sectors (Nord/Centro/Sud)
- **Regions Management**: Add regions with contact info
- **Projects**: Create projects with budget and timeline tracking
- **Members**: Manage members and their membership cards
- **Donations**: Track donations with payment status
- **Static Pages**: Manage organization pages (Statute, Privacy, etc.)

## 🛠 Development Workflow

### Make changes to models

```bash
python manage.py makemigrations
python manage.py migrate
```

### Create test data

```bash
python manage.py shell
>>> from core.models import Sector, Region
>>> s = Sector.objects.create(name="Piemonte", region_type="nord")
>>> r = Region.objects.create(name="Turin", code="NORD-01", sector=s)
>>> r.save()
```

### Run tests

```bash
python manage.py test
```

## 📦 Dependencies

- **Django 4.2**: Web framework
- **djangorestframework**: REST API
- **django-cors-headers**: CORS support for frontend
- **django-allauth**: Authentication
- **django-crispy-forms**: Form rendering
- **Pillow**: Image processing
- **psycopg2**: PostgreSQL support (production)
- **Celery**: Background tasks
- **Redis**: Caching & Celery broker

## 🚢 Production Deployment

### Using PostgreSQL

1. Update `.env`:

```bash
DATABASE_URL=postgresql://user:password@localhost:5432/party_db
DEBUG=False
SECRET_KEY=your-super-secret-key
```

2. Install production dependencies:

```bash
pip install -r requirements.txt
```

3. Collect static files:

```bash
python manage.py collectstatic --noinput
```

4. Migration to production database:

```bash
python manage.py migrate
python manage.py createsuperuser
```

### Using Docker

```dockerfile
FROM python:3.10
WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt
COPY . .
CMD ["gunicorn", "config.wsgi:application", "--bind", "0.0.0.0:8000"]
```

Run with:

```bash
docker build -t party-backend .
docker run -p 8000:8000 party-backend
```

## 🔒 Security Checklist

- [ ] Change `SECRET_KEY` in production
- [ ] Set `DEBUG=False` in production
- [ ] Configure allowed hosts
- [ ] Use HTTPS/SSL
- [ ] Configure password validators
- [ ] Set up email notifications
- [ ] Enable CSRF protection
- [ ] Use environment variables for secrets

## 📚 Useful Commands

```bash
# Create superuser
python manage.py createsuperuser

# Create app
python manage.py startapp app_name

# Make migrations
python manage.py makemigrations

# Apply migrations
python manage.py migrate

# Shell access
python manage.py shell

# Run tests
python manage.py test

# Collect static files
python manage.py collectstatic

# Clear database
python manage.py flush

# Create backup
python manage.py dumpdata > backup.json

# Restore backup
python manage.py loaddata backup.json
```

## 🐛 Troubleshooting

### Port 8000 already in use:

```bash
python manage.py runserver 8001
```

### Database locked:

```bash
rm db.sqlite3
python manage.py migrate
```

### Missing migrations:

```bash
python manage.py makemigrations
python manage.py migrate
```

## 📞 Support

For issues or questions, check:
- Django Documentation: https://docs.djangoproject.com/
- DRF Documentation: https://www.django-rest-framework.org/
- Admin Panel for data management

## 📝 Next Steps

1. **Phase 1** ✅ Models & Django Admin
2. **Phase 2** → Create REST API endpoints
3. **Phase 3** → Email notifications & Live Chat
4. **Phase 4** → Docker & Production deployment

---

Last updated: February 2026
