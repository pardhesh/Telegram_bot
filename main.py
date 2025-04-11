import asyncio
import os
import google.generativeai as genai
from aiogram import Bot, Dispatcher, types
from aiogram.filters import Command
from aiogram.enums import ParseMode
from aiogram.fsm.storage.memory import MemoryStorage
from aiogram.fsm.state import State, StatesGroup
from aiogram.fsm.context import FSMContext
from aiogram.client.default import DefaultBotProperties
from dotenv import load_dotenv

load_dotenv()
TELEGRAM_BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")

# Gemini
genai.configure(api_key=GEMINI_API_KEY)
model = genai.GenerativeModel("gemini-2.0-flash")

bot = Bot(
    token=TELEGRAM_BOT_TOKEN,
    default=DefaultBotProperties(parse_mode=ParseMode.HTML)
)
dp = Dispatcher(storage=MemoryStorage())

class ChatState(StatesGroup):
    chatting = State()

@dp.message(Command("/start"))
async def start_handler(message: types.Message, state: FSMContext):
    await message.answer("Hi! I’m your Gemini-powered AI Assistant.\nAsk me anything!")

@dp.message(Command("/about"))
async def about_handler(message: types.Message):
    await message.answer("I'm an AI bot using Google Gemini + Aiogram 3.0.\nBuilt by Pardhesh.")
    
    
@dp.message(Command("/clear"))
async def clear_handler(message: types.Message, state: FSMContext):
    await state.clear()
    await message.answer("Memory cleared!")

@dp.message()
async def chat_handler(message: types.Message, state: FSMContext):
    try:
        prompt = message.text
        response = model.generate_content(prompt)
        reply = response.text.strip()
        await message.answer(reply)
    except Exception as e:
        await message.answer(f"⚠️ Error: {e}")

async def main():
    await dp.start_polling(bot, skip_updates=True)

if __name__ == "__main__":
    asyncio.run(main())
