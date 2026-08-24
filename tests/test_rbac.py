def test_admin_page_requires_login(client):
    assert client.get("/admin/users").status_code == 302


def test_admin_can_view_users(client):
    client.post("/login", data={"username": "admin", "password": "secret"})
    assert client.get("/admin/users").status_code == 200
