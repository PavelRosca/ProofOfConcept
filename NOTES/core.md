# NOTES — core app

Location: `website-wag/core/`

What exists:
- `models.py`, `admin.py`, `serializers.py`, `views.py`, `migrations/0001_initial.py` — initial schema and admin.
- Core currently contains the effective business domain and API router used by `/api/`.

Important lines to inspect:
- Models canonical schema in migration: [website-wag/core/migrations/0001_initial.py](website-wag/core/migrations/0001_initial.py#L1-L400)
- Admin config: [website-wag/core/admin.py](website-wag/core/admin.py#L1-L220)
- API viewsets/actions: [website-wag/core/views.py](website-wag/core/views.py#L1-L320)
- API routing: [website-wag/core/urls.py](website-wag/core/urls.py#L1-L120)

Action items:
- Review models fields for constraints (unique, indexes).
- Add tests for existing endpoints and custom actions (`featured`, `active`, `statistics`).
- Decide if current architecture stays core-centric or is split into dedicated apps.
