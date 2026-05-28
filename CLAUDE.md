# CLAUDE.md — ProofOfConcept (Partito Politico)

## What This Is

A proof-of-concept web platform for an Italian political party ("Sciarrone"). Handles public content, member management, party projects, donations, and regional organization. Bilingual: Italian (IT) and English (EN).

**Git remote:** `https://github.com/VaraTechRepo/ProofOfConcept.git`  
**Branch:** `main`  
**Python:** 3.12.8

---

## Tech Stack

| Layer | Technology |
|-------|-----------|
| Backend | Django 4.2 + Django REST Framework 3.16 |
| CMS | Wagtail 7.3 + wagtail-localize (IT/EN) |
| Database | SQLite (dev) / PostgreSQL (prod via `DATABASE_URL`) |
| Auth | django-allauth + DRF SessionAuthentication |
| Frontend | Django Templates + Tailwind CSS + vanilla JS |
| Forms | crispy-forms + Bootstrap 5 |
| Static files | WhiteNoise (production) |
| Task queue | Celery + Redis (configured, not yet used) |
| Deployment | Gunicorn on Render.com |

---

## Directory Map

```
ProofOfConcept/               ← git root
├── CLAUDE.md                 ← this file
├── website-wag/              ← Django project root (run everything from here)
│   ├── config/               ← settings.py, urls.py, wsgi.py, asgi.py
│   ├── core/                 ← ALL business logic: models, API viewsets, serializers, admin
│   ├── website/              ← Wagtail CMS page models + StreamField blocks
│   ├── members/              ← empty scaffold (models live in core)
│   ├── projects/             ← empty scaffold (models live in core)
│   ├── donations/            ← empty scaffold (models live in core)
│   ├── templates/
│   │   ├── site/             ← 23 public HTML templates (base, index, about, blog, etc.)
│   │   └── cms/              ← Wagtail admin overrides
│   ├── static/
│   │   ├── styles/main.css   ← compiled Tailwind CSS
│   │   ├── scripts/main.js   ← theme toggle, carousel, scroll animations
│   │   ├── scripts/lang.js   ← IT/EN language switcher
│   │   └── plugins/          ← Swiper, jQuery, Font Awesome
│   ├── .env.example          ← copy to .env for local dev
│   ├── requirements.txt      ← 18 pinned dependencies
│   ├── manage.py
│   ├── SETUP.md              ← full Windows setup guide (human reference)
│   └── SETUP-IT.md           ← Italian quick-start guide
└── runtime.txt               ← python-3.12.8 (Render.com)
```

---

## How to Run

```powershell
cd website-wag
.venv\Scripts\Activate.ps1          # Windows
# source .venv/bin/activate         # Linux/macOS
pip install -r requirements.txt
cp .env.example .env                # then edit .env
python manage.py migrate
python manage.py createsuperuser
python manage.py runserver
```

| URL | Purpose |
|-----|---------|
| `http://127.0.0.1:8000/` | Public site (redirects to `/en/`) |
| `http://127.0.0.1:8000/admin/` | Django admin |
| `http://127.0.0.1:8000/cms/` | Wagtail CMS |
| `http://127.0.0.1:8000/api/` | REST API root |
| `http://127.0.0.1:8000/api-status/` | Health check |

---

## Data Models

All models are in `core/models.py`.

| Model | Key Fields | Notes |
|-------|-----------|-------|
| `Sector` | name, region_type (nord/centro/sud_isole), order | Party macro-regions |
| `Region` | name, code, sector (FK), contact_email, phone, active | Sub-divisions |
| `Project` | title, slug, status, sectors (M2M), budget, start/end_date, is_featured | status choices: pianificato / in_corso / completato / sospeso |
| `Member` | user (OneToOne), region (FK), tessera_number, status, phone | status: attivo / inattivo / sospeso |
| `Donation` | donor_name, amount, currency, status, payment_method, transaction_id, is_anonymous, member (FK optional) | status: pending / completed / failed / refunded |
| `StaticPage` | slug, title, page_type, content, is_published | page_type: statuto / privacy / commissione_garanzia / rendiconto / contributi / regolamento_iscrizioni / regolamento_congresso / contatti |

---

## API Endpoints

Base: `/api/`  Auth: `IsAuthenticatedOrReadOnly` (session-based)

