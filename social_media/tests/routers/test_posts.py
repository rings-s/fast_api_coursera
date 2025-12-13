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
