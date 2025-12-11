# FastAPI Social Media - Course Notes

## Table of Contents
- [Running the Application](#running-the-application)
- [Basic FastAPI Setup](#basic-fastapi-setup)
- [Key Concepts](#key-concepts)
  - [Decorators](#decorators)
  - [Async Functions](#async-functions)

---

## Running the Application

To run the FastAPI application in development mode with auto-reload:

```bash
uvicorn main:app --reload
```

---

## Basic FastAPI Setup

Here's the minimal setup for a FastAPI application:

```python
from fastapi import FastAPI

app = FastAPI()

@app.get("/")
async def root():
    return {"message": "Hello World"}
```

---

## Key Concepts

### Decorators

A **decorator** is a way to extend the functionality of a function. When we apply a decorator in FastAPI (like `@app.get("/")`), it tells FastAPI to receive requests at this specific endpoint.

### Async Functions

The `async` keyword in front of a function means that this function can run more or less at the same time as other functions. 

**Important notes about async:**
- If any of the functions that we are trying to run at the same time do heavy computation, then they can't run at the same time
- However, if they are all just waiting for:
  - The client to send us some data
  - The database to respond to our requests
  - Other I/O operations
  
Then those functions can run in parallel more or less. **This is where we get a speed benefit when we're using FastAPI and async functions.**

---



### linting and Formatting

## Ruff

- Ruff is a Python linter and formatter that enforces a consistent code style and helps catch common errors. It is a fast and opinionated linter that is easy to use and can be integrated into your development workflow.    





### adding posts to our API