def test_transaction_list_requires_login(client):
    assert client.get("/transactions/").status_code == 302


def test_authenticated_user_can_create_transaction(client):
    client.post("/login", data={"username": "admin", "password": "secret"})
    response = client.post("/transactions/new", data={"reference": "TX-9", "supplier": "Vendor", "amount": "42"})
    assert response.status_code == 302
    assert b"TX-9" in client.get("/transactions/").data