| Endpoint | Methods | Notes |
|----------|---------|-------|
| `/api/sectors/` | GET | list + detail |
| `/api/sectors/{id}/regions/` | GET | custom action |
| `/api/regions/` | GET | list + detail |
| `/api/regions/{id}/members/` | GET | custom action |
| `/api/projects/` | GET | filterable, searchable, orderable |
| `/api/projects/featured/` | GET | is_featured=True |
| `/api/projects/active/` | GET | status=in_corso |
| `/api/members/` | GET | read-only |
| `/api/donations/` | GET, POST | requires `ENABLE_DONATIONS_API=True` in .env |
| `/api/donations/statistics/` | GET | requires same flag |
| `/api/pages/` | GET | StaticPage list + detail |
| `/api/auth/` | — | DRF session auth |
| `/api-status/` | GET | health check, returns JSON |

All list endpoints support `?search=`, `?ordering=`, and django-filter params.

---

## Apps Status

| App | Status | Where the code actually lives |
|-----|--------|-------------------------------|
| `core` | **Active** — all models, ViewSets, serializers, admin | `core/models.py`, `core/views.py`, `core/serializers.py`, `core/admin.py` |
| `website` | **Active** — Wagtail page types + StreamField blocks | `website/models.py`, `website/blocks.py` |
| `members` | **Empty scaffold** | models in `core`; no registration flow yet |
| `projects` | **Empty scaffold** | models in `core`; admin-only management |
| `donations` | **Empty scaffold** | models in `core`; API disabled by default |

**Architecture decision pending:** keep all logic in `core` vs split into dedicated apps. Either is valid; decide before adding new features.

---

## Key Files

| File | Role |
|------|------|
| `config/settings.py` | All Django config — apps, middleware, db, auth, security |
| `config/urls.py` | Root routing: `/admin/`, `/cms/`, `/api/`, `/accounts/`, `/pages/<slug>/`, `/<lang>/` |
| `config/views.py` | `cms_page` view (renders Wagtail pages) + `api_status` view |
| `core/models.py` | Single source of truth for all data models |
| `core/views.py` | DRF ViewSets for all API endpoints |
| `core/serializers.py` | Nested serializers (user data in members, region in sectors) |
| `core/admin.py` | Custom admin: list_display, list_filter, search_fields, fieldsets |
| `core/urls.py` | DRF DefaultRouter wiring |
| `website/models.py` | `HomePage`, `StandardPage`, `ManagedSitePage` (Wagtail) |
| `website/blocks.py` | `CTASectionBlock`, `CardsGridBlock`, `FAQBlock`, `ImageTextSplitBlock` |
| `templates/site/base.html` | Base template — Tailwind, Font Awesome 6, Swiper, dark mode toggle |
| `static/scripts/lang.js` | Client-side IT/EN language switcher (localStorage + cookie) |
| `.env.example` | Full reference for all env vars |

---

## Environment Variables

Copy `.env.example` to `.env`. Key vars:

| Variable | Default | Notes |
|----------|---------|-------|
| `DEBUG` | `True` | Set `False` in production |
| `SECRET_KEY` | *(required)* | Generate with `python -c "from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())"` |
| `ALLOWED_HOSTS` | `localhost,127.0.0.1` | Comma-separated |
| `DATABASE_URL` | *(empty = SQLite)* | Set to `postgres://...` for production |
| `ENABLE_DONATIONS_API` | `False` | Set `True` to expose `/api/donations/` |
| `CORS_ALLOWED_ORIGINS` | *(empty)* | Comma-separated origins |
| `SECURE_SSL_REDIRECT` | `False` | `True` in production |
| `SESSION_COOKIE_SECURE` | `False` | `True` in production |
| `CSRF_COOKIE_SECURE` | `False` | `True` in production |
| `SECURE_HSTS_SECONDS` | `0` | Set to `31536000` in production |

---

## Development Workflow

```powershell
# After changing models
python manage.py makemigrations
python manage.py migrate

# Django shell
python manage.py shell

# Check for issues
python manage.py check

# Collect static (only needed for production / WhiteNoise test)
python manage.py collectstatic --noinput
```

**Checklist before committing:**
- [ ] `python manage.py check` passes
- [ ] New models have migrations
- [ ] `.env` secrets not committed (covered by `.gitignore`)
- [ ] No hardcoded `SECRET_KEY` or credentials in code

---

## Security Notes

| Item | Status |
|------|--------|
| `SECRET_KEY` | Loaded from `.env` — never hardcoded |
| Database | SQLite dev / PostgreSQL prod via `DATABASE_URL` |
| Static files | WhiteNoise — no separate web server needed |
| HTTPS / SSL | Available via `.env` flags — **not enabled by default** |
| HSTS | Available via `.env` flags — **not enabled by default** |
| Secure cookies | Available via `.env` flags — **not enabled by default** |
| CORS | `django-cors-headers` — configure `CORS_ALLOWED_ORIGINS` |
| Payment processing | **Not implemented** — no Stripe/PayPal integration |
| Celery/Redis | Configured but unused — secure before enabling |
| `.env.example` | Contains placeholder values only — safe to commit |

