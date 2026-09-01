from AstraHaven.extensions import db
    from AstraHaven.models import User

def test_admin_page_requires_login(client):
    assert client.get("/admin/users").status_code == 302


def test_admin_can_view_users(client):
    client.post("/login", data={"username": "admin", "password": "secret"})
    assert client.get("/admin/users").status_code == 200


    def create_user(
     username,
     role,
    ):
     user = User(
     username=username,
     email=f"{username}@test.local",
     role=role,
     )

     user.set_password(
     "Password123!"
     )

     return user


    def login(client, username):
     return client.post(
     "/login",
     data={
     "username": username,
     "password": "Password123!",
     },
     )


    def test_analyst_cannot_change_roles(
     app,
     client,
    ):
     with app.app_context():

     analyst = create_user(
     "analyst",
     "ANALYST",
     )

     db.session.add(analyst)
     db.session.commit()

     login(client, "analyst")

     response = client.get(
     "/admin/users"
     )

     assert response.status_code == 403


    def test_owner_can_access_admin(
     app,
     client,
    ):
     with app.app_context():

     owner = create_user(
     "owner",
     "OWNER",
     )

     db.session.add(owner)
     db.session.commit()

     login(client, "owner")

     response = client.get(
     "/admin/users"
     )

     assert response.status_code == 200
