# NOTES — donations app

Location: `website-wag/donations/`

What exists:
- `models.py`, `views.py`, `admin.py` placeholders.
- Donation model + API currently live in `website-wag/core`.

Action items:
- Add payment integration (Stripe/PayPal) and secure handling of payment info.
- Keep admin filters for status/date if donations are moved into dedicated app (already present in `core/admin.py`).
