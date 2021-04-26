from fastapi import FastAPI, Request
from fastapi.responses import Response

app = FastAPI()


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
