def test_register_user_success(client):
    response = client.post(
        "/api/v1/users/register",
        json={
            "username": "testuser",
            "email": "testuser@example.com",
            "password": "strongpassword1234",
        },
    )

    assert response.status_code == 201

    data = response.json()

    assert data["username"] == "testuser"
    assert data["email"]  == "testuser@example.com"
    assert data["is_active"] is True

    assert "password" not in data
    assert "hashed_password" not in data