# TODO — Tasks organized by Phases

## FAZA 1 — Bază solidă (High priority)
- [x] Define `STATIC_ROOT` in `website-wag/config/settings.py` and keep static serving consistent.
- [x] Add WhiteNoise middleware + `STATICFILES_STORAGE` for production static serving.
- [x] Add `dj-database-url` (or equivalent logic) to parse `DATABASE_URL`; current settings always use SQLite.
- [x] Remove duplicated `if settings.DEBUG:` static/media block in URL config.
- [x] Consolidate runtime in Django app (`website-wag/`) and remove dependency on separate `front-end/` folder.
- [x] Enforce `SECRET_KEY` in production (`DEBUG=False`) and keep dev-only fallback for local setup.
- [ ] Keep `.env` out of git (covered by `website-wag/.gitignore`); verify no secrets are committed.

## FAZA 2 — Conținut public (Medium priority)
- [ ] Add dedicated registration endpoint/workflow in `members` app (currently member API is read-only in `core`).
- [ ] Decide donation flow ownership: keep in `core` router or move to `donations` app and update routes consistently.
- [ ] Connect template forms (`join`, `support`, `contact`) to backend endpoints with validation and CSRF strategy.
- [ ] Add unit tests for models, routers and API actions (`featured`, `active`, `statistics`).

## FAZA 3 — Funcționalități avansate (Low/Medium)
- [ ] Integrate email notifications (configure SMTP or transactional provider).
- [ ] Implement payment provider integration for donations (Stripe/PayPal).
- [ ] Add admin dashboards and analytics pages.

## FAZA 4 — Scalabilitate & infra
- [ ] Add Celery configuration and sample `tasks.py` if background jobs needed; configure Redis broker (if keeping celery in requirements).
- [ ] Add Dockerfile and `docker-compose.yml` for local dev and production deployments.
- [ ] Add CI (GitHub Actions) to run tests and linting.
