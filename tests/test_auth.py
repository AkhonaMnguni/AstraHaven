 from AstraHaven.extensions import db
 from AstraHaven.models import User



def test_login_and_logout(client):
    response = client.post("/login", data={"username": "admin", "password": "secret"}, follow_redirects=True)
    assert response.status_code == 200
    assert b"AstraHaven" in response.data
    response = client.get("/logout", follow_redirects=True)
    assert b"Sign in" in response.data


def test_invalid_login(client):
    response = client.post("/login", data={"username": "admin", "password": "wrong"})
    assert b"Invalid username or password" in response.data


    def test_login_success(app, client):
     with app.app_context():

     user = User(
     username="testuser",
     email="test@example.com",
     role="ANALYST",
     )

     user.set_password(
     "CorrectPassword123!"
     )

     db.session.add(user)
     db.session.commit()

     response = client.post(
     "/login",
     data={
     "username": "testuser",
     "password": "CorrectPassword123!",
     },
     follow_redirects=False,
     )

     assert response.status_code == 302


    def test_login_failure(app, client):
     with app.app_context():

     user = User(
     username="testuser",
     email="test@example.com",
     role="ANALYST",
     )

     user.set_password(
     "CorrectPassword123!"
     )

     db.session.add(user)
     db.session.commit()

     response = client.post(
     "/login",
     data={
     "username": "testuser",
     "password": "WrongPassword",
     },
     )

     assert response.status_code == 401
