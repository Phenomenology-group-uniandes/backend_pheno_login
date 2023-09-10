from fastapi import FastAPI
from sqlmodel import SQLModel

from .users import user_router

app = FastAPI(
    title="Detector School Bootcamp",
    description="This is a very fancy project, with auto docs for the API and everything",  # noqa
    version="0.0.1",
)


@app.on_event("startup")
def on_startup():
    from app.db import engine

    from .users import User  # noqa

    SQLModel.metadata.create_all(engine)


def get_app() -> FastAPI:
    app.include_router(user_router)

    return app
