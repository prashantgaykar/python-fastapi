from typing import Any, Dict
from fastapi import FastAPI, Body, Request
from fastapi.responses import FileResponse
from .database import init_models
from .routers import post, user, auth, test
from . import gps_util

init_models()
app = FastAPI()

app.include_router(post.router)
app.include_router(user.router)
app.include_router(auth.router)
app.include_router(test.router)


@app.get("/")
async def root():
    return {"message": "Hello World !"}


@app.post("/test")
def test_post(test_data: Dict = dict()):
    print("Test Data : ", test_data)
    return "Success!"


@app.post("/text")
async def test_post(request: Request):
    data = await request.body()
    loc_raw_data = str(data, 'utf-8')
    print("TEXT : ", loc_raw_data)
    gps_util.save_location_data(loc_raw_data)
    return "Success!"


@app.get("/gf")
async def get_file():
    print("downloading location file.")
    try:
        return FileResponse(path=gps_util.get_file_path(), media_type='application/octet-stream',filename='location.kml')
    except RuntimeError as e:
        return "File not found"
