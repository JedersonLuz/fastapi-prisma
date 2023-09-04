from fastapi import Depends, FastAPI
from prisma import Prisma

from .dependencies import get_query_token, get_token_header
from .internal import admin
from .routers import posts, users

app = FastAPI()


app.include_router(
    users.router, 
    dependencies=[Depends(get_query_token)]
)
app.include_router(
    posts.router, 
    dependencies=[Depends(get_query_token)]
)
app.include_router(
    admin.router,
    prefix="/admin",
    tags=["admin"],
    dependencies=[Depends(get_token_header)],
    responses={418: {"description": "I'm a teapot"}},
)


db = Prisma()


@app.on_event("startup")
async def startup():
    await db.connect()


@app.on_event("shutdown")
async def shutdown():
    await db.disconnect()


@app.get("/")
async def root():
    return {"message": "Hello Bigger Applications!"}
