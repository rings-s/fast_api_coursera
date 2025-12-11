from fastapi import APIRouter, HTTPException

from models.post import UserPostIn, UserPost, CommentIn, Comment, UserPostWithComments

router = APIRouter()


# A decorator is a way to extend the functionality of a function. when we apply a decorator it tells fast api to recieve requests at this endpoint
# async in front of a function just means that this function can run more or less at the same time as other functions. If any of the functions that we are trying to run at the same time, do heavy computation, then they can't run at the same time. But if they are all just waiting for the client to send us some data or they're waiting for the database to respond to our requests or things like that, then those functions can run in parallel more or less. So that is where we get a speed benefit when we're using fast API and async functions. So that is where we get a speed benefit when we're using fast API and async functions.
@router.get("/")
async def root():
    return {"message": "Hello World"}


post_table = {}
comment_table = {}


def find_post(post_id: int):
    return post_table.get(post_id)


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



@router.post("/comments", response_model=Comment)
async def create_comment(comment: CommentIn):
    post = find_post(comment.post_id)
    if not post:
        raise HTTPException(status_code=404, detail="Post not found")

    data = comment.dict()
    last_record_id = len(comment_table)
    new_comment = {**data, "id": last_record_id}
    comment_table[last_record_id] = new_comment
    return new_comment


@router.get("/posts/{post_id}/comments", response_model=list[Comment])
async def get_comments_on_the_post(post_id: int):
    return [comment for comment in comment_table.values()  if comment["post_id"] == post_id]


@router.get("/posts/{post_id}", response_model=UserPostWithComments)
async def get_post_with_comments(post_id: int):
    post = find_post(post_id)
   
    if not post:
        raise HTTPException(status_code=404, detail="Post not found")

    return {"post": post, "comments": await get_comments_on_the_post(post_id)}