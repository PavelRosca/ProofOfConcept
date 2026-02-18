# CONTEXT — Partito Politico (ProofOfConcept)

**Executive summary (în română)**

Acest proiect este o dovadă de concept pentru backend Django + frontend Tailwind pentru un site de partid politic italian. Scopul principal este gestionarea membrilor (tesserati), proiectelor pe regiuni/sectoare, și a donațiilor. În prezent există o bază Django cu aplicații `core`, `members`, `projects`, `donations` și un frontend static bazat pe Tailwind/Gulp. Multe componente CRUD și admin sunt implementate; funcționalități avansate (Celery, Redis, plăți, chat live, containerizare) sunt parțial sau deloc implementate.

**Conversation origin & history (sintetizat)**

- Interlocutori: Felicia ↔ Paolo (conversație inițială despre arhitectură și setup). 
- Limbă finală a proiectului: italiană. 
- Domeniu: site partid politic din Italia — suport familii, donații, membri, regiuni/sectoare.
- Dezvoltare planificată pe faze (1..4): bază → conținut public → funcționalități avansate → scalabilitate.

Short summaries:
- Italiano: Progetto Django per un partito politico italiano. Backend, amministrazione, modelli core e frontend con Tailwind. Alcune configurazioni di produzione mancano.
- English: Django + Tailwind proof-of-concept for a political party website (members, projects, donations). Core models and admin exist; production hardening and advanced features are pending.

---

## Current scope — what is implemented (Done / Partial / Missing)

