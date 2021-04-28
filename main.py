import datetime
import os

from fastapi import FastAPI, HTTPException, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import Response
from pydantic import BaseModel

import mydb

app = FastAPI()


class class_ten_data(BaseModel):
    value: list
    access_token: str


app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


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


@app.get("/class_ten")
async def get_class_ten(request: Request):
    return mydb.get_class_ten()


@app.post("/class_ten")
async def post_class_ten(data: class_ten_data):
    if data.access_token != os.getenv("API_AT"):
        raise HTTPException(status_code=403)
    class_name = data.value[1][1] + data.value[2][0]
    status = data.value[3]
    updated_at = datetime.datetime.now()
    if data.value[4] == "変更しない":
        mydb.update_class_ten(class_name, status, "", False, updated_at)
    elif data.value[4] == "削除する":
        mydb.update_class_ten(class_name, status, "", True, updated_at)
    elif data.value[4] == "更新する":
        comment = data.value[5]
        mydb.update_class_ten(class_name, status, comment, False, updated_at)
    else:
        raise HTTPException(status_code=400)
    return 0
