# DB_CONFIG

from sqlmodel import Session, create_engine

sqlite_file_name = "database.db"
sqlite_url = f"sqlite:///{sqlite_file_name}"

engine = create_engine(sqlite_url, echo=True)


async def get_session() -> Session:
    with Session(engine) as session:
        yield session
