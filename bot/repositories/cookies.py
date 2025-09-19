from pydantic.v1.schema import normalize_name
from sqlalchemy.future import select
from sqlalchemy.ext.asyncio import AsyncSession
from bot.database.models import CookieType, CookieStorage, Location

# Добавить новый вид печенья
async def add_cookie_type(session: AsyncSession, name: str):
    normalized_name = name.strip().lower()
    cookie = CookieType(name=normalized_name)
    session.add(cookie)
    await session.commit()
    await session.refresh(cookie)
    return cookie

# получить все типы печенья
async def get_all_cookie(session: AsyncSession):
    result = await session.execute(select(CookieType))
    return result.scalars().all()

#добавить количество печенья на точке
async def add_cookie_to_storage(session: AsyncSession, location_id: int, cookie_id: int, quantity: int):
    storage = CookieStorage(
        location_id = location_id,
        cookie_id = cookie_id,
        quantity = quantity,
    )
    session.add(storage)
    await session.commit()
    await session.refresh(storage)
    return storage


#получить запасы печенья на точке
async def get_cookie_by_location(session: AsyncSession, location_id: int):
    result = await session.execute(select(CookieStorage).where(CookieStorage.location_id == location_id))
    return result.scalars().all()

## Обновить или создать запасы печенья на точке
async def update_cookie_storage(session: AsyncSession, location_id: int, cookie_id: int, quantity: int):
    result = await session.execute(
        select(CookieStorage).where(
            CookieStorage.location_id == location_id,
            CookieStorage.cookie_id == cookie_id,
        )
    )
    storage = result.scalar_one_or_none()

    if storage:  # если запись уже есть - обновляем
        storage.quantity = quantity
    else:  # если нет - создаем
        storage = CookieStorage(
            location_id=location_id,
            cookie_id=cookie_id,
            quantity=quantity,
        )
        session.add(storage)

    await session.commit()
    await session.refresh(storage)  # гарантируем актуальные данные
    return storage

#Найти печенье по имени
async def get_cookie_by_name(session: AsyncSession, name: str):
    normalized_name = name.strip().lower()
    result = await session.execute(select(CookieType).where(CookieType.name == normalized_name))
    return result.scalar_one_or_none()





