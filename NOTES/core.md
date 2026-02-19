# NOTES — core app

Location: `back-end/core/`

What exists:
- `models.py`, `admin.py`, `serializers.py`, `views.py`, `migrations/0001_initial.py` — initial schema and admin.
- Core currently contains the effective business domain and API router used by `/api/`.

Important lines to inspect:
- Models canonical schema in migration: [back-end/core/migrations/0001_initial.py](back-end/core/migrations/0001_initial.py#L1-L400)
- Admin config: [back-end/core/admin.py](back-end/core/admin.py#L1-L200)
- API viewsets/actions: [back-end/core/views.py](back-end/core/views.py#L1-L260)
- API routing: [back-end/core/urls.py](back-end/core/urls.py#L1-L80)

Action items:
- Review models fields for constraints (unique, indexes).
- Add tests for existing endpoints and custom actions (`featured`, `active`, `statistics`).
- Decide if current architecture stays core-centric or is split into dedicated apps.
