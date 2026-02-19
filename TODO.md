# TODO — Tasks organized by Phases

## FAZA 1 — Bază solidă (High priority)
- [x] Define `STATIC_ROOT` in `back-end/config/settings.py` and keep static serving consistent with `back-end/config/urls.py`.
- [x] Add WhiteNoise middleware + `STATICFILES_STORAGE` for production static serving. See: [back-end/requirements.txt](back-end/requirements.txt#L1-L20)
- [x] Add `dj-database-url` (or equivalent logic) to parse `DATABASE_URL`; current settings always use SQLite.
- [x] Remove duplicated `if settings.DEBUG:` static/media block in `back-end/config/urls.py`.
- [x] Fix frontend script mismatch in `front-end/package.json` (`removeDarkMode.js` vs `removeDarkmode.js`, and `yarn format` vs npm flow).
- [x] Enforce `SECRET_KEY` in production (`DEBUG=False`) and keep dev-only fallback for local setup.
- [ ] Keep `.env` out of git (already covered by `back-end/.gitignore`); verify no secrets are committed.

## FAZA 2 — Conținut public (Medium priority)
- [ ] Add dedicated registration endpoint/workflow in `members` app (currently member API is read-only in `core`).
- [ ] Decide donation flow ownership: keep in `core` router or move to `donations` app and update routes consistently.
- [ ] Connect `front-end` forms (`join`, `support`, `contact`) to backend endpoints with validation and CSRF strategy.
- [ ] Add unit tests for models, routers and API actions (`featured`, `active`, `statistics`).

## FAZA 3 — Funcționalități avansate (Low/Medium)
- [ ] Integrate email notifications (configure SMTP or transactional provider).
- [ ] Implement payment provider integration for donations (Stripe/PayPal).
- [ ] Add admin dashboards and analytics pages.

## FAZA 4 — Scalabilitate & infra
- [ ] Add Celery configuration and sample `tasks.py` if background jobs needed; configure Redis broker (if keeping celery in requirements).
- [ ] Add Dockerfile and `docker-compose.yml` for local dev and production deployments.
- [ ] Add CI (GitHub Actions) to run tests and linting.
