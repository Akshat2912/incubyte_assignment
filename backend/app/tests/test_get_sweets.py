import pytest

@pytest.mark.asyncio
async def test_get_sweets_list(client):
    resp = await client.get("/api/sweets/")
    assert resp.status_code == 200
    assert isinstance(resp.json(), list)
