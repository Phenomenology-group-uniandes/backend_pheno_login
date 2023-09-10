from fastapi import APIRouter, Depends, HTTPException, status
from sqlmodel import select

from app.db import Session, get_session
from app.utils import hash_password, verify_password

from .models import User, UserCreate, UserRead

user_router = APIRouter(
    prefix="/users",
    tags=["users"],
)


@user_router.get("/")
async def get_users(
    session: Session = Depends(get_session),
) -> list[UserRead]:
    db_users = session.exec(select(User)).all()
    return db_users


@user_router.get("/{username}")
async def get_user(
    username: str,
    session: Session = Depends(get_session),
) -> UserRead:
    db_user = session.exec(select(User).where(User.username == username)).first()
    if not db_user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"User with username {username} not found",
        )
    return db_user


@user_router.post("/")
async def create_user(
    user: UserCreate,
    session: Session = Depends(get_session),
) -> UserRead:
    # Check if user already exists
    db_user = session.exec(select(User).where(User.username == user.username)).first()
    if db_user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"User with username {user.username} already exists",
        )
    db_user = User.from_orm(user)
    db_user.password = hash_password(db_user.password)
    session.add(db_user)
    session.commit()
    session.refresh(db_user)
    return db_user


@user_router.post("/login")
async def login_user(
    username: str,
    password: str,
    session: Session = Depends(get_session),
) -> bool:
    db_user = session.exec(select(User).where(User.username == username)).first()
    if not db_user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"User with username {username} not found",
        )
    if not verify_password(password, db_user.password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect password",
        )
    return True
