# CHECKPOINT — ProofOfConcept

Updated: 2026-02-19

## Current Goal
Pregătire frontend pentru prezentare (demo-ready), cu scope clar pe 5 pagini.

## Completed (Backend)
- Added `STATIC_ROOT` in `back-end/config/settings.py`.
- Removed duplicated DEBUG static/media block in `back-end/config/urls.py`.
- Configured WhiteNoise middleware + static storage.
- Added `DATABASE_URL` parsing with `dj-database-url`.
- Hardened `SECRET_KEY` handling: required when `DEBUG=False`, dev-only fallback.
- Added `/staticfiles/` to `back-end/.gitignore`.

## Completed (Frontend Presentation)
- **Step 1:** Navigation scope frozen to 5 pages:
  - `index.html`, `projects.html`, `support.html`, `join.html`, `contact.html`
  - Cleaned main nav in `front-end/src/partials/header.html`.
  - Aligned footer quick links in `front-end/src/partials/footer.html`.
- **Step 2:** Removed generic template leftovers:
  - Cleaned `front-end/src/pages/index.html` (removed generic services/reviews/download blocks).
  - Cleaned `front-end/src/pages/contact.html` (removed duplicate Pinwheel contact template).
- **Step 3:** EN/IT switch now works consistently on presentation scope (5 pages):
  - Root cause fixed: i18n script moved into build source (`front-end/src/scripts/lang.js`) so Gulp includes it in `theme/scripts/`.
  - Added complete `data-i18n` coverage for `index`, `projects`, `support`, `join`, `contact`.
  - Split CTA keys (`supportUs` vs `donateNow`) to avoid incorrect text replacement.
  - `site_lang` persists in `localStorage`; language applies on page load.

## Validation Results
- Backend:
  - `python manage.py check` → OK
  - `python manage.py test` → OK (0 tests)
  - `python manage.py collectstatic --noinput` → OK
- Frontend:
  - `npm run build` → OK
  - Existing Sass/JSHint warnings are non-blocking and pre-existing.

## Remaining Work (Recommended Order)
1. **Frontend Step 4:** add demo form states (success/error) without backend dependency.
3. Decide architecture direction (`core` monolith vs split into `members/projects/donations`).
4. Add first real backend tests (API + model baselines).
5. Continue production hardening (secure cookies, HSTS, SSL redirect).
6. Add Docker + CI.

## Important Files for Resume
- `CONTEXT.md`
- `CONTEXT.json`
- `NOTES/FRONTEND_CHANGES.md`
- `TODO.md`
- `front-end/src/pages/index.html`
- `front-end/src/pages/contact.html`
- `front-end/src/partials/header.html`
- `front-end/src/partials/footer.html`
