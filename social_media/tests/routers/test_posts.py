import pytest
from httpx import AsyncClient


async def create_post(body: str, async_client: AsyncClient) -> dict:
    # Helper function creates a post via the API using the test client
    response = await async_client.post("/posts", json={"body": body})
    return response.json()


@pytest.fixture()
async def created_post(async_client: AsyncClient):
    # Fixture that ensures a post creates before a test runs
    # Returns the API response (the created post) to the test function
    return await create_post("test post", async_client)


@pytest.mark.anyio
async def test_create_post(async_client: AsyncClient):
    body = "test post"
    response = await async_client.post("/posts", json={"body": body})
    assert response.status_code == 201
    assert {"id": 0, "body": body}.items() <= response.json().items()


@pytest.mark.anyio
async def test_create_post_missing_data(async_client: AsyncClient):
    response = await async_client.post("/posts", json={})
    assert response.status_code == 422


@pytest.mark.anyio
async def test_all_posts(async_client: AsyncClient, created_post: dict):
    response = await async_client.get("/posts")
    assert response.status_code == 200
    assert response.json() == [created_post]
