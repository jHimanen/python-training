def test_create_and_get_user(client):
    # Create user via API
    resp = client.post("/users", json={"email": "x@y.com", "full_name": "X Y"})
    assert resp.status_code == 201
    data = resp.json()
    user_id = data["id"]
    assert data["email"] == "x@y.com"

    # Fetch same user
    resp2 = client.get(f"/users/{user_id}")
    assert resp2.status_code == 200
    data2 = resp2.json()
    assert data2["id"] == user_id
    assert data2["email"] == "x@y.com"
