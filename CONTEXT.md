# CONTEXT — Partito Politico (ProofOfConcept)

Updated: 2026-02-19

## Executive summary (RO)

ProofOfConcept-ul este funcțional pe baza unui backend Django + frontend Tailwind/Gulp. În practică, logica de business și API-ul sunt implementate în `back-end/core` (nu în app-urile `members/projects/donations`, care rămân schelet). Admin-ul și modelele principale există, iar API-ul DRF este deja expus pe `/api/`.

Starea curentă nu este production-ready: hardening-ul de deployment și testele reale încă lipsesc, dar P0-ul tehnic inițial pe config a fost închis.

---

## What is actually implemented

### Backend
- Django 4.2 cu apps: `core`, `members`, `projects`, `donations`
- `core` conține modelele reale: `Sector`, `Region`, `Project`, `Member`, `Donation`, `StaticPage`
- Admin custom pentru toate modelele din `core`
- API DRF în `core` via router (`ReadOnlyModelViewSet` pentru majoritatea; `ModelViewSet` pentru donations)
- Endpoint de health/status în rădăcină (`/`)

### API routes currently active
- `/api/sectors/`
- `/api/regions/`
- `/api/projects/` (+ `featured`, `active`)
- `/api/members/` (read-only)
- `/api/donations/` (+ `statistics`)
- `/api/pages/` (lookup după `slug`)
- `/api/auth/` (DRF browsable auth)
- `/accounts/` (django-allauth)

### Frontend
- Template Tailwind (Themefisher) cu build pe Gulp
- Pagini principale localizate către context politic: `index`, `projects`, `support`, `join`, `contact`
- Language switch client-side (`IT`/`EN`) în `front-end/scripts/lang.js`
- Navigația principală este curățată pentru scope de prezentare (doar cele 5 pagini)
- Secțiunile template placeholder au fost eliminate din Home și Contact (Presentation Step 2)

---

## Verified discrepancies vs previous docs

1. `allauth.account.middleware.AccountMiddleware` **este valid** (importabil în mediul curent). Nu trebuie eliminat doar pentru că „nu ar exista”.
2. API-ul din faza 2 nu este „to be implemented” în totalitate: există deja endpoint-uri DRF în `core`.
3. Scriptul frontend `remove-darkmode` a fost corectat (path + npm format) la 2026-02-19.
4. Blocul DEBUG duplicat pentru static/media din `config/urls.py` a fost eliminat (2026-02-19).
5. `config/urls.py` referă `settings.STATIC_ROOT`; `STATIC_ROOT` este definit (2026-02-19).
6. `DATABASE_URL` este acum parsat prin `dj-database-url` (2026-02-19); cu `.env` curent, engine-ul rezultat rămâne SQLite.

---

## Architecture reality (important)

- Deși există 4 apps locale, domain-ul real este centralizat în `core`.
- `members`, `projects`, `donations` nu conțin încă modele/view-uri utile (fișiere placeholder).
- Acest lucru este acceptabil pentru PoC, dar trebuie decis clar:
  - ori păstrezi `core` ca app agregator,
  - ori migrezi logic spre apps dedicate și actualizezi routerele + importurile.

---

## Risks and blockers

### P0 (imediat)
- Nu mai există blocker P0 deschis în configurația de bază.

### P1 (următor sprint)
- Clarificare ownership API: `core` vs apps dedicate
- Endpoint dedicat de înregistrare member (acum `members` este read-only)
- Conectare formulare frontend la API cu validare completă

### P2 (după stabilizare)
- Celery/Redis efectiv configurat sau eliminat din deps
- Docker + CI
- Teste automate (momentan `manage.py test` raportează 0 teste)

---

## Security posture snapshot

- `SECRET_KEY` este impus pentru production (`DEBUG=False`), cu fallback doar pentru development local
- `.env` este ignorat corect în `back-end/.gitignore`
- Setările de secure cookies / HSTS / SSL redirect nu sunt activate explicit (normal pentru PoC, insuficient pentru prod)

---

## Recommended next concrete actions

1. Frontend presentation Step 3: finalizează copy italian + CTA-uri coerente pe toate cele 5 pagini.
2. Frontend presentation Step 4: adaugă stări demo pentru formulare (success/error) fără dependență backend.
3. Decide direcția arhitecturală pentru apps (core monolith vs split by domain).
4. Adaugă primele teste de bază pentru endpoint-uri și modele.
5. Continuă hardening security pentru production (`DEBUG=False`, secure cookies, HSTS, SSL redirect).
6. Adaugă Docker + CI.

---

## Validation run (2026-02-19)

- `python manage.py check` → OK
- `python manage.py test` → OK (0 tests)
- `python manage.py check` după fix `STATIC_ROOT` → OK
- `python manage.py check` după cleanup `config/urls.py` (bloc DEBUG duplicat) → OK
- `npm run build` după fix script frontend → OK (warnings Sass/JSHint non-blocante)
- `python manage.py check` + `collectstatic --noinput` după configurare WhiteNoise → OK
- `python manage.py check` + verificare engine DB după parser `DATABASE_URL` (`django.db.backends.sqlite3` din env curent) → OK
- `python manage.py check` după hardening `SECRET_KEY` (required in prod) → OK
- `python manage.py test` după hardening `SECRET_KEY` → OK (0 tests)
- `npm run build` după frontend presentation Step 1 (scope + navigație) → OK
- `npm run build` după frontend presentation Step 2 (cleanup Home/Contact) → OK
