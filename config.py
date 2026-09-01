import os
from pathlib import Path
from datetime import timedelta

BASE_DIR = Path(__file__).resolve().parent


class Config:
    """Base Flask configuration for the application in normal runtime."""

    SECRET_KEY = os.getenv("SECRET_KEY", "change-this-development-key")
    SQLALCHEMY_DATABASE_URI = os.getenv(
        "DATABASE_URL", f"sqlite:///{BASE_DIR / 'astrahaven.db'}"
    )
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    DEBUG = os.getenv("FLASK_DEBUG", "0") == "1"


class TestingConfig(Config):
    """Test configuration that runs against an in-memory SQLite database."""

    TESTING = True
    WTF_CSRF_ENABLED = False
    SQLALCHEMY_DATABASE_URI = "sqlite:///:memory:"







# class Config:
#     SECRET_KEY = os.environ.get(
#         "SECRET_KEY",
#         "development-only-change-me",
#     )
#
#     SQLALCHEMY_DATABASE_URI = os.environ.get(
#         "DATABASE_URL",
#         "sqlite:///AstraHaven.db",
#     )
#
#     SQLALCHEMY_TRACK_MODIFICATIONS = False
#
#     SESSION_COOKIE_HTTPONLY = (
#         os.environ.get("SESSION_COOKIE_HTTPONLY", "1") == "1"
#     )

    SESSION_COOKIE_SECURE = (
        os.environ.get("SESSION_COOKIE_SECURE", "0") == "1"
    )

    SESSION_COOKIE_SAMESITE = os.environ.get(
        "SESSION_COOKIE_SAMESITE",
        "Lax",
    )

    PERMANENT_SESSION_LIFETIME = timedelta(minutes=30)

    WTF_CSRF_TIME_LIMIT = 3600

    RATELIMIT_DEFAULT = os.environ.get(
        "RATELIMIT_DEFAULT",
        "100 per minute",
    )
