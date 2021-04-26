from fastapi import FastAPI, Request, HTTPException
from fastapi.responses import Response
from pydantic import BaseModel
import os

app = FastAPI()


class class_ten_data(BaseModel):
    value: list
    access_token: str


@app.middleware("http")
async def head(request: Request, call_next):
    if request.method == "HEAD":
        response = Response()
    else:
        response = await call_next(request)
    return response


@app.get("/")
async def root(request: Request):
    return {"message": "hello, world"}


@app.post("/class_ten")
async def class_ten(data: class_ten_data):
    if data.access_token != os.getenv("API_AT"):
        raise HTTPException(status_code=403)
    print(data.value)
    return 0
