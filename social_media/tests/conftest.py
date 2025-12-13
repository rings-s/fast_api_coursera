from typing import Generator, AsyncGenerator
import pytest
from fastapi.testclient import TestClient
from httpx import AsyncClient, ASGITransport


from social_media.main import app

from social_media.routers.posts import post_table, comment_table


@pytest.fixture(scope="session")
def anyio_backend():
    # Setup asyncio as the backend for async tests, running once per session
    return "asyncio"


@pytest.fixture()
def client() -> Generator:
    # Yields a synchronous TestClient for interacting with the API
    yield TestClient(app)


@pytest.fixture(autouse=True)
async def db() -> AsyncGenerator:
    # Automatically clears database tables before every test to ensure isolation
    post_table.clear()
    comment_table.clear()
    yield


@pytest.fixture()
async def async_client(client) -> AsyncGenerator:
    # Yields an AsyncClient for making asynchronous API requests using ASGITransport for the FastAPI app
    async with AsyncClient(
        transport=ASGITransport(app=app), base_url=client.base_url
    ) as ac:
        yield ac
