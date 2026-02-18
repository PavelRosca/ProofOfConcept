# NOTES — core app

Location: `back-end/core/`

What exists:
- `models.py`, `admin.py`, `serializers.py`, `views.py`, `migrations/0001_initial.py` — initial schema and admin.

Important lines to inspect:
- Models canonical schema in migration: [back-end/core/migrations/0001_initial.py](back-end/core/migrations/0001_initial.py#L1-L400)
- Admin config: [back-end/core/admin.py](back-end/core/admin.py#L1-L200)

Action items:
- Review models fields for constraints (unique, indexes).
- Add API serializers and views if missing for public read endpoints.
