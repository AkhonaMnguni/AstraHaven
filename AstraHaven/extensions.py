"""Shared Flask extensions used throughout the AstraHaven application."""

from flask_login import LoginManager
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address
from flask_sqlalchemy import SQLAlchemy
from flask_wtf import CSRFProtect

# SQLAlchemy handles the database session and model mapping.
db = SQLAlchemy()
login_manager = LoginManager()

# CSRF protection is configured at the app level for form submissions.
csrf = CSRFProtect()

# Rate limiting protects login and API-like endpoints from abuse.
limiter = Limiter(
    key_func=get_remote_address,
    default_limits=[],
    storage_uri="memory://",
)