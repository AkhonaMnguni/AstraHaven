from AstraHaven.models import User


def test_password_is_hashed(app):
    with app.app_context():
        user = User.query.filter_by(username="admin").one()
        assert user.password_hash != "secret"
        assert user.check_password("secret")
        assert not user.check_password("wrong")
