# SECURITY_ISSUES — Observed security concerns

1. SECRET_KEY fallback in `back-end/config/settings.py` uses a hard-coded insecure default. Replace with environment-only secret. See [back-end/config/settings.py](back-end/config/settings.py#L16-L28).

2. `.env.example` includes many sensitive keys placeholders. Ensure real `.env` is excluded from git and secrets are REDACTED. See [.env.example](back-end/.env.example#L1-L40).

3. `allauth.account.middleware.AccountMiddleware` is not a standard middleware and may lead to startup errors which could be used to leak stack traces in DEBUG mode. Remove or correct it: [back-end/config/settings.py](back-end/config/settings.py#L40-L60).

4. Static files not hardened — `collectstatic` and WhiteNoise config missing; ensure `STATIC_ROOT` and `STATICFILES_STORAGE` defined before running collectstatic. See [back-end/config/settings.py](back-end/config/settings.py#L140-L200).

5. No payment provider integration yet — do not commit API keys. Plan secret storage (env vars, vault).

6. If Celery/Redis are enabled, secure the Redis instance (require AUTH, use private network). Currently Celery config missing — do not enable until properly configured.

7. Recommended production settings (not present): `DEBUG=False`, `ALLOWED_HOSTS` hardened, `SECURE_SSL_REDIRECT=True`, `SESSION_COOKIE_SECURE=True`, `CSRF_COOKIE_SECURE=True`, `SECURE_HSTS_SECONDS` configured.

Mark any discovered keys in files as REDACTED; do not output their values.
