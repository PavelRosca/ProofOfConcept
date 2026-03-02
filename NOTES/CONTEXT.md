# CONTEXT — Partito Politico (ProofOfConcept)

Updated: 2026-03-02

## Executive summary (RO)

Proiectul rulează acum unificat din `website-wag/` prin Django (`python manage.py runserver`).
Nu mai există flux separat de frontend în workspace; paginile publice sunt servite din `templates/site`, iar asset-urile din `static/`.

## Ce este implementat acum

### Platformă
- Django 4.2 + Wagtail + Django REST Framework
- Rulare locală unică din `website-wag/`
- Admin Django (`/admin/`) + Wagtail admin (`/cms/`)

### Domeniu și API
- Modele principale în `core`: `Sector`, `Region`, `Project`, `Member`, `Donation`, `StaticPage`
- API DRF activ în `core` pe `/api/`
- Rute active:
  - `/api/sectors/`
  - `/api/regions/`
  - `/api/projects/` (`featured`, `active`)
  - `/api/members/` (read-only)
  - `/api/donations/` (`statistics`)
  - `/api/pages/`
  - `/api/auth/`, `/accounts/`

### Website/UI
- Paginile publice există în `website-wag/templates/site/`
- Scripturile publice sunt în `website-wag/static/scripts/` (`main.js`, `lang.js`)
- URL legacy `*.html` sunt redirectate la rutele curate (`/about/`, `/projects/` etc.)

## Realitatea arhitecturală

- `core` conține implementarea reală a domeniului și API-ului.
- `members`, `projects`, `donations` sunt în mare parte schelet.
- Wagtail este deja integrat (`website` app, pagini managed).

## Stare de hardening

- `SECRET_KEY` este impus când `DEBUG=False`
- `DATABASE_URL` este parsat via `dj-database-url`
- WhiteNoise este activ pentru static
- Mai lipsesc setările stricte production (`SECURE_SSL_REDIRECT`, cookies secure, HSTS)

## Next steps recomandate

1. Clarificare ownership: rămâne logică în `core` sau split pe apps dedicate.
2. Endpoint dedicat de member registration (în prezent members API este read-only).
3. Teste reale pentru modele și API actions.
4. Hardening production complet + Docker + CI.
