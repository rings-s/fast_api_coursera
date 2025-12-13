# FastAPI Routers - Organizing Your API

## Overview
API routers allow you to organize your FastAPI application into separate modules. Instead of having all endpoints in `main.py`, you can split them into logical groups (posts, users, comments, etc.) and include them in your main application.

---

## What is an APIRouter?

**An API router is basically a FastAPI app, but instead of running on its own, it can be included into an existing app.**

- It lets you use endpoints from the router in the original app
- Helps organize code into logical modules
- Makes the codebase more maintainable as it grows

---

## Creating a Router

### File Structure
```
social_media/
├── routers/
│   └── posts.py
├── models/
│   └── post.py
└── main.py
```

### routers/posts.py

```python
from fastapi import APIRouter
from models.post import UserPostIn, UserPost

# Create a router instance instead of a FastAPI app
router = APIRouter()

# Database (in-memory for now)
post_table = []

# Define endpoints using @router instead of @app
@router.post("/posts")
async def create_post(post: UserPostIn):
    data = post.dict()
    last_record_id = len(post_table)
    new_post = {**data, "id": last_record_id}
    post_table[last_record_id] = new_post
    return new_post

@router.get("/posts", response_model=list[UserPost])
async def get_all_posts():
    return list(post_table.values())
```

### Key Changes from main.py

1. **Import APIRouter instead of FastAPI**:
   ```python
   from fastapi import APIRouter  # Instead of: from fastapi import FastAPI
   ```

2. **Create a router instance**:
   ```python
   router = APIRouter()  # Instead of: app = FastAPI()
   ```

3. **Use @router decorators**:
   ```python
   @router.post("/posts")  # Instead of: @app.post("/posts")
   @router.get("/posts")   # Instead of: @app.get("/posts")
   ```

---

## Including the Router in main.py

### main.py

```python
from fastapi import FastAPI
from routers.posts import router as posts_router

app = FastAPI()

# A decorator is a way to extend the functionality of a function
# async allows functions to run concurrently when waiting for I/O operations
@app.get("/")
async def root():
    return {"message": "Hello World"}

# Include the posts router
app.include_router(posts_router)
```

### Import with Alias

```python
from routers.posts import router as posts_router
```

**Why use an alias?**
- We might have multiple routers in our application (users, comments, etc.)
- Each router file exports a variable named `router`
- Using aliases (`posts_router`, `users_router`) makes it clear which router is which
- Prevents naming conflicts

### Including the Router

```python
app.include_router(posts_router)
```

This line tells FastAPI to include all the endpoints from `posts_router` into the main app.

---

## Router Prefixes (Optional)

You can add a prefix to all endpoints in a router. This can help organize your API and avoid repeating the same path segment.

### Adding a Prefix

```python
# In main.py
app.include_router(posts_router, prefix="/posts")
```

### How Prefixes Work

**Without prefix:**
- Endpoint in router: `@router.post("/posts")`
- Final URL: `http://127.0.0.1:8000/posts`

**With prefix="/posts":**
- Endpoint in router: `@router.post("/create")`
- Final URL: `http://127.0.0.1:8000/posts/create`

### Example with Prefix

**routers/posts.py:**
```python
@router.post("/create")
async def create_post(post: UserPostIn):
    # ... code ...

@router.get("/")
async def get_all_posts():
    # ... code ...
```

**main.py:**
```python
app.include_router(posts_router, prefix="/posts")
```

**Resulting URLs:**
- `POST /posts/create` - Create a post
- `GET /posts/` - Get all posts

### Note on Prefixes in This Course

**We're NOT using prefixes in this course**, but they're available if you want to use them. They can simplify your router definitions, but they're optional.

---

## Benefits of Using Routers

### 1. **Code Organization**
- Each router handles a specific domain (posts, users, comments)
- Easy to find and maintain related endpoints
- Cleaner `main.py` file

### 2. **Separation of Concerns**
- Each router can have its own database connections, models, and logic
- Changes to one router don't affect others
- Easier to test individual routers

### 3. **Scalability**
- As your API grows, you can add more routers
- Team members can work on different routers simultaneously
- Easier to refactor and reorganize

### 4. **Reusability**
- Routers can be reused in different applications
- Can create router libraries for common functionality

---

## Testing the Router

### Using Insomnia

1. **Start the server**:
   ```bash
   uvicorn main:app --reload
   ```

2. **Create a post**:
   - Method: POST
   - URL: `http://127.0.0.1:8000/posts`
   - Body:
     ```json
     {
       "body": "Testing the router!"
     }
     ```

3. **Get all posts**:
   - Method: GET
   - URL: `http://127.0.0.1:8000/posts`

The endpoints work exactly the same as before, but now the code is better organized!

---

## Complete Code Example

### routers/posts.py
```python
from fastapi import APIRouter
from models.post import UserPostIn, UserPost

router = APIRouter()

post_table = []

@router.post("/posts")
async def create_post(post: UserPostIn):
    data = post.dict()
    last_record_id = len(post_table)
    new_post = {**data, "id": last_record_id}
    post_table[last_record_id] = new_post
    return new_post

@router.get("/posts", response_model=list[UserPost])
async def get_all_posts():
    return list(post_table.values())
```

### models/post.py
```python
from pydantic import BaseModel

class UserPostIn(BaseModel):
    body: str

class UserPost(UserPostIn):
    id: int
```

### main.py
```python
from fastapi import FastAPI
from routers.posts import router as posts_router

app = FastAPI()

@app.get("/")
async def root():
    return {"message": "Hello World"}

app.include_router(posts_router)
```

---

## Key Takeaways

1. **APIRouter** is like a mini FastAPI app that can be included in the main app
2. Use `@router` decorators instead of `@app` in router files
3. Import routers with **aliases** to avoid naming conflicts
4. Use `app.include_router()` to add the router to your main application
5. **Prefixes** are optional but can help organize your API structure
6. Routers help keep your code **organized, maintainable, and scalable**

---

## What's Next?

As your API grows, you can create more routers:
- `routers/users.py` - User management endpoints
- `routers/comments.py` - Comment endpoints
- `routers/auth.py` - Authentication endpoints

Each router follows the same pattern:
1. Import `APIRouter`
2. Create a `router` instance
3. Define endpoints with `@router` decorators
4. Import and include in `main.py`
