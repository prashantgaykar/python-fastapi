from typing import Any, Dict
from fastapi import FastAPI
from .database import init_models
from .routers import post, user, auth, test

init_models()
app = FastAPI()

app.include_router(post.router)
app.include_router(user.router)
app.include_router(auth.router)
app.include_router(test.router)


@app.get("/")
async def root():
    return "Hello World !"


@app.post("/test")
def test_post(test_data: Dict = dict()):
    print("Test Data : ", test_data)
    return "Success!"
