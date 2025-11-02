import pytest

@pytest.mark.asyncio
async def test_purchase_sweet(client, auth_headers):
    # Add a sweet first
    sweet_data = {
    "name": "Jalebi",
    "price": 10.0,
    "quantity": 5,
    "category": "Mithai"
    }

    create = await client.post("/api/sweets/", json=sweet_data, headers=auth_headers)
    sweet = create.json()

    # Purchase 2
    resp = await client.post(f"/api/sweets/{sweet['id']}/purchase", json={"qty": 2}, headers=auth_headers)
    assert resp.status_code == 200
    updated = resp.json()
    assert updated["quantity"] == 3
