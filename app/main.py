from fastapi import FastAPI
from mangum import Mangum
from app.posts.router import router as posts_router

app = FastAPI()

app.include_router(posts_router, tags=["posts"])


@app.get("/")
async def read_root():
    return {"message": "Welcome to the FAST API running with AWS Lambda"}


handler = Mangum(app)
