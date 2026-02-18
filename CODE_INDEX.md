# CODE_INDEX — Important files & snippets

Below is a quick index of critical files, why they matter, and short relevant snippets (approx. lines).

- `back-end/config/settings.py` — main settings (INSTALLED_APPS, MIDDLEWARE, DATABASES, REST_FRAMEWORK)
  - snippet: `os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')` (~[back-end/manage.py](back-end/manage.py#L1-L40))
  - note: `SECRET_KEY = config('SECRET_KEY', default='django-insecure-...')` (~[back-end/config/settings.py](back-end/config/settings.py#L16-L28))

- `back-end/requirements.txt` — pinned deps (Django 4.2, djangorestframework, whitenoise, celery, redis)
  - inspect: [back-end/requirements.txt](back-end/requirements.txt#L1-L30)

- `back-end/core/migrations/0001_initial.py` — canonical model fields (use to derive schema)
  - location: [back-end/core/migrations/0001_initial.py](back-end/core/migrations/0001_initial.py#L1-L400)

- `back-end/core/admin.py` — admin registrations and customizations
  - location: [back-end/core/admin.py](back-end/core/admin.py#L1-L200)

- `back-end/.env.example` — recommended env vars (DEBUG, SECRET_KEY, DATABASE_URL)
  - location: [back-end/.env.example](back-end/.env.example#L1-L40)

- `front-end/package.json` — frontend dev scripts and dependencies
  - important scripts: `dev`, `build`, `format` (~[front-end/package.json](front-end/package.json#L1-L40))

- `front-end/gulpfile.js` — Tailwind build tasks (check for `dev` and `build` tasks)
  - location: `front-end/gulpfile.js`

Search TODO / FIXME occurrences (developer notes) in repo: use `grep "TODO|FIXME|HACK"` to list; many matches found in vendored libs — focus on project files.
