from fastapi import FastAPI
from mangum import Mangum

app = FastAPI()
handler = Mangum(app)

@app.get("/")
async def read_root():
    return {"message": "Welcome to the FAST API running with AWS Lambda"}
