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


def test_login_success(client):

    register_response = client.post(
        "/api/v1/users/register",
        json={
            "username": "testuser",
            "email": "test@example.com",
            "password": "StrongPassword123"
        }
    )

    assert register_response.status_code == 201

    login_response = client.post(
        "/api/v1/users/login",
        json={
            "email": "test@example.com",
            "password": "StrongPassword123",
        },
    )

    assert login_response.status_code == 200

    data = login_response.json()

    assert "access_token" in data
    assert data["token_type"] == "bearer"

def test_login_invalid_password(client):
    #  ----> Register a user
    client.post(
        "/api/v1/users/register",
        json={
            "username": "testuser",
            "email": "test@example.com",
            "password": "StrongPassword123",
        },
    )
    # ---> Login with an incorrect password

    response = client.post(
        "/api/v1/users/login",
        json={
            "email": "test@example.com",
            "password": "WorngPassword123"
        },
    )

    assert response.status_code == 401
    assert response.json()["detail"] == "Invalid email or password"

def test_get_current_user_success(client):
    # ----> Register a user
    client.post(
        "/api/v1/users/register",
        json={
            "username": "testuser",
            "email": "test@example.com",
            "password": "StrongPassword123",
        },
    )

    # --> Login to get access token
    login_response = client.post(
        "/api/v1/users/login",
        json={
            "email": "test@example.com",
            "password": "StrongPassword123",
        },
    )

    token = login_response.json()["access_token"]

    #---- Accesss protected endpoint

    response = client.get(
        "/api/v1/users/me",
        headers={"Authorization": f"Bearer {token}"},
    )

    assert response.status_code == 200
    assert response.json()["email"] == "test@example.com"
    assert response.json()["username"] == "testuser"
    assert "hashed_password" not in response.json()

def test_get_current_user_invalid_token(client):
    response = client.get(
        "/api/v1/users/me",
        headers={"Authorization": "Bearer invalid-token"},
    )

    assert response.status_code == 401

def test_get_current_user_without_token(client):
    response = client.get("api/v1/users/me")

    assert response.status_code == 401
