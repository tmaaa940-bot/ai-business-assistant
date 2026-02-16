import asyncio
import logging
from aiogram import Bot, Dispatcher, types
from aiogram.filters import Command
from openai import AsyncOpenAI

# Конфигурация (в реальном проекте берется из .env)
API_TOKEN = 'YOUR_TELEGRAM_BOT_TOKEN'
OPENAI_API_KEY = 'YOUR_OPENAI_KEY'

# Инициализация ИИ и Бота
client = AsyncOpenAI(api_key=OPENAI_API_KEY)
bot = Bot(token=API_TOKEN)
dp = Dispatcher()

logging.basicConfig(level=logging.INFO)

@dp.message(Command("start"))
async def cmd_start(message: types.Message):
    await message.answer("Привет! Я AI-ассистент для вашего бизнеса. Чем могу помочь?")

@dp.message()
async def handle_message(message: types.Message):
    """Логика обработки запроса через OpenAI"""
    try:
        response = await client.chat.completions.create(
            model="gpt-4-turbo-preview",
            messages=[
                {"role": "system", "content": "Ты профессиональный бизнес-консультант."},
                {"role": "user", "content": message.text}
            ]
        )
        await message.answer(response.choices[0].message.content)
    except Exception as e:
        logging.error(f"Error: {e}")
        await message.answer("Произошла ошибка при обращении к ИИ.")

async def main():
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
