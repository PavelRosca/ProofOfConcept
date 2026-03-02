# ADMIN_GUIDE — How to run the project (development)

Prereqs:
- Python 3.10+ recommended

Runtime (development):

```bash
cd website-wag
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
cp .env.example .env   # edit values as needed (SECRET_KEY, DEBUG, ALLOWED_HOSTS)
python manage.py migrate
python manage.py createsuperuser
python manage.py runserver
```

Admin panel: http://localhost:8000/admin (login with superuser)
Wagtail CMS: http://localhost:8000/cms

Notes:
- The provided `website-wag/setup.sh` automates many steps (virtualenv, install, migrate, createsuperuser) — review it before running. See [website-wag/setup.sh](website-wag/setup.sh#L1-L120).
- For production, configure `STATIC_ROOT` and WhiteNoise, set `DEBUG=False`, and use a real DB (Postgres) via `DATABASE_URL`.
