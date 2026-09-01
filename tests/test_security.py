from AstraHaven.extensions import db
from AstraHaven.models import User


def test_password_is_hashed(app):
    """Verify that stored passwords are not kept in plain text."""
    with app.app_context():
        user = User.query.filter_by(username="admin").one()
        assert user.password_hash != "secret"
        assert user.check_password("secret")
        assert not user.check_password("wrong")





def test_security_headers(client):
    """Check that security-related response headers are enabled on the login page."""

    response = client.get(
        "/login"
    )

    assert response.headers[
        "X-Content-Type-Options"
    ] == "nosniff"

    assert response.headers[
        "X-Frame-Options"
    ] == "DENY"

    assert "Content-Security-Policy" in (
        response.headers
    )


def test_password_is_not_stored_plaintext(
    app,
):
    """Ensure a user password hash is different from the plaintext secret."""

    with app.app_context():

        user = User(
            username="secureuser",
            email="secure@example.com",
            role="ANALYST",
        )

        user.set_password(
            "SuperSecret123!"
        )

        assert user.password_hash != (
            "SuperSecret123!"
        )

        assert user.check_password(
            "SuperSecret123!"
        )

        assert not user.check_password(
            "WrongPassword"
        )
