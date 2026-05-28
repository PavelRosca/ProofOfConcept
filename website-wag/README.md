# Partito Politico — ProofOfConcept

Django 4.2 + Wagtail 7.3 web platform for an Italian political party. Bilingual IT/EN.

**Full context (architecture, models, API, roadmap):** see [`CLAUDE.md`](../CLAUDE.md) at the repo root.

**Setup guide (Windows, step-by-step):** see [`SETUP.md`](SETUP.md)  
**Setup guide (Italian):** see [`SETUP-IT.md`](SETUP-IT.md)

## Quick start

```powershell
.venv\Scripts\Activate.ps1
pip install -r requirements.txt
cp .env.example .env
python manage.py migrate
python manage.py createsuperuser
python manage.py runserver
```

App runs at `http://127.0.0.1:8000/`
