from fastapi import FastAPI
from app.posts.router import router as posts_router
from app.auth.router import router as auth_router

app = FastAPI()

app.include_router(posts_router, tags=["posts"])
app.include_router(auth_router, tags=["auth"])


@app.get("/")
async def read_root():
    return {"message": "Welcome to the FAST API running with AWS Lambda"}
