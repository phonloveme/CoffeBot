from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker
from bot.config import settings
from bot.database.models import Base

#движок
engine = create_async_engine(settings.DATABASE_URL,echo=True)

# фабрика сессий
async_session = sessionmaker(engine, expire_on_commit=False, class_=AsyncSession)

# фукнция инициализации БД
async def init_db():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)