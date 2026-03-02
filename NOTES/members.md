# NOTES — members app

Location: `website-wag/members/`

What exists:
- `models.py`, `views.py`, `admin.py` — skeleton present.

Checks:
- `Member` domain model currently lives in `website-wag/core/models.py` (not in `members/models.py`).
- Add dedicated registration API / form and validation workflow if app split is desired.
- If `members` remains placeholder, document that ownership is intentionally in `core`.
