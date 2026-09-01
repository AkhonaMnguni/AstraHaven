"""Shared pytest fixtures used to create a test database and client for the app."""

import pytest

from config import TestingConfig
from AstraHaven import create_app
from AstraHaven.extensions import db
from AstraHaven.models import User


@pytest.fixture
def app():
    """Create a fresh Flask app using the testing config for each test."""
    app = create_app(TestingConfig)
    with app.app_context():
        db.drop_all()
        db.create_all()
        user = User(username="admin", email="admin@test.local", role="ADMIN")
        user.set_password("secret")
        db.session.add(user)
        db.session.commit()
    yield app
    with app.app_context():
        db.session.remove()
        db.drop_all()


@pytest.fixture
def client(app):
    """Return a test client that exercises the application routes without a live server."""
    return app.test_client()