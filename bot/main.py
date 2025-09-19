import asyncio
from aiogram import Bot, Dispatcher, types
from aiogram.filters import Command
from bot.config import settings
from bot.database.db import init_db, async_session
from bot.repositories import cookies, locations

# Экземпляры
bot = Bot(token=settings.BOT_TOKEN)
dp = Dispatcher()


# ПРОСТОЙ ОБРАБОТЧИК КОМАНД
@dp.message(Command('start'))
async def cmd_start(message: types.Message):
    await message.answer('👋 Привет! Я готов к работе с запасами!')


# ЛОКАЦИИ
@dp.message(Command('add_location'))
async def cmd_add_location(message: types.Message):
    args = message.text.split(maxsplit=1)
    if len(args) < 2:
        await message.answer('Используй: /add_location <название>')
        return

    name = args[1]
    async with async_session() as session:
        loc = await locations.add_location(session, name)
    await message.answer(f'🏬 Локация добавлена: <b>{loc.name.title()}</b>', parse_mode="HTML")


@dp.message(Command('list_locations'))
async def cmd_list_locations(message: types.Message):
    async with async_session() as session:
        locs = await locations.get_all_locations(session)

    if not locs:
        await message.answer('❌ Локаций пока нет.')
    else:
        text = '📍 Список локаций:\n' + '\n'.join([f'{loc.id}. {loc.name.title()}' for loc in locs])
        await message.answer(text)


# ОБНОВЛЕНИЕ ЗАПАСОВ
@dp.message(Command('set_cookie'))
async def cmd_set_cookie(message: types.Message):
    """
    Использование:
    /set_cookie <локация> <печенье> <количество>
    """
    args = message.text.split(maxsplit=3)
    if len(args) != 4:
        await message.answer('Используй: /set_cookie <локация> <печенье> <количество>')
        return

    loc_name, cookie_name, qty = args[1], args[2], args[3]

    try:
        qty = int(qty)
    except ValueError:
        await message.answer('Количество должно быть числом.')
        return

    async with async_session() as session:
        loc = await locations.get_location_by_name(session, loc_name)
        if not loc:
            await message.answer(f"❌ Локация <b>{loc_name}</b> не найдена. Добавь её через /add_location",
                                 parse_mode="HTML")
            return

        cookie = await cookies.get_cookie_by_name(session, cookie_name)
        if not cookie:
            await message.answer(f"❌ Печенье <b>{cookie_name}</b> не найдено. Добавь его через /add_cookie",
                                 parse_mode="HTML")
            return

        storage = await cookies.update_cookie_storage(session, loc.id, cookie.id, qty)

    await message.answer(
        f"✅ На точке <b>{loc.name.title()}</b> теперь <b>{storage.quantity}</b> шт. печенья "
        f"<b>{cookie.name.title()}</b>.",
        parse_mode="HTML"
    )


# ПЕЧЕНЬЕ
@dp.message(Command('add_cookie'))
async def cmd_add_cookie(message: types.Message):
    args = message.text.split(maxsplit=1)
    if len(args) < 2:
        await message.answer('Используй: /add_cookie <название печенья>')
        return

    cookie_name = args[1]
    async with async_session() as session:
        cookie = await cookies.add_cookie_type(session, cookie_name)

    await message.answer(f'🍪 Печенье добавлено: <b>{cookie.name.title()}</b>', parse_mode="HTML")


@dp.message(Command('list_cookies'))
async def cmd_list_cookies(message: types.Message):
    async with async_session() as session:
        all_cookies = await cookies.get_all_cookie(session)

    if not all_cookies:
        await message.answer('❌ Список печенья пуст.')
    else:
        text = '🍪 Список печенья:\n' + '\n'.join([f'– {c.name.title()}' for c in all_cookies])
        await message.answer(text)


# ТОЧКА ВХОДА
async def main():
    print('DB INIT...')
    await init_db()
    print('Bot started...')
    await dp.start_polling(bot)


if __name__ == '__main__':
    asyncio.run(main())
