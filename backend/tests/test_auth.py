def test_api_root_returns_database_url(client):
    client_instance, _ = client
    response = client_instance.get("/api/v1/")
    assert response.status_code == 200
    assert isinstance(response.json(), str)


def test_protected_route_returns_current_user(client):
    client_instance, user = client
    response = client_instance.get("/api/v1/protected")
    assert response.status_code == 200
    assert response.json()["email"] == user.email


def test_register_user_success(client):
    client_instance, _ = client
    payload = {"email": "reg@example.com", "password": "Pass!", "display_name": "User"}
    response = client_instance.post(
        "/api/v1/auth/register?remember_me=false", json=payload
    )
    assert response.status_code == 200
    assert "access_token" in response.json()
    assert "refresh_token=" in response.headers["set-cookie"]


def test_register_user_duplicate_email_returns_409(client):
    client_instance, _ = client
    payload = {
        "email": "dupe@example.com",
        "password": "Pass!",
        "display_name": "First",
    }
    client_instance.post("/api/v1/auth/register?remember_me=false", json=payload)
    second = client_instance.post(
        "/api/v1/auth/register?remember_me=true", json=payload
    )
    assert second.status_code == 409


def test_login_user_success(client):
    client_instance, _ = client
    register_payload = {
        "email": "login@example.com",
        "password": "StrongPass123!",
        "display_name": "Login User",
    }
    client_instance.post(
        "/api/v1/auth/register?remember_me=false", json=register_payload
    )

    login_response = client_instance.post(
        "/api/v1/auth/login?remember_me=false",
        data={"username": "login@example.com", "password": "StrongPass123!"},
    )

    assert login_response.status_code == 200
    assert "access_token" in login_response.json()


def test_login_user_invalid_credentials_returns_401(client):
    client_instance, _ = client
    response = client_instance.post(
        "/api/v1/auth/login?remember_me=false",
        data={"username": "missing@example.com", "password": "wrong"},
    )

    assert response.status_code == 401


def test_refresh_with_cookie_returns_access_token(client):
    client_instance, _ = client
    reg = {"email": "ref@ex.com", "password": "123", "display_name": "Ref"}
    res = client_instance.post("/api/v1/auth/register?remember_me=true", json=reg)
    cookie = res.headers["set-cookie"].split(";")[0].split("=")[1]
    client_instance.cookies.set("refresh_token", cookie)
    response = client_instance.post("/api/v1/auth/refresh")
    assert response.status_code == 200
    assert "access_token" in response.json()


def test_verify_returns_current_user_fields(client):
    client_instance, user = client
    response = client_instance.get("/api/v1/auth/verify")
    assert response.status_code == 200
    assert response.json()["display_name"] == user.display_name
