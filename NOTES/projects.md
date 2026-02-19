# NOTES — projects app

Location: `back-end/projects/`

What exists:
- `models.py`, `views.py`, `admin.py` — placeholder for political projects per region/sector.

Action items:
- Current `Project` model and API endpoints are implemented in `back-end/core`.
- If splitting domain by app, migrate model/viewset from `core` to `projects` and keep URLs backward-compatible.
- If staying core-centric, keep `projects` app as placeholder only with explicit documentation.
