from fastapi import FastAPI,HTTPException
from app.schemas import PostCreate,ReturnResponse
from app.db import Post, create_db_and_tables , get_async_session
from sqlalchemy.ext.asyncio import AsyncSession
from contextlib import asynccontextmanager

@asynccontextmanager
async def lifespan(app:FastAPI):
    await create_db_and_tables()
    yield

app = FastAPI(lifespan=lifespan)#automatically creates tables when the app started

text_messages = {
    1: {"title": "Morning Reminder", "content": "Walk the dogs."},
    2: {"title": "House Duty", "content": "Clean the Kitchen."},
    3: {"title": "Quiet Time", "content": "Read a book."},
    4: {"title": "Fitness Boost", "content": "Go for a run."},
    5: {"title": "Coding Session", "content": "Write some code."},
    6: {"title": "Dinner Prep", "content": "Cook dinner."},
    7: {"title": "Stay Connected", "content": "Call a friend."},
    8: {"title": "Adventure Planning", "content": "Plan a trip."},
    9: {"title": "Mindfulness Break", "content": "Meditate for 10 minutes."},
    10: {"title": "Learning Moment", "content": "Watch a tutorial video."}
}

@app.get("/posts")
def get_all_posts(limit: int=None):
    if limit:
        return list(text_messages.values())[:limit]
    return text_messages


@app.get("/posts/{id}")
def get_posts(id: int):
    if id not in text_messages:
        raise HTTPException(status_code=404,detail="Post not found")
    return text_messages.get(id)

@app.post("/posts")
def create_posts(post: PostCreate)->ReturnResponse:
    new_post = {"title": post.title,"content": post.content}
    text_messages[max(text_messages.keys())+1] = new_post
    return new_post
