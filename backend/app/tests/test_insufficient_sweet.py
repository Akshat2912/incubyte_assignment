import pytest

@pytest.mark.asyncio
async def test_purchase_insufficient_stock(client, auth_headers):
    sweet_data = {
    "name": "Barfi",
    "price": 20.0,
    "quantity": 1,
    "category": "Mithai"
    }

    create = await client.post("/api/sweets/", json=sweet_data, headers=auth_headers)
    sweet = create.json()

    # Try purchasing more than available
    resp = await client.post(f"/api/sweets/{sweet['id']}/purchase", json={"qty": 5}, headers=auth_headers)
    assert resp.status_code in (400, 422)
    data = resp.json()
    assert "insufficient" in data.get("detail", "").lower()