**Production hardening checklist (Render.com):**
Set these in environment: `DEBUG=False`, `SECURE_SSL_REDIRECT=True`, `SESSION_COOKIE_SECURE=True`, `CSRF_COOKIE_SECURE=True`, `SECURE_HSTS_SECONDS=31536000`, `SECURE_HSTS_INCLUDE_SUBDOMAINS=True`, `SECURE_HSTS_PRELOAD=True`

---

## Sharing the Site Publicly

### Option A — Instant tunnel (temporary, works while PC is on)

Make sure the local server is running first (`python manage.py runserver`), then open a **second terminal** and run:

```powershell
# No account needed — works immediately
ssh -o StrictHostKeyChecking=no -R 80:localhost:8000 serveo.net
```

The terminal will print a public URL like `https://xxxx.serveousercontent.com`.
Share that URL. It stays alive as long as that terminal window is open.
Visitors see a warning page on first load — they click "Visit Site" to continue.

**Note:** `settings.py` is configured to set `ALLOWED_HOSTS = ['*']` when `DEBUG=True`, so any tunnel domain is accepted automatically. In production (`DEBUG=False`) the strict host list applies.

```powershell
# Alternative: ngrok (requires free account at ngrok.com)
# After logging in and running: ngrok config add-authtoken <TOKEN>
ngrok http 8000
```

### Option B — Render.com (permanent, always-on)

**One-time setup in the Render dashboard:**
1. New → Web Service → connect `VaraTechRepo/ProofOfConcept`
2. Root Directory: `website-wag`
3. Build Command: `pip install -r requirements.txt && python manage.py collectstatic --noinput`
4. Start Command: `python manage.py migrate && gunicorn config.wsgi:application --bind 0.0.0.0:$PORT`
5. Health Check Path: `/api-status/`

**Environment variables (set in Render dashboard):**

| Key | Value |
|-----|-------|
| `DEBUG` | `False` |
| `SECRET_KEY` | Generate: `python -c "from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())"` |
| `PUBLIC_DEMO` | `True` |
| `DATABASE_URL` | Create a free Render PostgreSQL → paste the connection URL |

**After first deploy — create admin user via Render Shell tab:**
```bash
python manage.py createsuperuser
```

---

## Roadmap / TODO

### Phase 1 — Foundation (complete)
- [x] Unified Django/Wagtail runtime in `website-wag/`
- [x] REST API for all core models
- [x] Django admin with custom interfaces
- [x] Wagtail CMS with IT/EN localization
- [x] WhiteNoise static serving
- [x] Environment-based config

### Phase 2 — Core Workflows (pending)
- [ ] Member registration form wired to `Member` model
- [ ] Contact / Support / Join form POST handlers
- [ ] Email notifications (Celery task for sign-up confirmation)
- [ ] Automated tests (models, API endpoints, views)

### Phase 3 — Features (pending)
- [ ] Payment integration (Stripe or PayPal) for donations
- [ ] Admin dashboards (member counts, donation totals)
- [ ] App architecture decision: keep logic in `core` vs split to `members/projects/donations`

### Phase 4 — Infrastructure (pending)
- [ ] Docker containerization
- [ ] CI/CD pipeline (GitHub Actions)
- [ ] Production security hardening (see Security Notes)
- [ ] Celery/Redis activation for async tasks

---

## Known Issues & Sessions

### 2026-03-04 — i18n Language Switch Bug
**Problem:** Bilingual EN/IT language switch broke after CMS edits.  
**Root causes identified:**
1. Client-side `lang.js` toggling was overriding Wagtail's server-side locale routing
2. `wagtail_localize` table missing: `no such table wagtail_localize_translatableobject`
3. Middleware cookie handling conflicting with Wagtail i18n patterns

**Fixes applied:** `settings.py` (i18n middleware order), `urls.py` (i18n patterns), `lang.js` (cookie path), `base.html` (hreflang), `requirements.txt` (added `wagtail-localize`)  
**Migration:** `python manage.py migrate` required after adding `wagtail-localize`  
**Status:** Resolved. CMS content may need manual re-translation in Wagtail admin if locale data was lost.

---

## Archived Notes

The following topics were previously tracked in separate files and are now superseded:
- **Old frontend folder** — there is no separate frontend. Public pages are `templates/site/`, static assets are `static/`. This was reorganized in early 2026.
- **CHECKPOINT.md / WHOLE_PROJECT_DESCRIPTION.txt** — historical snapshots; current state is reflected in this file.
