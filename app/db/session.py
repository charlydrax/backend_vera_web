from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker
from app.core.config import settings

# URL async : note le "postgresql+asyncpg://"
DATABASE_URL_ASYNC = settings.database_url.replace("postgresql://", "postgresql+asyncpg://")

engine = create_async_engine(DATABASE_URL_ASYNC, echo=True)

# Session factory async
AsyncSessionLocal = sessionmaker(
    bind=engine,
    class_=AsyncSession,
    expire_on_commit=False
)

# Dependency pour FastAPI
async def get_db():
    async with AsyncSessionLocal() as session:
        yield session
