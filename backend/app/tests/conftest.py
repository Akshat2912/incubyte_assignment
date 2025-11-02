import pytest_asyncio
from httpx import AsyncClient, ASGITransport
from app.main import app
import uuid

@pytest_asyncio.fixture
async def client():
    """Create an async test client for FastAPI."""
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as ac:
        yield ac

@pytest_asyncio.fixture
async def auth_headers(client):
    """Register and login a user, returning valid auth headers."""
    username = f"user_{uuid.uuid4().hex[:6]}"
    await client.post("/api/auth/register", json={"username": username, "password": "pass"})
    login = await client.post("/api/auth/login", data={"username": username, "password": "pass"})
    token = login.json()["access_token"]
    return {"Authorization": f"Bearer {token}"}
