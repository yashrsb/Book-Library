from sqlmodel import create_engine, text, SQLModel
from sqlalchemy.ext.asyncio import create_async_engine, AsyncEngine
from sqlmodel.ext.asyncio.session import AsyncSession
from sqlalchemy.orm import sessionmaker

from config import Config

async_engine = AsyncEngine (
    create_engine(
    url=Config.DATABASE_URL
    )
)


async def init_db():
    print("Initializing DB connection...")
    try:
        async with async_engine.begin() as conn:
            from src.db.models import Book

            await conn.run_sync(SQLModel.metadata.create_all)
    except Exception as e:
        print(e)

async def get_session() ->AsyncSession:
    session = sessionmaker(
        bind=async_engine,
        class_=AsyncSession,
        expire_on_commit=False
    )
    async with session() as session:
        yield session


