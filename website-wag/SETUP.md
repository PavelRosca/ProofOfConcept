# Complete Setup Guide — website-wag (Windows)

**Step-by-step guide to run "Partito Politico" (website-wag) from scratch on Windows**

This is a Django 4.2 + Wagtail CMS project with REST API endpoints. Tested on Python 3.12.8.

---

## Quick Reference

| Component | Value |
|-----------|-------|
| **Framework** | Django 4.2 + Wagtail 7.3 CMS |
| **Python** | 3.12.8+ |
| **Database** | SQLite (default) or PostgreSQL |
| **API** | Django REST Framework |
| **Authentication** | django-allauth |
| **Language** | Italian (it) / English (en) |
| **Timezone** | Europe/Rome |

---

## Table of Contents

1. [Prerequisites](#prerequisites)
2. [Setup Process](#setup-process)
3. [Access the Application](#access-the-application)
4. [Database & Admin](#database--admin)
5. [API Endpoints](#api-endpoints)
6. [Troubleshooting](#troubleshooting)
7. [Development Tips](#development-tips)

---

## Prerequisites

### Python 3.12.8+

Download and install from https://www.python.org/downloads/

**IMPORTANT**: During installation, check **"Add Python to PATH"**

Verify installation in PowerShell:
```powershell
python --version
```

Expected output:
```
Python 3.12.8
```

If not showing 3.12+, reinstall Python with PATH option checked.

### Windows PowerShell or CMD

This guide uses PowerShell examples, but CMD works identically.

---

## Setup Process

### Step 1: Extract Project

1. Extract `website-wag.zip` to a folder (e.g., `C:\Users\YourName\website-wag`)
2. Open PowerShell
3. Navigate to the project:
   ```powershell
   cd C:\path\to\website-wag
   ```

### Step 2: Activate Virtual Environment

A virtual environment (`venv`) is already included. Activate it:

```powershell
.\.venv\Scripts\activate
```

Or if that doesn't work, try:
```powershell
.venv\Scripts\activate.ps1
```

**Success looks like this:**
```
(.venv) PS C:\Users\YourName\website-wag>
```

Notice `(.venv)` at the beginning of your prompt.

**If you see an error about execution policies**, run this first:
```powershell
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser
```

Then try activating again.

### Step 3: Install Python Dependencies

With the virtual environment activated, install all required packages:

```powershell
pip install -r requirements.txt
```

**This installs:**
- Django 4.2
- Wagtail 7.3 (CMS)
- Django REST Framework (API)
- django-allauth (authentication)
- Pillow (image processing)
- psycopg2-binary (PostgreSQL support, optional)
- WhiteNoise (static file serving)
- Celery (async tasks, optional)
- And 20+ other dependencies

This may take 2-5 minutes. If you get errors, see [Troubleshooting](#troubleshooting).

### Step 4: Create `.env` Configuration File

Django reads settings from a `.env` file. A template exists: `.env.example`

**Option A: Manual (Recommended for first-time setup)**

1. Copy the template:
   ```powershell
   cp .env.example .env
   ```

2. Open `.env` in a text editor and set minimum required values:
   ```
   DEBUG=True
   PUBLIC_DEMO=False
   SECRET_KEY=your-local-dev-secret-key-change-in-production
   ALLOWED_HOSTS=localhost,127.0.0.1
   DATABASE_URL=sqlite:///db.sqlite3
   ENABLE_DONATIONS_API=False
   ```

**Option B: Quick setup (defaults work for local development)**

```powershell
cp .env.example .env
```

The `.env.example` already has good local defaults.

### Step 5: Run Database Migrations

The database schema is defined in migrations. Apply them:

```powershell
python manage.py migrate
```

**Expected output:**
```
Running migrations:
  Applying contenttypes.0001_initial... OK
  Applying auth.0001_initial... OK
  Applying admin.0001_initial... OK
  Applying admin.0002_logentry_remove_auto_add... OK
  Applying auth.0002_alter_permission_options... OK
  ...
  (30-40 more migrations)
  ...
Operation to perform:
  Apply all migrations: [all apps]
```

This creates tables for:
- **core**: Sectors, Regions, Projects, Members, Donations, StaticPages
- **website**: Wagtail CMS pages
- **auth**: Django users and permissions
- **wagtail**: CMS admin interface and content
- **allauth**: User accounts and social auth

### Step 6: Create Admin Account (Superuser)

Create the first user who can access Django Admin and Wagtail CMS:

```powershell
python manage.py createsuperuser
```

Follow the prompts:
```
Username: admin
Email address: admin@example.com
Password: 
Password (again): 
Superuser created successfully.
```

**Save your credentials!** You'll use them to log in.

**Example (for testing):**
- Username: `admin`
- Email: `admin@example.com`
- Password: `TestPassword123!`

### Step 7: Collect Static Files (Optional but Recommended)

This gathers CSS, JavaScript, and images for production-like serving:

```powershell
python manage.py collectstatic --noinput
```

Expected output:
```
121 static files copied to '.\staticfiles', 121 post-processed.
```

---

## Start Development Server

Run the Django development server:

```powershell
python manage.py runserver
```

**Expected output:**
```
Watching for file changes with StatReloader
Performing system checks...

System check identified no issues (0 silenced).
Starting development server at http://127.0.0.1:8000/
Quit the server with CTRL-BREAK.
```

**The server is now running!** ✅

Leave this terminal running. Open a new terminal for other commands.

---

## Access the Application

Open your web browser and visit:

| Interface | URL | Purpose |
|-----------|-----|---------|
| **Public Site** | http://127.0.0.1:8000/ | Visitor-facing website |
| **Wagtail CMS** | http://127.0.0.1:8000/cms/ | Manage pages, content, media |
| **Django Admin** | http://127.0.0.1:8000/admin/ | Manage models, users, data |
| **API Base** | http://127.0.0.1:8000/api/ | REST API endpoints |
| **API Status** | http://127.0.0.1:8000/api-status/ | Check API health |

**Log in** with the superuser credentials you created in Step 6.

### Wagtail CMS (http://127.0.0.1:8000/cms/)

This is where you:
- Create and edit pages
- Manage media (images, documents)
- Configure site settings
- Manage user accounts

### Django Admin (http://127.0.0.1:8000/admin/)

This is where you:
- Edit Sectors (political regions)
- Edit Regions (sub-divisions)
- Manage Projects
- Manage Members
- View Donations (if enabled)
- Manage StaticPages (Statuto, Privacy, etc.)
- Manage Users and Groups

---

## Database & Admin

### What's in the Database

The project models (from `core/models.py`):

| Model | Purpose | Editable in |
|-------|---------|-------------|
| **Sector** | Political party regions (Nord, Centro, Sud/Isole) | Django Admin |
| **Region** | Sub-regions within sectors | Django Admin |
| **Project** | Political initiatives/plans | Django Admin |
| **Member** | Party members (tessera holders) | Django Admin |
| **Donation** | Donations to the party (optional) | Django Admin |
| **StaticPage** | Statute, Privacy, Contact info, Regulations | Django Admin |

### Useful Admin Commands

| Command | Purpose |
|---------|---------|
| `python manage.py check` | Verify project configuration |
| `python manage.py test` | Run test suite |
| `python manage.py makemigrations` | Create new database migrations |
| `python manage.py migrate` | Apply migrations to database |
| `python manage.py createsuperuser` | Create another admin user |
| `python manage.py shell` | Interactive Python shell with Django context |
| `python manage.py dbshell` | Interactive database shell (SQLite) |

Example: Check project health
```powershell
python manage.py check
```

Should output:
```
System check identified no issues (0 silenced).
```

---

## API Endpoints

The REST API is at `http://127.0.0.1:8000/api/`

### Available Endpoints

| Endpoint | Method | Purpose |
|----------|--------|---------|
| `/api/sectors/` | GET | List all sectors with region types |
| `/api/sectors/{id}/` | GET | Get single sector details |
| `/api/sectors/{id}/regions/` | GET | Get regions for a sector |
| `/api/regions/` | GET | List all regions |
| `/api/regions/{id}/members/` | GET | Get members in a region |
| `/api/projects/` | GET | List all projects |
| `/api/projects/{id}/` | GET | Get project details |
| `/api/projects/featured/` | GET | Get featured projects only |
| `/api/projects/active/` | GET | Get active (in_corso) projects |
| `/api/members/` | GET | List all members |
| `/api/members/{id}/` | GET | Get member details |
| `/api/pages/` | GET | List static pages (Statute, Privacy, etc.) |
| `/api/pages/{id}/` | GET | Get page content |
| `/api/donations/` | GET, POST | Manage donations (if `ENABLE_DONATIONS_API=True`) |

### Example API Calls

**Get all sectors:**
```powershell
curl http://127.0.0.1:8000/api/sectors/
```

**Get featured projects:**
```powershell
curl http://127.0.0.1:8000/api/projects/featured/
```

**Filter active projects:**
```powershell
curl "http://127.0.0.1:8000/api/projects/?status=in_corso"
```

**Search in member names:**
```powershell
curl "http://127.0.0.1:8000/api/members/?search=mario"
```

---

## Stop the Server

Press `CTRL+BREAK` (or `CTRL+C`) in the terminal where the server is running:

```
Quit the server with CTRL-BREAK.
^C
```

---

## Restarting After Closing

If you closed the terminal and want to restart:

1. Open PowerShell and navigate to the project:
   ```powershell
   cd C:\path\to\website-wag
   ```

2. Activate the virtual environment:
   ```powershell
   .venv\Scripts\activate
   ```

3. Start the server:
   ```powershell
   python manage.py runserver
   ```

---

## Environment Variables Reference

The `.env` file controls all configuration. See `.env.example` for all options.

### Local Development (Minimum)

```
DEBUG=True
SECRET_KEY=change-me-in-production
ALLOWED_HOSTS=localhost,127.0.0.1
DATABASE_URL=sqlite:///db.sqlite3
```

### Features (Optional)

```
# Enable donations API (set to False by default)
ENABLE_DONATIONS_API=False

# CORS (if using a separate frontend)
CORS_ALLOWED_ORIGINS=http://localhost:3000,http://127.0.0.1:3000
CSRF_TRUSTED_ORIGINS=http://localhost:8000,http://127.0.0.1:8000

# Email (optional)
EMAIL_BACKEND=django.core.mail.backends.console.EmailBackend

# Redis caching (optional)
REDIS_URL=redis://localhost:6379/0
```

### Production (When Deploying)

```
DEBUG=False
PUBLIC_DEMO=False
SECRET_KEY=<generate-long-random-string>
ALLOWED_HOSTS=your-domain.com,www.your-domain.com
DATABASE_URL=postgresql://user:pass@host:5432/dbname
SECURE_SSL_REDIRECT=True
SESSION_COOKIE_SECURE=True
CSRF_COOKIE_SECURE=True
```

---

## Troubleshooting

### ❌ "Python not found"

**Problem:** Command not recognized when running `python --version`

**Solution:**
1. Python wasn't added to PATH during installation
2. Reinstall Python from https://www.python.org/downloads/
3. **Check "Add Python to PATH"** during setup
4. Restart PowerShell after reinstalling

### ❌ Execution Policy Error

**Problem:** 
```
cannot be loaded because running scripts is disabled on this system
```

**Solution:**
```powershell
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser
```

Then try activating venv again.

### ❌ "No module named 'django'"

**Problem:** Import error after activating venv

**Solution:**
1. Verify venv is activated (you should see `(.venv)` in prompt)
2. Install dependencies:
   ```powershell
   pip install -r requirements.txt
   ```
3. If still failing, recreate the venv:
   ```powershell
   rm -r .venv
   python -m venv .venv
   .venv\Scripts\activate
   pip install -r requirements.txt
   ```

### ❌ Port 8000 Already In Use

**Problem:**
```
OSError: [WinError 10048] Only one usage of each socket address
```

**Solution:** Run on a different port:
```powershell
python manage.py runserver 8001
```

Then visit http://127.0.0.1:8001/

### ❌ "db.sqlite3 permission denied"

**Problem:** Can't write to database

**Solution:**
1. Close any other applications using the database
2. Check file permissions:
   ```powershell
   icacls db.sqlite3
   ```
3. If needed, delete and recreate:
   ```powershell
   rm db.sqlite3
   python manage.py migrate
   python manage.py createsuperuser
   ```

### ❌ Static Files Not Loading (CSS/Images Broken)

**Problem:** Site looks unstyled

**Solution:**
```powershell
python manage.py collectstatic --noinput
```

Then refresh the browser (Ctrl+F5 for hard refresh).

### ❌ Database Migration Errors

**Problem:**
```
AttributeError: 'NoneType' object has no attribute 'add'
```

**Solution:**
```powershell
python manage.py migrate --fake-initial
```

Or reset database:
```powershell
rm db.sqlite3
python manage.py migrate
```

### ❌ Superuser Already Exists

**Problem:** Can't create superuser because one already exists

**Solution:** You can skip creating another, or delete the old one:
```powershell
python manage.py shell
```

In the Python shell:
```python
from django.contrib.auth.models import User
User.objects.filter(username='admin').delete()
exit()
```

Then create a new one:
```powershell
python manage.py createsuperuser
```

### ❌ Wagtail Admin Blank/Broken

**Problem:** CMS pages show errors

**Solution:**
1. Clear browser cache (Ctrl+Shift+Delete)
2. Restart server
3. Ensure migrations ran:
   ```powershell
   python manage.py makemigrations website
   python manage.py migrate website
   ```

---

## Development Tips

### Quick Folder Navigation

To avoid typing long paths:

1. In File Explorer, go to the project folder
2. Hold `Shift` and right-click in empty space
3. Select "Open PowerShell window here"
4. You're already in the right folder!

### Useful Django Shell Commands

Open interactive Python shell with Django context:

```powershell
python manage.py shell
```

Then you can:

```python
from core.models import Project, Sector, Member
from django.contrib.auth.models import User

# List all projects
projects = Project.objects.all()
for p in projects:
    print(p.title)

# Create a test sector
sector = Sector.objects.create(name="Test", region_type="nord")

# Count members
print(f"Total members: {Member.objects.count()}")

# Find users
admin = User.objects.get(username="admin")
print(admin.email)

exit()
```

### Popular Management Commands

```powershell
# Show all available commands
python manage.py help

# List installed apps
python manage.py shell -c "from django.conf import settings; print(settings.INSTALLED_APPS)"

# Check for issues
python manage.py check --deploy

# Run tests (if any exist)
python manage.py test

# Create a new migration (after changing models.py)
python manage.py makemigrations core

# Show SQL for a migration (before applying)
python manage.py sqlmigrate core 0001
```

### Code Changes

When you modify Python files (views, models, etc.):

1. **Automatic reload**: The development server auto-reloads when files change
2. **Database changes**: If you modify `models.py`:
   ```powershell
   python manage.py makemigrations
   python manage.py migrate
   ```
3. **Static files**: CSS/JS changes appear automatically (hard-refresh browser if needed)

### Multiple Terminals

For development, you might need multiple terminals:

**Terminal 1:** Development server
```powershell
python manage.py runserver
```

**Terminal 2:** Run commands
```powershell
python manage.py createsuperuser
python manage.py shell
```

**Terminal 3:** Other tasks (Git, etc.)
```powershell
git status
```

Each needs its own venv activation.

---

## Project Structure

```
website-wag/
├── .venv/                      # Virtual environment (already created)
├── config/                     # Django project settings
│   ├── settings.py            # Main configuration
│   ├── urls.py                # URL routing
│   ├── views.py               # Project-level views
│   ├── wsgi.py                # WSGI server entry point
│   └── asgi.py                # ASGI server entry point
├── core/                       # Main app with models/API
│   ├── models.py              # Sector, Region, Project, Member, Donation, StaticPage
│   ├── views.py               # API ViewSets (REST Framework)
│   ├── serializers.py         # API serializers
│   ├── urls.py                # API routes
│   ├── admin.py               # Django admin configuration
│   └── migrations/            # Database migrations
├── website/                    # Wagtail CMS pages
│   ├── models.py              # HomePage, StandardPage, etc.
│   └── migrations/            # Wagtail migrations
├── members/                    # Placeholder app
├── projects/                   # Placeholder app
├── donations/                  # Placeholder app
├── templates/                  # HTML templates
│   ├── site/                   # Public site templates
│   └── cms/                    # CMS templates
├── static/                     # CSS, JS, images
│   ├── styles/main.css
│   ├── scripts/main.js
│   └── images/
├── manage.py                   # Django command runner
├── requirements.txt            # Python dependencies
├── .env                        # Configuration (create from .env.example)
├── .env.example                # Configuration template
├── db.sqlite3                  # SQLite database
└── SETUP.md                    # This file
```

---

## Next Steps

After setup is complete:

1. **Create content via CMS** (http://127.0.0.1:8000/cms/)
   - Create the home page
   - Add projects
   - Add sectors and regions

2. **Fill in data via Django Admin** (http://127.0.0.1:8000/admin/)
   - Create sectors (Nord, Centro, Sud/Isole)
   - Add regions under sectors
   - Add projects
   - Create member accounts

3. **Test the API** (http://127.0.0.1:8000/api/)
   - Try the endpoints
   - Build a frontend to consume the API

4. **Deploy to production** (see bottom of `.env.example`)
   - Use PostgreSQL instead of SQLite
   - Set DEBUG=False
   - Configure a production web server (Gunicorn + Nginx)
   - Enable HTTPS

---

## Need Help?

- **Django Documentation**: https://docs.djangoproject.com/4.2/
- **Wagtail Documentation**: https://docs.wagtail.org/
- **Django REST Framework**: https://www.django-rest-framework.org/  
- **Project Notes**: See `NOTES/` folder for architecture and design docs

---

**Last Update**: This guide was created for Python 3.12.8, Django 4.2, Wagtail 7.3.

# HTTPS hardening
SECURE_SSL_REDIRECT=True
SESSION_COOKIE_SECURE=True
CSRF_COOKIE_SECURE=True
SECURE_HSTS_SECONDS=31536000
SECURE_HSTS_INCLUDE_SUBDOMAINS=True
SECURE_HSTS_PRELOAD=True

# Wagtail admin base URL
WAGTAILADMIN_BASE_URL=https://your-demo-domain.com
```

Deployment commands:

```bash
python manage.py migrate
python manage.py collectstatic --noinput
python manage.py check --deploy
```
