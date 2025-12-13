# Setting Up Pytest Fixtures with `conftest.py`

When working with **FastAPI** and **Pytest**, we often need to share setup code (like database cleaning or client creation) across multiple test files. We do this using a file named `conftest.py`.

Here is a beginner-friendly breakdown of our testing configuration, explaining exactly what each part does.

## 1. The Imports
We import tools to run tests, manage types, and interact with our FastAPI app.
- `pytest`: The testing framework.
- `TestClient` & `AsyncClient`: Tools to send requests to our API without running a full server.
- `app`, `post_table`, `comment_table`: Our actual application code to test.

## 2. Setting Up the Async Environment
Since FastAPI is asynchronous, our tests needs an async environment to run in.

```python
@pytest.fixture(scope="session")
def anyio_backend():
    """
    Tells pytest to use 'asyncio' as the backend for async tests.
    scope="session" means this setup runs only ONCE for the entire test suite.
    """
    return "asyncio"
```

## 3. The Synchronous Client
This fixture creates a standard client. While we might test asynchronously, the `TestClient` is often useful for synchronous operations or as a base.

```python
@pytest.fixture()
def client() -> Generator:
    """
    Creates a TestClient instance.
    'yield' is used instead of 'return' to allow for setup/teardown logic (code before/after yield).
    """
    yield TestClient(app)
```

## 4. The Database Fixture (Auto-Reset)
We need to ensure every test starts with a clean slate. This fixture clears our "database" (lists) before every single test.

```python
@pytest.fixture(autouse=True)
async def db() -> AsyncGenerator:
    """
    Clears the post and comment tables.
    autouse=True: Runs automatically for EVERY test function, so we don't need to call it manually.
    """
    post_table.clear()
    comment_table.clear()
    yield
```

## 5. The Async Client
This is the workhorse for our async tests. It allows us to `await` responses from our API.

**Note on Dependency Injection:** notice `async_client(client)`. Pytest automatically finds the `client` fixture we defined earlier and passes it into this function. This is how fixtures can use other fixtures!

```python
@pytest.fixture()
async def async_client(client) -> AsyncGenerator:
    """
    Creates an HTTPX AsyncClient for making async API requests.
    It reuses the base_url from our synchronous 'client' fixture.
    """
    async with AsyncClient(app=app, base_url=client.base_url) as ac:
        yield ac
```
