# AstraHaven

AstraHaven is a Flask-based transaction governance and risk-monitoring dashboard for small businesses. It combines transaction review, supplier oversight, alert triage, and role-based access control into one application.

## What this project does

- Tracks transactions, suppliers, employees, and business units
- Flags suspicious patterns such as expense spikes and supplier concentration
- Provides a dashboard for overview metrics and open risk alerts
- Enforces access control by role: OWNER, ADMIN, AUDITOR, MANAGER, ANALYST
- Logs audit events for user and system actions
- Includes seeded demo data for local testing and UI review

## Tech stack

- Python 3.13+
- Flask
- Flask-SQLAlchemy
- Flask-Login
- Flask-Limiter
- Flask-WTF
- SQLite (default local database)
- PostgreSQL option via Docker Compose
- pytest for automated tests

## Project structure

```text
AstraHaven/
  __init__.py
  admin/
  alerts/
  auth/
  dashboard/
  extensions.py
  models.py
  security.py
  static/
  templates/
  suppliers/
  transactions/
app.py
config.py
docker-compose.yml
Dockerfile
requirements.txt
requirements-dev.txt
scripts/
  seed_demo_data.py
tests/
```

## Installation

### 1) Clone and enter the project

```bash
cd AstraHaven
```

### 2) Create a virtual environment

Windows PowerShell:

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
```

macOS / Linux:

```bash
python3 -m venv .venv
source .venv/bin/activate
```

### 3) Install dependencies

```bash
python -m pip install --upgrade pip
python -m pip install -r requirements-dev.txt
```

This installs both the application dependencies and the developer tooling used for tests and linting.

## Run the project in every way

### Option A: Run locally with the built-in Flask server

This is the simplest way to run the app for daily local development.

```bash
python app.py
```

Then open:

```text
http://127.0.0.1:5000
```

The app will create the default SQLite database file automatically if it does not exist.

Default database file:

```text
astrahaven.db
```

### Option B: Run with Flask CLI

```bash
set FLASK_APP=app
set FLASK_ENV=development
flask run --host 127.0.0.1 --port 5000
```

On macOS / Linux:

```bash
export FLASK_APP=app
export FLASK_ENV=development
flask run --host 127.0.0.1 --port 5000
```

### Option C: Run using Docker Compose

This starts the application and a PostgreSQL database together.

```bash
docker compose up --build
```

Then open:

```text
http://localhost:5000
```

The Compose stack is defined in [docker-compose.yml](docker-compose.yml) and uses PostgreSQL on port 5432.

### Option D: Run the app in debug mode

```bash
python app.py
```

The app is configured with:

```python
app.run(host="127.0.0.1", port=5000, debug=True)
```

Use this when you want hot-reload behavior and easier template debugging.

## Seed demo data

This app includes a data seeding script that creates branches, users, employees, suppliers, transactions, and alerts.

Run:

```bash
python scripts\seed_demo_data.py
```

On macOS / Linux:

```bash
python3 scripts/seed_demo_data.py
```

This creates demo records and populates suspicious alert scenarios for testing.

## Default login accounts

After running the seed script, these accounts are available:

| Role | Username | Password |
| --- | --- | --- |
| Owner | owner | OwnerPassword123! |
| Admin | admin | AdminPassword123! |
| Analyst | analyst | AnalystPassword123! |

You can sign in from the login screen at:

```text
http://127.0.0.1:5000/login
```

## Main pages and routes

Once the app is running, these are the screens you can view:

- `/` — dashboard overview
- `/login` — login page
- `/transactions/` — transaction list and creation form
- `/suppliers/` — supplier records
- `/alerts/` — list of generated alerts
- `/alerts/<alert_id>` — alert detail screen
- `/admin/users` — admin user and role management

## Database tables and schema

The default local database is SQLite, and the app creates these tables automatically:

- users
- branches
- suppliers
- employees
- transactions
- alerts
- audit_logs

### Inspect the SQLite database locally

List tables:

```bash
sqlite3 astrahaven.db ".tables"
```

Show schema:

```bash
sqlite3 astrahaven.db ".schema"
```

Preview rows from a table:

```bash
sqlite3 astrahaven.db "SELECT * FROM users;"
```

You can also open the database in a GUI such as DB Browser for SQLite.

## Environment variables

The app reads these values from the environment:

- `SECRET_KEY` — set a custom secret key for production
- `DATABASE_URL` — override the default SQLite database location
- `FLASK_DEBUG` — set to `1` to enable debug mode

Example:

```bash
set SECRET_KEY=my-super-secret-key
set DATABASE_URL=sqlite:///C:/path/to/astrahaven.db
```

Or in bash:

```bash
export SECRET_KEY=my-super-secret-key
export DATABASE_URL=sqlite:////absolute/path/to/astrahaven.db
```

## Running tests

```bash
python -m pytest -q
```

Optional coverage report:

```bash
python -m pytest --cov=.
```

## Useful development commands

Install dependencies:

```bash
python -m pip install -r requirements-dev.txt
```

Rebuild demo data:

```bash
python scripts\seed_demo_data.py
```

Start the local app:

```bash
python app.py
```

## Troubleshooting

### App does not start

Check that dependencies are installed:

```bash
python -m pip install -r requirements-dev.txt
```

### SQLite database is empty or missing tables

Run:

```bash
python app.py
```

The app calls `db.create_all()` when the application is created, so the tables are created automatically on startup.

### Login fails

Make sure you ran the seed script:

```bash
python scripts\seed_demo_data.py
```

Then use one of the demo credentials listed above.

### Docker is not running

Start Docker Desktop or your local Docker daemon, then run:

```bash
docker compose up --build
```

## Notes

- The default app configuration is intentionally simple for local development.
- The app uses SQLite by default to reduce setup friction.
- For production, replace the demo credentials and set a strong `SECRET_KEY`.
- The seeded users and transactions are designed to let you review the dashboard and alert logic quickly.

## Quick start summary

```bash
cd AstraHaven
python -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install -r requirements-dev.txt
python scripts\seed_demo_data.py
python app.py
```

Then go to:

```text
http://127.0.0.1:5000/login
```

Sign in with `admin` / `AdminPassword123!` and explore the dashboard, alerts, transactions, and supplier tables.


