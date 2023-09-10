from sqlmodel import Field, SQLModel


class UserBase(SQLModel):
    username: str = Field(
        default=None, description="The username of the user", unique=True
    )
    email: str = Field(default=None, description="The email of the user")
    password: str = Field(default=None, description="The password of the user")
    container_name: str | None = Field(
        default=None, description="The container name of the user"
    )


class User(UserBase, table=True):
    id: int = Field(default=None, primary_key=True)


class UserCreate(UserBase):
    pass


class UserRead(SQLModel):
    id: int
    username: str
    email: str
    container_name: str | None
