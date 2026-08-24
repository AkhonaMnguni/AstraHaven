# AstraHaven

A Flask application for small-business transaction risk monitoring.

## Run locally

```powershell
python -m venv .venv
.venv\Scripts\Activate.ps1
pip install -r requirements-dev.txt
python scripts\seed_demo_data.py
python app.py
```

Open `http://localhost:5000` and sign in with `admin` / `admin-password` after seeding demo data. For production, replace the demo password and set a strong `SECRET_KEY`.

## Test

```powershell
python -m pytest
```


