import pytest

from config import TestingConfig
from AstraHaven import create_app
from AstraHaven.extensions import db
from AstraHaven.models import User


@pytest.fixture
def app():
    app = create_app(TestingConfig)
    with app.app_context():
        db.drop_all()
        db.create_all()
        user = User(username="admin", role="admin")
        user.set_password("secret")
        db.session.add(user)
        db.session.commit()
    yield app
    with app.app_context():
        db.session.remove()
        db.drop_all()


@pytest.fixture
def client(app):
    return app.test_client()
