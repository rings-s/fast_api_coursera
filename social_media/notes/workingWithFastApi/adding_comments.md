# Adding Comments to Posts

## Overview
This guide covers how to add comments functionality to posts in a FastAPI application. The thought process for adding any new feature to an API follows these steps:

1. **Define data models** - What data the user sends and what you send back
2. **Plan database storage** - What data you'll store in your database
3. **Create endpoints** - The interface with the user

## Data Models

### CommentIn (Input Model)
What the user sends when creating a comment:
- `body`: string - The comment text
- `post_id`: integer - The ID of the post being commented on

```python
from pydantic import BaseModel

class CommentIn(BaseModel):
    body: str
    post_id: int
```

### Comment (Output Model)
What we send back to the user (inherits from CommentIn):
- `body`: string - The comment text
- `post_id`: integer - The ID of the post
- `id`: integer - Unique identifier for the comment

```python
class Comment(CommentIn):
    id: int
```

### UserPostWithComments (Nested Model)
A model that combines a post with its comments:
- `post`: UserPost - The post object
- `comments`: list[Comment] - List of comments on that post

```python
class UserPostWithComments(BaseModel):
    post: UserPost
    comments: list[Comment]
```

**Example response structure:**
```json
{
  "post": {
    "id": 0,
    "body": "My post"
  },
  "comments": [
    {
      "id": 2,
      "post_id": 0,
      "body": "My comment"
    }
  ]
}
```

## Database Setup

### Comment Table
Create an in-memory table to store comments:

```python
comment_table = {}
```

### Helper Function
Create a function to find posts by ID:

```python
def find_post(post_id: int):
    return post_table.get(post_id)
```

## Endpoints

### 1. Create Comment
**Endpoint:** `POST /comments`  
**Status Code:** `201 Created`  
**Response Model:** `Comment`

```python
@router.post("/comments", response_model=Comment, status_code=201)
async def create_comment(comment: CommentIn):
    # Validate that the post exists
    post = find_post(comment.post_id)
    if not post:
        raise HTTPException(status_code=404, detail="Post not found")
    
    # Create the comment
    data = comment.dict()
    last_record_id = len(comment_table)
    new_comment = {**data, "id": last_record_id}
    comment_table[last_record_id] = new_comment
    
    return new_comment
```

**Key Points:**
- Always validate that the post exists before creating a comment
- Raise errors as early as possible (before doing any work)
- Use status code `201` for creating resources (not `200`)
- Status code `404` means "Not Found"
- `HTTPException` bypasses the normal Pydantic response model

### 2. Get Comments on a Post
**Endpoint:** `GET /posts/{post_id}/comments`  
**Response Model:** `list[Comment]`

```python
@router.get("/posts/{post_id}/comments", response_model=list[Comment])
async def get_comments_on_post(post_id: int):
    return [
        comment for comment in comment_table.values() 
        if comment["post_id"] == post_id
    ]
```

**Key Points:**
- Dynamic URL segments are defined with curly braces: `{post_id}`
- The parameter name must match the URL segment name
- FastAPI automatically extracts the value from the URL
- Uses list comprehension to filter comments by post_id

### 3. Get Post with Comments
**Endpoint:** `GET /posts/{post_id}`  
**Response Model:** `UserPostWithComments`

```python
@router.get("/posts/{post_id}", response_model=UserPostWithComments)
async def get_post_with_comments(post_id: int):
    # Find the post
    post = find_post(post_id)
    
    # Validate it exists
    if not post:
        raise HTTPException(status_code=404, detail="Post not found")
    
    # Return post with its comments
    return {
        "post": post,
        "comments": await get_comments_on_post(post_id),
    }
```

**Key Points:**
- You can call other endpoint functions directly (no need to make HTTP requests)
- Use `await` to wait for async functions to complete before continuing
- The response structure must match the `UserPostWithComments` model
- Adding a trailing comma helps code formatters split lines properly

## Important Concepts

### Dynamic URL Segments
When you add a parameter to an endpoint function:
- **Pydantic model parameter** → FastAPI expects it in the JSON request body
- **Non-Pydantic parameter matching URL segment** → FastAPI extracts it from the URL

Example:
```python
@router.get("/posts/{post_id}/comments")
async def get_comments_on_post(post_id: int):
    # post_id comes from the URL
```

### Status Codes
- `200 OK` - Used for retrieving resources (GET requests)
- `201 Created` - Used for creating resources (POST requests)
- `404 Not Found` - Resource doesn't exist

### Error Handling
```python
from fastapi import HTTPException

if not post:
    raise HTTPException(status_code=404, detail="Post not found")
```

- Raise errors as early as possible
- Don't do work if validation fails
- `HTTPException` bypasses the normal Pydantic response model

### Calling Endpoint Functions
You can call endpoint functions from other endpoints:

```python
comments = await get_comments_on_post(post_id)
```

- Just call the function directly
- Use `await` for async functions
- No need to make HTTP requests to your own API

### List Comprehensions
Filtering data with list comprehensions:

```python
[comment for comment in comment_table.values() if comment["post_id"] == post_id]
```

This is equivalent to:
```python
result = []
for comment in comment_table.values():
    if comment["post_id"] == post_id:
        result.append(comment)
return result
```

## Testing with Insomnia/Postman

### 1. Create a Post
```
POST /posts
{
  "body": "My first post"
}
```

### 2. Create a Comment
```
POST /comments
{
  "body": "Great post!",
  "post_id": 0
}
```

### 3. Get Comments on a Post
```
GET /posts/0/comments
```

### 4. Get Post with Comments
```
GET /posts/0
```

## FastAPI Advantages

- **Fast development** - Adding new features is quick and straightforward
- **Automatic validation** - Pydantic models validate data automatically
- **Auto-generated docs** - API documentation is created automatically
- **Type safety** - Python type hints provide IDE support and catch errors early
- **Nested models** - Easy to create complex data structures

## Next Steps

Future enhancements to consider:
- Adding tests
- User authentication
- Relational databases (replacing in-memory tables)
- Pagination for comments
- Comment editing and deletion
- Comment voting/likes
