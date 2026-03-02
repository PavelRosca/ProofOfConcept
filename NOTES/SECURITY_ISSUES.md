# SECURITY_ISSUES — Observed security concerns

1. SECRET_KEY handling updated (2026-02-19): production now requires `SECRET_KEY` when `DEBUG=False`; dev fallback remains local-only (`django-insecure-dev-only-change-me`). Ensure deployment always injects a strong secret via environment.

2. `.env.example` includes sensitive key placeholders. Ensure real `.env` is excluded from git and secrets are REDACTED. See [.env.example](website-wag/.env.example#L1-L60).

3. Static files baseline is configured (`STATIC_ROOT`, WhiteNoise), but production hardening still requires strict deployment settings and verification on target infra.

4. WhiteNoise is enabled; validate `collectstatic` and cache behavior in production deployment pipeline.

5. `DATABASE_URL` parsing is now implemented with `dj-database-url`; ensure production value points to a managed PostgreSQL instance and is validated in deployment pipelines.

6. No payment provider integration yet — do not commit API keys. Plan secret storage (env vars, vault).

7. If Celery/Redis are enabled, secure Redis (AUTH/TLS/private network). Packages are present but runtime config is not implemented yet.

8. Recommended production settings still need hardening: `DEBUG=False`, strict `ALLOWED_HOSTS`, `SECURE_SSL_REDIRECT=True`, `SESSION_COOKIE_SECURE=True`, `CSRF_COOKIE_SECURE=True`, `SECURE_HSTS_SECONDS`.

Mark any discovered keys in files as REDACTED; do not output their values.
