from sqlmodel import create_engine, SQLModel
from sqlalchemy.ext.asyncio import AsyncEngine
from sqlmodel.ext.asyncio.session import AsyncSession
from sqlalchemy.orm import sessionmaker
from app.config import settings
from ..entities.post import Post

# local machine
SQLALCHEMY_DATABASE_URL = f"postgresql+asyncpg://{settings.database_username}:Postgres%40123@{settings.database_hostname}:{settings.database_port}/{settings.database_name}"

engine = AsyncEngine(
    create_engine(
    url=SQLALCHEMY_DATABASE_URL,
    echo=True
))

async def init_db() -> None:
    async with engine.begin() as conn:
        await conn.run_sync(SQLModel.metadata.create_all)
        

async def get_session() -> AsyncSession:
    Session = sessionmaker(
        bind=engine,
        class_=AsyncSession,
        expire_on_commit=False
    )

    async with Session() as session:
        yield session
