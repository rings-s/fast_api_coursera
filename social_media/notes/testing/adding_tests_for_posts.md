# Writing Tests for Post Endpoints

In this section, we write actual test functions to verify our API behaves as expected. We define three main tests.

## 1. Testing Post Creation (`test_create_post`)

This test ensures we can successfully create a new post.

```python
@pytest.mark.anyio
async def test_create_post(async_client: AsyncClient):
    body = "test post"
    response = await async_client.post("/posts", json={"body": body})
    
    # Assert status code is 201 (Created)
    assert response.status_code == 201
    
    # Assert that the expected data (id and body) is present in the response
    # We use <= to check if our subset of data exists in the response
    assert {"id": 0, "body": body}.items() <= response.json().items()
```

### Key Concepts:
*   **`@pytest.mark.anyio`**: Marks this as an async test so Pytest uses the AnyIO backend.
*   **No Fixture**: We do *not* use `created_post` here because the goal is to test the creation process itself.
*   **Resilient Assertion**: Using `<= response.json().items()` allows the API to return *extra* fields (like a timestamp) without breaking the test, as long as the data we care about is correct.

---

## 2. Testing Missing Data (`test_create_post_missing_data`)

This test ensures the API correctly rejects invalid requests (e.g., missing body).

```python
@pytest.mark.anyio
async def test_create_post_missing_data(async_client: AsyncClient):
    # Send a POST request with an empty JSON object
    response = await async_client.post("/posts", json={})
    
    # Assert status code is 422 (Unprocessable Entity)
    # FastAPI/Pydantic automatically handles this validation
    assert response.status_code == 422
```

### Key Concepts:
*   **Validation**: We expect a **422** error because the `UserPostIn` model requires a `body` field. If we send nothing, Pydantic catches it.

---

## 3. Testing Get All Posts (`test_all_posts`)

This test ensures we can retrieve the list of posts.

```python
@pytest.mark.anyio
async def test_all_posts(async_client: AsyncClient, created_post: dict):
    # Retrieve all posts
    response = await async_client.get("/posts")
    
    # Assert success and that the list contains our created post
    assert response.status_code == 200
    assert response.json() == [created_post]
```

### Key Concepts:
*   **Using Fixtures**: We pass `created_post` as an argument.
    1.  Pytest runs the `created_post` fixture *before* the test.
    2.  The fixture creates a post in the database.
    3.  The test runs, ensuring there is data to retrieve.
*   **Database Isolation**: Because of our `db` autouse fixture (in `conftest.py`), the database is cleared before this sequence starts, guaranteeing exactly one post exists (the one we just created).
