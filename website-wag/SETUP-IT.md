# Setup Guide — website-wag (Italiano)

Guida rapida per eseguire il progetto Django + Wagtail CMS in locale su Windows.

---

## Requisiti

- **Python 3.12+** — Scarica da https://www.python.org/downloads/  
  Durante l'installazione, seleziona **"Add Python to PATH"**
- **PowerShell** o **Command Prompt** (Windows)

---

## Installazione (5 minuti)

### 1. Naviga al progetto

```powershell
cd C:\percorso\a\website-wag
```

### 2. Attiva l'ambiente virtuale

```powershell
.venv\Scripts\activate
```

Dovresti vedere `(.venv)` all'inizio del prompt:
```
(.venv) PS C:\Users\YourName\website-wag>
```

### 3. Installa dipendenze

```powershell
pip install -r requirements.txt
```

### 4. Crea file `.env`

```powershell
copy .env.example .env
```

### 5. Applica migrazioni database

```powershell
python manage.py migrate
```

### 6. Crea account admin

```powershell
python manage.py createsuperuser
```

Segui le istruzioni e salva le credenziali.

### 7. Avvia il server

```powershell
python manage.py runserver
```

Dovresti vedere:
```
Starting development server at http://127.0.0.1:8000/
```

---

## Accedi all'applicazione

Apri il browser:

| Interfaccia | URL |
|---|---|
| Sito Pubblico | http://127.0.0.1:8000/ |
| Wagtail CMS | http://127.0.0.1:8000/cms/ |
| Admin Django | http://127.0.0.1:8000/admin/ |
| API REST | http://127.0.0.1:8000/api/ |

Accedi con le credenziali del superuser creato al passo 6.

---

## Comandi utili

| Comando | Descrizione |
|---|---|
| `CTRL+BREAK` | Interrompi il server |
| `python manage.py check` | Verifica integrità del progetto |
| `python manage.py shell` | Shell Python interattiva |
| `python manage.py collectstatic --noinput` | Raccogli file statici |

---

## Problemi comuni

### "Python non trovato"
Reinstalla Python e seleziona **"Add Python to PATH"** durante l'installazione.

### "No module named 'django'"
Verifica che `(.venv)` sia attivo nel prompt, poi esegui:
```powershell
pip install -r requirements.txt
```

### "Port 8000 già in uso"
Esegui:
```powershell
python manage.py runserver 8001
```
Accedi a http://127.0.0.1:8001/

### "Permission denied su db.sqlite3"
Ricrea il database:
```powershell
rm db.sqlite3
python manage.py migrate
python manage.py createsuperuser
```

---

## Riavvia il servizio

Dopo aver chiuso il terminal:

```powershell
cd C:\percorso\a\website-wag
.venv\Scripts\activate
python manage.py runserver
```

---

## Documenti aggiuntivi

- **SETUP.md** — Guida completa e dettagliata in inglese
- **.env.example** — Tutte le variabili d'ambiente disponibili
- **NOTES/** — Documentazione del progetto
