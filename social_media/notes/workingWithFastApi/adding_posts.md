# Adding Posts to FastAPI - Course Notes

## Overview
In this section, we're working on adding posts to a database using our REST API. We'll start by defining what requests will be made in Insomnia, then write the code to fulfill those requests.

---

## HTTP Methods and REST API Concepts

### POST Requests
- **POST requests** are used to send data to a server to create a resource
- In this case, we're using a POST request to create posts (a bit confusing since we're POSTing posts!)
- The HTTP method (POST) is not customizable - you should use the method that's most commonly used for the type of operation you're performing
- **For creating resources, we use POST**

### Endpoint Structure
```
POST http://127.0.0.1:8000/posts
```

**Request Body (JSON):**
```json
{
  "body": "This is my first post"
}
```

- The endpoint path (`/posts`) is customizable
- The field names (`body`) are customizable by the API developers
- The HTTP method (POST) should follow conventions

---

## Setting Up the Models

### Pydantic BaseModel
```python
from pydantic import BaseModel
```

- **BaseModel** is a class from Pydantic that allows us to define a model
- Models are used to **validate data**
- We need to validate the data that the client sends us

### Creating the Models

#### UserPostIn - For Incoming Data
```python
class UserPostIn(BaseModel):
    body: str
```

- **Convention**: Classes ending in `In` represent data coming INTO our API
- Uses Python type hinting to define fields
- `body: str` means the body field must be a string
- Pydantic will automatically validate that:
  - The `body` field exists
  - The `body` field is a string

#### UserPost - For Outgoing Data
```python
class UserPost(UserPostIn):
    id: int
```

- Inherits from `UserPostIn` (gets the `body` field)
- Adds an `id` field which is an integer
- This is what we return to the user (includes both body and the unique identifier we generate)

---

## Data Storage

### In-Memory Database (Dictionary)
```python
post_table = {}
```

- For now, we're using a Python **dictionary** as our database
- Later in the course, we'll introduce SQL databases (SQLite and PostgreSQL)
- **Important**: Data stored in a dictionary doesn't persist across application restarts
- Whenever you save a file (triggering a reload), all data is lost

---

## Creating the POST Endpoint

### Endpoint Definition
```python
@app.post("/posts", response_model=UserPost)
async def create_post(post: UserPostIn):
    data = post.dict()
    last_record_id = len(post_table)
    new_post = {**data, "id": last_record_id}
    post_table[last_record_id] = new_post
    return new_post
```

### How FastAPI Handles This

1. **Automatic Detection**: FastAPI detects that `post` is a Pydantic model
2. **JSON Body Parsing**: It knows the data comes from the JSON body of the request (not from query parameters)
3. **Automatic Validation**: FastAPI checks that:
   - The `body` field is in the JSON payload
   - The `body` field is a string
4. **Object Construction**: If validation passes, it constructs a `UserPostIn` object and passes it as the `post` variable
5. **Response Validation**: The `response_model=UserPost` ensures the response matches the UserPost model

### Code Breakdown

```python
data = post.dict()
```
- Converts the Pydantic model to a Python dictionary

```python
last_record_id = len(post_table)
```
- Gets the number of records in the database to use as the new ID

```python
new_post = {**data, "id": last_record_id}
```
- **Dictionary unpacking** with `**data`
- Creates a new dictionary containing all fields from `data` PLUS the `id` field
- Example result: `{"body": "This is my first post", "id": 0}`

```python
post_table[last_record_id] = new_post
```
- Stores the new post in the dictionary
- Uses the ID as the key for easier retrieval later

```python
return new_post
```
- Returns the new post (body + ID)
- FastAPI automatically converts this to JSON

---

## Creating the GET Endpoint

### Endpoint Definition
```python
@app.get("/posts", response_model=list[UserPost])
async def get_all_posts():
    return list(post_table.values())
```

### Response Model for Lists
```python
response_model=list[UserPost]
```
- Uses Python type hinting with square brackets
- `list[UserPost]` means we're responding with a list containing UserPost objects
- Pydantic and FastAPI will convert everything to JSON correctly

### Code Breakdown

```python
return list(post_table.values())
```
- `post_table.values()` gets all the values from the dictionary
- `list()` converts it to a Python list
- Pydantic converts the list of UserPost objects back to JSON
- Each object becomes a dictionary with `id` and `body` fields

---

## Testing the API

### Using Insomnia

1. **Create a POST request**:
   - Method: POST
   - URL: `http://127.0.0.1:8000/posts`
   - Body (JSON):
     ```json
     {
       "body": "This is my first post"
     }
     ```
   - Response: `{"body": "This is my first post", "id": 0}`

2. **Create a GET request**:
   - Method: GET
   - URL: `http://127.0.0.1:8000/posts`
   - Response: Array of all posts

### Running the Application
```bash
uvicorn main:app --reload
```
- The `--reload` flag makes the app restart when you make code changes
- **Remember**: Restarting the app deletes all data (since we're using a dictionary)

---

## Organizing Code into Multiple Files

### Why Split Code?
As the API grows with more endpoints, keeping everything in `main.py` becomes messy. We need to organize our code into separate files.

### Creating the Models Module

**File structure:**
```
social_media/
├── models/
│   └── post.py
└── main.py
```

**models/post.py:**
```python
from pydantic import BaseModel


class UserPostIn(BaseModel):
    body: str


class UserPost(UserPostIn):
    id: int
```

**main.py:**
```python
from fastapi import FastAPI
from models.post import UserPostIn, UserPost

app = FastAPI()

# ... rest of the code
```

### Import Statement
```python
from models.post import UserPostIn, UserPost
```
- Imports the models from the `models/post.py` file
- Keeps `main.py` cleaner and more focused on endpoints

---

## Key Takeaways

1. **POST requests** are used to create resources
2. **Pydantic models** validate incoming and outgoing data automatically
3. **Type hinting** is used to define model fields and response types
4. **Dictionary unpacking** (`{**data, "id": value}`) combines dictionaries
5. **In-memory storage** (dictionaries) doesn't persist across restarts
6. **Code organization** is important - split models into separate files
7. **FastAPI automatically**:
   - Validates request data
   - Converts Pydantic models to/from JSON
   - Generates API documentation

---

## What's Next?

In the next video, we'll learn how to:
- Extract endpoint code from `main.py` into separate files
- Keep the codebase organized as we add more endpoints
- Use proper project structure for larger APIs

Later in the course:
- Test-driven development (TDD)
- SQL databases (SQLite and PostgreSQL)
- More HTTP methods (PUT, DELETE, etc.)
