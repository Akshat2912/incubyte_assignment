import pytest

@pytest.mark.asyncio
async def test_register_and_login(client):
    username = "user_login_test"
    r = await client.post("/api/auth/register", json={"username": username, "password": "pass"})
    assert r.status_code == 200
    data = r.json()
    assert "access_token" in data

    r2 = await client.post("/api/auth/login", data={"username": username, "password": "pass"})
    assert r2.status_code == 200
    assert "access_token" in r2.json()
