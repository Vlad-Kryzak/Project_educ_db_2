from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker
from sqlalchemy.exc import SQLAlchemyError

DATABASE_URL = "sqlite+aiosqlite:///./database.db"

engine = create_async_engine(
    DATABASE_URL,
    echo=True,
    future=True
)

async_session = sessionmaker(
    engine,
    class_=AsyncSession,
    expire_on_commit=False
)

async def get_db():
    """
    Зависимость FastAPI для получения сессии базы данных.
    """
    async with async_session() as session:
        try:
            yield session
        except SQLAlchemyError as e:
            await session.rollback()
            raise e
        finally:
            await session.close()

async def init_db():
    """
    Создание всех таблиц по моделям.
    """
    from models import Base
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    print("✅ База данных и таблицы созданы")
