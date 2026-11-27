
def test_register_user_invalid_email(client):
    payload = {
        "username": "testuser",
        "email": "invalid-email",
        "password": "strongpassword123",
    }
    response = client.post(
        "/api/v1/users/register",
        json=payload,
    )

    assert response.status_code == 422


def test_register_user_short_password(client):
    response = client.post(
        "/api/v1/users/register",
        json={
            "username": "testuser",
            "email": "test@example.com",
            "password": "123",
        },
    )

    assert response.status_code == 422
