# CODE_INDEX — Important files & snippets

Below is a quick index of critical files, why they matter, and short relevant snippets (approx. lines).

- `website-wag/config/settings.py` — main settings (apps, middleware, auth, DRF, Wagtail)
  - verified: `allauth.account.middleware.AccountMiddleware` is importable/valid with installed `django-allauth`
  - updated: `STATIC_ROOT` + WhiteNoise middleware/static storage are configured
  - updated: `DATABASE_URL` env is parsed via `dj-database-url` with SQLite fallback
  - updated: `SECRET_KEY` is required when `DEBUG=False` (dev-only fallback remains)

- `website-wag/requirements.txt` — pinned deps (Django 4.2, djangorestframework, wagtail, whitenoise, celery, redis)
  - inspect: [website-wag/requirements.txt](website-wag/requirements.txt#L1-L40)

- `website-wag/core/migrations/0001_initial.py` — canonical data schema (Sector, Region, Project, Member, Donation, StaticPage)
  - location: [website-wag/core/migrations/0001_initial.py](website-wag/core/migrations/0001_initial.py#L1-L400)

- `website-wag/core/views.py` + `website-wag/core/urls.py` — actual API implementation and routing
  - implemented endpoints: `/api/sectors`, `/api/regions`, `/api/projects`, `/api/members`, `/api/donations`, `/api/pages`
  - custom actions: `projects/featured`, `projects/active`, `donations/statistics`

- `website-wag/core/admin.py` — admin registrations and customizations
  - location: [website-wag/core/admin.py](website-wag/core/admin.py#L1-L220)

- `website-wag/.env.example` — recommended env vars (DEBUG, SECRET_KEY, DATABASE_URL)
  - location: [website-wag/.env.example](website-wag/.env.example#L1-L60)

- `website-wag/config/urls.py` — root URL map (admin, cms, API, legacy redirects)
  - includes `.html` legacy redirects and Wagtail routing

- `website-wag/templates/site/*.html` — public pages currently served by Django/Wagtail
  - main pages used in current scope: `index`, `projects`, `support`, `join`, `contact`

- `website-wag/static/scripts/lang.js` — client-side language script in current runtime

- `website-wag/website/models.py` — Wagtail page models (`HomePage`, `StandardPage`, `ManagedSitePage`)
  - this is where CMS-managed site structure lives now

Search TODO / FIXME occurrences (developer notes) in repo: use `grep "TODO|FIXME|HACK"` to list; many matches found in vendored libs — focus on project files.