- Django project skeleton: Done. (`/back-end/manage.py`, `/back-end/config/settings.py`) — see [back-end/manage.py](back-end/manage.py#L1-L40) and [back-end/config/settings.py](back-end/config/settings.py#L1-L220).
- Core models and initial migration: Done (see `/back-end/core/migrations/0001_initial.py`).
- Admin customization: Done (presence of `core/admin.py`).
- REST framework installed: Done (in `requirements.txt`, `rest_framework` in `INSTALLED_APPS`) — [back-end/requirements.txt](back-end/requirements.txt#L1-L40) and [back-end/config/settings.py](back-end/config/settings.py#L1-L120).
- CORS configured for localhost: Partial — CORS settings exist but origin list comes from env example: see [back-end/config/settings.py](back-end/config/settings.py#L40-L80) and [.env.example](back-end/.env.example#L1-L40).
- Static files / WhiteNoise: Missing — `whitenoise` is in requirements but not configured in `settings.py` (add middleware, `STATIC_ROOT`, `STATICFILES_STORAGE`). See [back-end/requirements.txt](back-end/requirements.txt#L1-L20) and [back-end/config/settings.py](back-end/config/settings.py#L150-L200).
- DATABASE_URL / Postgres support: Partial — `psycopg2-binary` in requirements and `.env.example` mentions `DATABASE_URL` but `settings.py` currently defaults to SQLite unconditionally (no `dj-database-url` usage). See [back-end/config/settings.py](back-end/config/settings.py#L100-L120) and [.env.example](back-end/.env.example#L1-L20).
- Celery/Redis: Missing config — packages present in `requirements.txt` but no Celery app config or tasks found in repo scan. See [back-end/requirements.txt](back-end/requirements.txt#L20-L30).
- Frontend Tailwind/Gulp tooling: Done — `package.json` and `gulpfile.js` present; docs instruct Node v18+. See [front-end/package.json](front-end/package.json#L1-L80) and [front-end/README.md](front-end/README.md#L1-L40).
- Docker / docker-compose: Missing — no `Dockerfile` or `docker-compose.yml` in scanned root (mark Missing).

---

## Architecture & components

- Django project: `back-end/config` (entrypoint `manage.py`). Key files:
  - `back-end/config/settings.py` — main configuration (language, INSTALLED_APPS, middleware). [back-end/config/settings.py](back-end/config/settings.py#L1-L220)
  - `back-end/config/urls.py` — root URL configuration (inspect for API endpoints).
  - `back-end/manage.py` — CLI entrypoint. [back-end/manage.py](back-end/manage.py#L1-L40)
- Apps:
  - `core` — models, admin, serializers, migrations. (`back-end/core/models.py`, `back-end/core/admin.py`, `back-end/core/migrations/0001_initial.py`)
  - `members` — user/member related (placeholder files exist).
  - `projects` — project management (placeholder files exist).
  - `donations` — donation tracking (placeholder files exist).
- Frontend: Tailwind-based static site built with Gulp. Files in `/front-end/src`, `/front-end/theme`, and tooling in `package.json` and `gulpfile.js`.

---

## Data model — overview of key models (fields & relationships)

Note: details below reference model files and initial migration. If you need field-level canonical definitions, open [back-end/core/models.py] and [back-end/core/migrations/0001_initial.py]. Below is a consolidated summary extracted from migrations and comments.

- Sector (core.models.Sector) — fields (approx): `name`, `region_type` (choice: nord/centro/sud), `description`, `order`. (See [back-end/core/migrations/0001_initial.py](back-end/core/migrations/0001_initial.py#L1-L200)).
- Region (core.models.Region) — fields: `name`, `code`, `sector` (FK to Sector), `contact_email`, `contact_phone`, `active` boolean. (See migration: [back-end/core/migrations/0001_initial.py](back-end/core/migrations/0001_initial.py#L1-L300)).
- Project (core.models.Project) — fields: `title`, `slug`, `description`, `status` (choices), `sectors` (M2M to Sector), `budget`, `start_date`, `end_date`, `is_featured`.
- Member (core.models.Member) — fields: `user` (OneToOne to `auth.User`), `region` (FK to Region), `tessera_number` (unique), `status`, `profile_image`.
- Donation (core.models.Donation) — fields: `donor_name`, `donor_email`, `amount`, `status`, `payment_method`, `member` (FK optional), `is_anonymous`.
- StaticPage (core.models.StaticPage) — `title`, `slug`, `page_type`, `content`, `is_published`.

If any of the above fields differ from the migration, open: [back-end/core/migrations/0001_initial.py](back-end/core/migrations/0001_initial.py#L1-L400).

---

## Auth & Admin

- Authentication/backends: `AUTHENTICATION_BACKENDS` configured for Django default and `allauth` (see [back-end/config/settings.py](back-end/config/settings.py#L120-L160)).
- Admin customizations: `core/admin.py` present — models registered. See [back-end/core/admin.py](back-end/core/admin.py#L1-L200).
- Permissions: DRF default permission class set to `IsAuthenticatedOrReadOnly` in `REST_FRAMEWORK` (see [back-end/config/settings.py](back-end/config/settings.py#L160-L200)).

---

## UX / UI — menus and sector structure

- Frontend organizes content by sector and region; pages and templates in `front-end/src/pages` and `front-end/theme`. Example pages: `index.html`, `pricing.html`, `signup.html`. See [front-end/src/pages](front-end/src/pages).
- Menu flows for registration/donation are present in templates and `scripts/main.js` but backend endpoints for API forms may be missing (mark Partial).

---

## Forms & flows

- Registration: frontend signup template exists (`front-end/src/pages/signup.html`) — backend route for registration (DRF endpoint or Django form view) must be verified in `members.views` / `core.views`.
- Donation: model exists; API or payment integration is missing (no payment provider config). See [back-end/donations/models.py](back-end/donations/models.py).

---

## Background tasks & scalability

- `celery` and `redis` included in `requirements.txt` but no Celery app configuration or `tasks.py` found — Missing. See [back-end/requirements.txt](back-end/requirements.txt#L20-L30).
- No Dockerfile / docker-compose present — Missing containerization.
- `whitenoise` in requirements but not configured; static production serving incomplete. See [back-end/requirements.txt](back-end/requirements.txt#L1-L20) and [back-end/config/settings.py](back-end/config/settings.py#L150-L200).

---

## Third-party services

- Email: `.env.example` includes SMTP settings and console backend example. No production email provider configured. See [.env.example](back-end/.env.example#L1-L40).
- Payments: Not configured — no stripe/paypal keys or integration files found.
- Live chat: Not present.

---

## Deployment & environment

- Development: instructions use virtualenv and `setup.sh` (see [back-end/setup.sh](back-end/setup.sh#L1-L120)).
- Frontend: Node/npm and Gulp required; docs advise Node v18+. See [front-end/README.md](front-end/README.md#L1-L40) and [front-end/package.json](front-end/package.json#L1-L40).
- Production: recommended steps in READMEs, but key settings (`STATIC_ROOT`, database URL parsing, secure settings) are not implemented in `settings.py` (Missing). See [back-end/config/settings.py](back-end/config/settings.py#L140-L200).

---

## Open TODOs & Gaps (mapped to phases)

FAZA 1 — Bază solidă (priority)
- Ensure `settings.py` production readiness (STATIC_ROOT, WhiteNoise). Files: [back-end/config/settings.py](back-end/config/settings.py#L140-L200). Status: Missing.
- Fix middleware: remove incorrect `allauth.account.middleware.AccountMiddleware` (causes import error). See [back-end/config/settings.py](back-end/config/settings.py#L40-L80). Status: High priority.
- Add DATABASE_URL handling (dj-database-url) or document explicit SQLite-only deployment. Files: [back-end/config/settings.py](back-end/config/settings.py#L100-L120), [.env.example](back-end/.env.example#L1-L20). Status: Partial.

FAZA 2 — Conținut public
- Build and wire frontend forms to backend endpoints (registration, donation). Files: `front-end/src/pages/signup.html`, `back-end/members/views.py`. Status: Partial/Missing.

FAZA 3 — Funcționalități avansate
- Add email notifications, admin dashboards, payment integration. Files missing: payment clients. Status: Missing.

FAZA 4 — Scalabilitate
- Configure Celery + Redis; add Docker + CI; configure CDN. Files: none present. Status: Missing.

---

## Security concerns

- `.env` files: present as `.env.example`; ensure real `.env` is in `.gitignore` (do not commit secrets). If `.env` exists, mark secrets REDACTED. See [.env.example](back-end/.env.example#L1-L40).
- SECRET_KEY default fallback in `settings.py` uses an insecure default — must be changed for production. See [back-end/config/settings.py](back-end/config/settings.py#L20-L28).

---

## Suggested next steps (concrete)

1. Fix `MIDDLEWARE`: remove `allauth.account.middleware.AccountMiddleware` and add `whitenoise.middleware.WhiteNoiseMiddleware` after `SecurityMiddleware`. Edit: [back-end/config/settings.py](back-end/config/settings.py#L30-L60).
2. Add `STATIC_ROOT` and `STATICFILES_STORAGE` settings. See suggestion in root `DEV_CHECKLIST.md`.
3. Add `dj-database-url` or conditionally parse `DATABASE_URL` to support Postgres in production.
4. Decide whether to keep Celery/Redis now — implement or remove from `requirements.txt`.
5. Wire frontend forms to backend API endpoints; add API views/serializers in `members` and `donations` apps.
6. Add Dockerfile + docker-compose for local development; add CI workflows in `.github/workflows` for tests and linting.

---

## References (key files cited)
- [back-end/config/settings.py](back-end/config/settings.py#L1-L220)
- [back-end/manage.py](back-end/manage.py#L1-L40)
- [back-end/requirements.txt](back-end/requirements.txt#L1-L40)
- [back-end/setup.sh](back-end/setup.sh#L1-L120)
- [back-end/.env.example](back-end/.env.example#L1-L40)
- [back-end/core/migrations/0001_initial.py](back-end/core/migrations/0001_initial.py#L1-L400)
- [front-end/package.json](front-end/package.json#L1-L80)
- [front-end/README.md](front-end/README.md#L1-L40)

---

End of CONTEXT.md
