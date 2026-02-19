# CODE_INDEX — Important files & snippets

Below is a quick index of critical files, why they matter, and short relevant snippets (approx. lines).

- `back-end/config/settings.py` — main settings (apps, middleware, auth, DRF)
  - verified: `allauth.account.middleware.AccountMiddleware` is importable/valid with installed `django-allauth`
  - updated: `STATIC_ROOT` + WhiteNoise middleware/static storage are configured
  - updated: `DATABASE_URL` env is parsed via `dj-database-url` with SQLite fallback
  - updated: `SECRET_KEY` is required when `DEBUG=False` (dev-only fallback remains)

- `back-end/requirements.txt` — pinned deps (Django 4.2, djangorestframework, whitenoise, celery, redis)
  - inspect: [back-end/requirements.txt](back-end/requirements.txt#L1-L30)

- `back-end/core/migrations/0001_initial.py` — canonical data schema (Sector, Region, Project, Member, Donation, StaticPage)
  - location: [back-end/core/migrations/0001_initial.py](back-end/core/migrations/0001_initial.py#L1-L400)

- `back-end/core/views.py` + `back-end/core/urls.py` — actual API implementation and routing
  - implemented endpoints: `/api/sectors`, `/api/regions`, `/api/projects`, `/api/members`, `/api/donations`, `/api/pages`
  - custom actions: `projects/featured`, `projects/active`, `donations/statistics`

- `back-end/core/admin.py` — admin registrations and customizations
  - location: [back-end/core/admin.py](back-end/core/admin.py#L1-L200)

- `back-end/.env.example` — recommended env vars (DEBUG, SECRET_KEY, DATABASE_URL)
  - location: [back-end/.env.example](back-end/.env.example#L1-L40)

- `back-end/config/urls.py` — root URL map + duplicated DEBUG static block
  - verify duplicated block at end of file and dependency on undefined `settings.STATIC_ROOT`

- `front-end/package.json` — frontend dev scripts and dependencies
  - important scripts: `dev`, `build`, `format`
  - verified mismatch: `remove-darkmode` points to `scripts/removeDarkMode.js` and `yarn format`, while file is `scripts/removeDarkmode.js`

- `front-end/gulpfile.js` — Tailwind build tasks (check for `dev` and `build` tasks)
  - location: `front-end/gulpfile.js`

Search TODO / FIXME occurrences (developer notes) in repo: use `grep "TODO|FIXME|HACK"` to list; many matches found in vendored libs — focus on project files.
