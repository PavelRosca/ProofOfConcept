# TODO — Tasks organized by Phases

## FAZA 1 — Bază solidă (High priority)
- [ ] Remove invalid middleware `allauth.account.middleware.AccountMiddleware` from `back-end/config/settings.py` (risk: app import error). See: [back-end/config/settings.py](back-end/config/settings.py#L30-L60)
- [ ] Add WhiteNoise middleware + `STATIC_ROOT` + `STATICFILES_STORAGE` to serve static files in production. See: [back-end/requirements.txt](back-end/requirements.txt#L1-L20)
- [ ] Add `dj-database-url` or logic to parse `DATABASE_URL` env var and use Postgres when provided. Update `requirements.txt` accordingly.
- [ ] Ensure `.env` is not committed; add `.env` to `.gitignore` if missing. See: [.env.example](back-end/.env.example#L1-L40)

## FAZA 2 — Conținut public (Medium priority)
- [ ] Implement API endpoints / views for: registration (`members`), donations (`donations`). Verify `serializers.py` in apps.
- [ ] Connect `front-end` forms to backend endpoints; add CSRF/DRF protection for API usage.
- [ ] Add unit tests for models and API endpoints.

## FAZA 3 — Funcționalități avansate (Low/Medium)
- [ ] Integrate email notifications (configure SMTP or transactional provider).
- [ ] Implement payment provider integration for donations (Stripe/PayPal).
- [ ] Add admin dashboards and analytics pages.

## FAZA 4 — Scalabilitate & infra
- [ ] Add Celery configuration and sample `tasks.py` if background jobs needed; configure Redis broker (if keeping celery in requirements).
- [ ] Add Dockerfile and `docker-compose.yml` for local dev and production deployments.
- [ ] Add CI (GitHub Actions) to run tests and linting.
