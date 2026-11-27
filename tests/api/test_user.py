def test_user_duplicate_email(client):
    payload = {
        "username": "userone",
        "email": "userone@example.com",
        "password": "strongpassword123",
    }

    first_response = client.post("/api/v1/users/register", json=payload)
    second_response = client.post(
        "/api/v1/users/register",
        json={
            **payload,
            "username": "usertwo",
        }
    )

    assert first_response.status_code == 201
    assert second_response.status_code == 409

def test_user_duplicate_useranme(client):
    payload = {
        "username": "same",
        "email": "first@example.com",
        "password": "strongpassword123",
    }

    first_response = client.post("/api/v1/users/register", json=payload)
    second_response = client.post(
        "/api/v1/users/register",
        json={
            **payload,
            "email": "second@example.com",
        },
    )

    assert first_response.status_code == 201
    assert second_response.status_code == 409