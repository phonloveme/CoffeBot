import asyncio
from aiogram import Bot, Dispatcher, types
from aiogram.filters import Command
from bot.config import settings
from bot.database.db import init_db

#экземляры
bot = Bot(token=settings.BOT_TOKEN)
dp = Dispatcher()

#простой обработчик команд
@dp.message(Command('start'))
async def cmd_start(message: types.Message):
    await message.answer('Привет! Я готов к работе!')

#точка входа
async def main():
    print('DB INIT...')
    await init_db()
    print('Bot started...')
    await dp.start_polling(bot)

if __name__ == '__main__':
    asyncio.run(main())