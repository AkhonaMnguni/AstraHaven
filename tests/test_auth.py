def test_login_and_logout(client):
    response = client.post("/login", data={"username": "admin", "password": "secret"}, follow_redirects=True)
    assert response.status_code == 200
    assert b"AstraHaven" in response.data
    response = client.get("/logout", follow_redirects=True)
    assert b"Sign in" in response.data


def test_invalid_login(client):
    response = client.post("/login", data={"username": "admin", "password": "wrong"})
    assert b"Invalid username or password" in response.data
