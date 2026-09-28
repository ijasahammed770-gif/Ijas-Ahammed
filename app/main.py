from contextlib import asynccontextmanager

from fastapi import FastAPI

from fastapi.staticfiles import StaticFiles

from .database import init_db

from .routers import (
    pages,
    auth,
    planners
)


@asynccontextmanager
async def lifespan(app: FastAPI):

    init_db()

    yield


app = FastAPI(

    title="PocketSmart AI",

    version="1.0.0",

    lifespan=lifespan
)


app.mount(

    "/static",

    StaticFiles(
        directory="app/static"
    ),

    name="static"
)


app.include_router(
    pages.router
)

app.include_router(
    auth.router
)

app.include_router(
    planners.router
)


@app.get("/health")
async def health():

    return {

        "status": "ok",

        "service":
            "PocketSmart AI"
    }


if __name__ == "__main__":

    import uvicorn

    uvicorn.run(

        "app.main:app",

        host="127.0.0.1",

        port=8000,

        reload=True
    )