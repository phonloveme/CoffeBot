import asyncio
from aiogram import Bot, Dispatcher, types
from aiogram.filters import Command

# === Настройки ===
TOKEN = "8414365680:AAHGWE9Dn0yMzZziETfJzTd9OhFKXt6-ONU"  # 🔑 Замените на токен от BotFather

bot = Bot(token=TOKEN)
dp = Dispatcher()

# === Данные (имитация БД) ===
# Список точек
locations = {
    1: "Екатерининская 59",
    2: "Ленина 7"
}

# Запасы: {location_id: {категория: [(название, количество), ...]}}
stocks = {
    1: {
        "Печенье": [("Овсяное", 20), ("Шоколадное", 15)],
        "Чай": [("Зеленый", 10), ("Черный", 8)],
        "Сиропы": [("Клубничный", 5)]
    },
    2: {
        "Печенье": [("Овсяное", 12)],
        "Чай": [("Черный", 7)],
        "Сиропы": [("Карамельный", 3), ("Ванильный", 4)]
    }
}

# === Хэндлеры ===

@dp.message(Command("start"))
async def start_command(message: types.Message):
    await message.answer(
        "Привет! Я бот учёта запасов.\n"
        "Команды:\n"
        "/stock – показать запасы точки.\n\n"
        "Доступные точки:\n"
        "1. Екатерининская 59\n"
        "2. Ленина 7\n\n"
        "Например: /stock 1"
    )

@dp.message(Command("stock"))
async def stock_command(message: types.Message):
    try:
        location_id = int(message.text.split()[1])
        if location_id not in locations:
            raise ValueError

        location_name = locations[location_id]
        data = stocks.get(location_id, {})

        if not data:
            await message.answer(f"Для точки {location_name} нет данных.")
            return

        # Формируем текст ответа
        result = [f"📍 Запасы точки *{location_name}*:"]
        for category, items in data.items():
            result.append(f"\n**{category}**")
            for name, qty in items:
                result.append(f"- {name}: {qty}")
        await message.answer("\n".join(result), parse_mode="Markdown")

    except (IndexError, ValueError):
        await message.answer(
            "Использование: /stock <ID точки>\nНапример: /stock 1"
        )

# === Точка входа ===
async def main():
    print("Бот запущен...")
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
