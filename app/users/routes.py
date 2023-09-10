from fastapi import APIRouter  # , Depends, HTTPException, status


user_router = APIRouter(
    prefix="/users",
    tags=["users"],
)


@user_router.get("/")
async def get_users():
    return {"message": "Hello World"}


@user_router.get("/{username}")
async def get_user(username: str):
    return {"message": f"Hello {username}"}


@user_router.post("/")
async def create_user():
    return {"message": "Hello World"}
