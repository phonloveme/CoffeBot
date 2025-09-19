from sqlalchemy.future import select
from sqlalchemy.ext.asyncio import AsyncSession
from bot.database.models import Location

# Добавить новую точку
async def add_location(session: AsyncSession, name: str):
    normalized_name = name.strip().lower()
    location = Location(name=normalized_name)
    session.add(location)
    await session.commit()
    await session.refresh(location)
    return location


#Получить все локации
async def get_all_locations(session: AsyncSession):
    result = await session.execute(select(Location))
    return result.scalars().all()

# Найти локацию по имени
async def get_location_by_name(session: AsyncSession, name: str):
    normalized_name = name.strip().lower()
    result = await session.execute(select(Location).where(Location.name == normalized_name))
    return result.scalar_one_or_none()



