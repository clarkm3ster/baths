"""Shared test fixtures for SPHERE/OS."""

import pytest
from httpx import ASGITransport, AsyncClient

from src.shared.app import app


@pytest.fixture
async def client():
    """Async HTTP client for testing FastAPI endpoints."""
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as ac:
        yield ac
