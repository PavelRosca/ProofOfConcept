# CHECKPOINT — ProofOfConcept

Updated: 2026-03-02

## Current Goal
Consolidare documentație și structură pe runtime unic Django/Wagtail.

## Completed
- Project runtime este unificat în `website-wag/`.
- Folderul `back-end/` a fost redenumit în `website-wag/`.
- Documentația a fost actualizată pentru structura curentă.
- S-au eliminat referințele active la un flux separat `front-end/`.

## Backend / Platform status
- `STATIC_ROOT` + WhiteNoise configurate.
- `DATABASE_URL` parsing configurat prin `dj-database-url`.
- `SECRET_KEY` enforced în production (`DEBUG=False`).
- URL routing include:
  - Django admin (`/admin/`)
  - Wagtail admin (`/cms/`)
  - DRF API (`/api/`)
  - Redirect-uri legacy `.html` către rute curate.

## Validation status
- `python manage.py check` → OK (ultima stare documentată)
- `python manage.py test` → OK (0 tests)

## Remaining work (recommended order)
1. Decide architecture direction (`core` centric vs split pe `members/projects/donations`).
2. Add dedicated registration workflow for members.
3. Add baseline tests for API and models.
4. Continue production hardening (secure cookies, HSTS, SSL redirect).
5. Add Docker + CI.

## Important files
- `CONTEXT.md`
- `CONTEXT.json`
- `WHOLE_PROJECT_DESCRIPTION.txt`
- `TODO.md`
- `website-wag/README.md`
- `website-wag/SETUP.md`
