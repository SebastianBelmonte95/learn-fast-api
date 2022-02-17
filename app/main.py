from fastapi import FastAPI
from . import models
from .database import engine
from .routers import post, user, auth
from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse

models.Base.metadata.create_all(bind=engine)
app = FastAPI()

app.include_router(post.router)
app.include_router(user.router)
app.include_router(auth.router)


@app.get("/")
async def root():
    return {"message": "Welcome to an API working with SQL Alchemy"}


@app.exception_handler(ValueError)
async def value_error_exception_handler(request: Request, exc: ValueError):
    return JSONResponse(
        status_code=400,
        content={"message": str(exc)},
    )
