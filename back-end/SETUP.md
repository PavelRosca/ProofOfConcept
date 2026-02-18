# 🚀 Django Backend - Complete Setup Guide

## 📁 Project Structure Created

```
back-end/
├── config/                  # Django Project Configuration
│   ├── settings.py         # Main Django settings (Italian lang, CORS, etc.)
│   ├── urls.py             # URL routing
│   └── wsgi.py             # WSGI application
│
├── core/                    # Core App - Models & Admin
│   ├── models.py           # Database models:
│   │                         - Sector (sectors: Nord/Centro/Sud)
│   │                         - Region (regions within sectors)
│   │                         - Project (political projects 1-8)
│   │                         - Member (party members with tessera)
│   │                         - Donation (donations tracker)
│   │                         - StaticPage (organization pages)
│   │
│   ├── admin.py            # Django Admin customization
│   ├── migrations/          # Database migrations
│   └── 0001_initial.py     # ✅ Initial models migration
│
├── members/                 # Members App (placeholder)
├── projects/                # Projects App (placeholder)
├── donations/               # Donations App (placeholder)
│
├── manage.py               # Django CLI tool
├── db.sqlite3              # ✅ Database created
├── requirements.txt        # ✅ Python dependencies
├── .env.example            # ✅ Environment variables template
├── .gitignore              # ✅ Git ignore rules
├── setup.sh                # ✅ Setup script
└── README.md               # ✅ Detailed documentation
```

## ✅ What's Already Installed

```
✅ Django Project initialized
✅ 4 Apps created (core, members, projects, donations)
✅ 6 Models created and migrated:
   - Sector (Nord/Centro/Sud regions)
   - Region (locations with contact info)
   - Project (projects 1-8 with budget tracking)
   - Member (members with membership cards - Tessera)
   - Donation (donation tracking system)
   - StaticPage (static content pages)
✅ Custom Django Admin configured with all models
✅ Database initialized (SQLite)
✅ Python environment configured
✅ CORS enabled for frontend (localhost:3000)
✅ Italian language configured
```

## 🎯 Step 1: First Time Setup

### Option A: Automated Setup (Linux/Mac)

```bash
cd back-end
chmod +x setup.sh
./setup.sh
```

This will:
1. Create `.env` file
2. Create virtual environment (if needed)
3. Install requirements
4. Run migrations
5. Create superuser account

### Option B: Manual Setup

```bash
cd back-end

# 1. Create .env file
cp .env.example .env

# 2. Create virtual environment
python3 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# 3. Install requirements
pip install -r requirements.txt

# 4. Run migrations
python manage.py migrate

# 5. Create superuser (admin account)
python manage.py createsuperuser
```

## 🎯 Step 2: Start Development Server

```bash
cd back-end
source venv/bin/activate  # activate virtual environment
python manage.py runserver
```

Server runs at: **http://localhost:8000**

## 🎯 Step 3: Access Admin Panel

1. Open browser: **http://localhost:8000/admin**
2. Login with superuser credentials you created
3. Start adding data:
   - Add Sectors (Nord/Centro/Sud)
   - Add Regions (NORD-01, NORD-02, etc.)
   - Add Projects
   - Add Static Pages (Statute, Privacy, etc.)

## 📊 Database Models Explained

### Sector
```python
- name: str (Piemonte, Campania, etc.)
- region_type: choice (nord/centro/sud)
- description: text
- order: int (for sorting)
```

### Region
```python
- name: str
- code: str (NORD-01, CENTRO-02, etc.)
- sector: FK to Sector
- contact_email: email
- contact_phone: phone
- active: bool
```

### Project
```python
- title: str
- slug: unique slug
- description: text
- status: (planificato/in_corso/completato/sospeso)
- sectors: Many-to-Many to Sector
- budget: decimal
- start_date, end_date: dates
- is_featured: bool
```

### Member
```python
- user: OneToOne to User
- region: FK to Region
- tessera_number: unique (membership card)
- status: (attivo/inattivo/sospeso)
- profile_image: image
```

### Donation
```python
- donor_name, donor_email: str, email
- amount: decimal
- status: (pending/completed/failed/refunded)
- payment_method: str
- member: FK to Member (optional)
- is_anonymous: bool
```

### StaticPage
```python
- title: str
- slug: unique slug
- page_type: (statuto/privacy/garantia/bilanci/etc)
- content: rich text
- is_published: bool
```

## 🔧 Common Commands

```bash
# Create new app
python manage.py startapp app_name

# Create migration for changes
python manage.py makemigrations

# Apply migrations
python manage.py migrate

# Check migrations
python manage.py showmigrations

# Interactive shell
python manage.py shell

# Run tests
python manage.py test

# Collect static files
python manage.py collectstatic

# Clear migrations (CAUTION!)
python manage.py migrate core 0000 --fake
```

## 🔒 Environment Variables

Edit `.env` file:

```bash
# Django
DEBUG=True                              # Set False in production
SECRET_KEY=your-secret-key              # Generate secure key
ALLOWED_HOSTS=localhost,127.0.0.1       # Allowed domains

# Database
DATABASE_URL=sqlite:///db.sqlite3       # Default SQLite
# For PostgreSQL:
# DATABASE_URL=postgresql://user:pass@host:5432/db

# CORS (Frontend URL)
CORS_ALLOWED_ORIGINS=http://localhost:3000

# Email (optional)
EMAIL_HOST=smtp.gmail.com
EMAIL_PORT=587
EMAIL_HOST_USER=your-email@gmail.com
EMAIL_HOST_PASSWORD=your-app-password

# Redis/Celery (optional)
REDIS_URL=redis://localhost:6379/0
```

## 📝 API Development (Phase 2)

Ready for Phase 2 - REST API endpoints will include:

```
GET    /api/sectors/              List all sectors
GET    /api/regions/              List all regions  
GET    /api/projects/             List all projects
GET    /api/projects/{id}/        Project detail
POST   /api/members/register/     Register new member
POST   /api/donations/            Submit donation
GET    /api/pages/{slug}/         Get static page
```

## 🐛 Troubleshooting

### Port 8000 already in use
```bash
python manage.py runserver 8001
```

### Database locked
```bash
rm db.sqlite3
python manage.py migrate
```

### Module not found
```bash
pip install -r requirements.txt
python manage.py migrate
```

### Changes not visible
```bash
python manage.py makemigrations
python manage.py migrate
```

## 📱 Integration with Frontend

Frontend (Gulp/Tailwind) makes requests to:

```
http://localhost:8000/api/...
```

CORS is already configured to accept requests from:
```
http://localhost:3000
```

## 🚢 Moving to Production

1. Change `DEBUG=False` in `.env`
2. Generate secure `SECRET_KEY`
3. Switch to PostgreSQL database
4. Use environment-based settings
5. Collect static files
6. Deploy with Gunicorn + Nginx
7. Add SSL certificate

## 📚 Resources

- Django Docs: https://docs.djangoproject.com/
- Django REST Framework: https://www.django-rest-framework.org/
- django-allauth: https://django-allauth.readthedocs.io/

## ✨ Next Phase

After successful local testing:

1. **Phase 2**: Create REST API endpoints
2. **Phase 3**: Email notifications, Live Chat integration
3. **Phase 4**: Docker containerization, production deployment

---

**Status**: ✅ Phase 1 Complete - Django backend ready!

Last updated: February 2026
