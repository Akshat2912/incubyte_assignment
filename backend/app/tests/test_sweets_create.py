import pytest

@pytest.mark.asyncio
async def test_create_sweet(client, auth_headers):
    sweet_data = {
    "name": "Ladoo",
    "price": 15.5,
    "quantity": 20,
    "category": "Mithai"
    }

    resp = await client.post("/api/sweets/", json=sweet_data, headers=auth_headers)
    print("RESPONSE STATUS:", resp.status_code)
    print("RESPONSE JSON:", resp.json())
    assert resp.status_code in (200, 201)

