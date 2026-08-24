# Architecture

The application is a Flask application factory with blueprints organized by business capability. Flask-SQLAlchemy persists users, transactions, and alerts in SQLite by default. Flask-Login manages the session boundary, while `security.py` provides role checks.

Requests flow from a blueprint route to the model layer. Templates are rendered server-side and share the base navigation shell. The deployment image runs the WSGI-compatible Flask process directly for the starter environment; production should place a hardened WSGI server and reverse proxy in front of it.
