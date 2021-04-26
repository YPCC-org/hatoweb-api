from fastapi import FastAPI, Request
from fastapi.responses import Response
from pydantic import BaseModel

app = FastAPI()


class class_ten_data(BaseModel):
    value: str


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
    return data
