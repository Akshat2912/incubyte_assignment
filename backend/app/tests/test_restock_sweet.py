import pytest

@pytest.mark.asyncio
async def test_restock_sweet(client, auth_headers):
    # Add a sweet first
    sweet_data = {
    "name": "Rasgulla",
    "price": 12.0,
    "quantity": 10,
    "category": "Mithai"
    }

    create = await client.post("/api/sweets/", json=sweet_data, headers=auth_headers)
    sweet = create.json()

    # Restock 5 more
    resp = await client.post(f"/api/sweets/{sweet['id']}/restock", json={"qty": 5}, headers=auth_headers)
    assert resp.status_code == 200
    updated = resp.json()
    assert updated["quantity"] == 15
