# SECURITY_ISSUES — Observed security concerns

1. SECRET_KEY handling updated (2026-02-19): production now requires `SECRET_KEY` when `DEBUG=False`; dev fallback remains local-only (`django-insecure-dev-only-change-me`). Ensure deployment always injects a strong secret via environment.

2. `.env.example` includes many sensitive keys placeholders. Ensure real `.env` is excluded from git and secrets are REDACTED. See [.env.example](back-end/.env.example#L1-L40).

3. Static files configuration is incomplete: `back-end/config/urls.py` references `settings.STATIC_ROOT` in DEBUG static serving, but `STATIC_ROOT` is not defined in settings. This can break local serving paths and blocks predictable production setup. See [back-end/config/urls.py](back-end/config/urls.py#L1-L40) and [back-end/config/settings.py](back-end/config/settings.py#L1-L200).

4. WhiteNoise is installed but not enabled in middleware/static storage settings. `collectstatic` hardening is incomplete for production. See [back-end/requirements.txt](back-end/requirements.txt#L1-L20) and [back-end/config/settings.py](back-end/config/settings.py#L1-L200).

5. `DATABASE_URL` parsing is now implemented with `dj-database-url`; ensure production value points to a managed PostgreSQL instance and is validated in deployment pipelines.

6. No payment provider integration yet — do not commit API keys. Plan secret storage (env vars, vault).

7. If Celery/Redis are enabled, secure Redis (AUTH/TLS/private network). Packages are present but runtime config is not implemented yet.

8. Recommended production settings still need hardening: `DEBUG=False`, strict `ALLOWED_HOSTS`, `SECURE_SSL_REDIRECT=True`, `SESSION_COOKIE_SECURE=True`, `CSRF_COOKIE_SECURE=True`, `SECURE_HSTS_SECONDS`.

Mark any discovered keys in files as REDACTED; do not output their values.
