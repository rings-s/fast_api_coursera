# Creating Posts in Tests: A Beginner's Guide

This guide explains how we set up our tests to create posts. Instead of rewriting the code to create a post in every single test, we use helper functions and **Pytest Fixtures**.

## 1. The Helper Function: `create_post`

First, we define a standard helper function.

*   **Not a Test or Fixture:** This is just a regular Python `async` function. It doesn't start with `test_` and isn't decorated with `@pytest.fixture`.
*   **Purpose:** It wraps the logic of making a POST request to our API.
*   **Arguments:** It takes the `body` content and the `async_client` to make the request.

```python
async def create_post(body: str, async_client: AsyncClient) -> dict:
    # Sends a POST request to the "/posts" endpoint using the client fixture
    response = await async_client.post("/posts", json={"body": body})
    return response.json()
```

## 2. The Fixture: `created_post`

Next, we wrap that helper function in a Pytest fixture. This is where the magic happens.

*   **Dependency Injection:** Notice `async_client` in the arguments. Pytest automatically finds the `async_client` fixture (defined in `conftest.py`) and passes it in.
*   **Why use this?** If a test needs a post to exist *before* it starts (e.g., to test "Get Post"), we just add `created_post` to that test's arguments. Pytest will run this fixture first, create the post, and pass the result to the test.

```python
@pytest.fixture()
async def created_post(async_client: AsyncClient):
    # This fixture ensures a post exists before the test runs.
    # It calls our helper function and returns the created post data.
    return await create_post("test post", async_client)
```

### Hierarchy of Fixtures
When `created_post` asks for `async_client`:
1.  Pytest looks in the current file (`test_posts.py`). Not there.
2.  It looks in `tests/routers/conftest.py`. Not there.
3.  It finds it in the parent `tests/conftest.py`. Success!
