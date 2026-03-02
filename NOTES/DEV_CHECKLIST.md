# DEV_CHECKLIST — quick checklist for development & PRs

- [ ] Recreate virtualenv and install `requirements.txt` before running.
- [ ] Run `python manage.py migrate` after model changes.
- [ ] Run tests: `python manage.py test` (add tests where missing).
- [ ] Lint Python code (flake8/ruff) — add to CI.
- [ ] Validate templates/static changes via Django pages and `collectstatic` when needed.
- [ ] Ensure `.env` not committed and secrets are REDACTED.
- [ ] Add integration tests for registration and donation flows.
- [ ] Add Dockerfile and `docker-compose.yml` for reproducible environments.
- [ ] Add GitHub Actions workflow to run tests on push/PR.
