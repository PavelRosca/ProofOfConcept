# UI CHANGES — archived summary

Updated: 2026-03-02

This file replaces the old detailed log that referenced a removed standalone `front-end/` folder.

## Historical summary

- Public pages were localized and simplified for political-site scope.
- Navigation/footer were cleaned to match core pages.
- EN/IT language switch behavior was stabilized.
- Generic template leftovers were removed from key pages.

## Current source of truth

Use these paths in the current workspace:
- `website-wag/templates/site/` for page templates
- `website-wag/templates/site/partials/` for shared template parts
- `website-wag/static/scripts/lang.js` for language script
- `website-wag/static/` for other static assets

## Runtime

Launch from:

```bash
cd website-wag
python manage.py runserver
```
