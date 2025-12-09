from fastapi import FastAPI


app = FastAPI()

# A decorator is a way to extend the functionality of a function. when we apply a decorator it tells fast api to recieve requests at this endpoint
# async in front of a function just means that this function can run more or less at the same time as other functions. If any of the functions that we are trying to run at the same time, do heavy computation, then they can't run at the same time. But if they are all just waiting for the client to send us some data or they're waiting for the database to respond to our requests or things like that, then those functions can run in parallel more or less. So that is where we get a speed benefit when we're using fast API and async functions. So that is where we get a speed benefit when we're using fast API and async functions. 
@app.get("/")
async def root():
    return {"message": "Hello World"}

