from aiogram import Bot, Dispatcher, F
from aiogram.types import Message, CallbackQuery
from aiogram.filters import Command
from aiogram.utils.keyboard import InlineKeyboardBuilder
import asyncio
import logging
from datetime import datetime

from config import BOT_TOKEN, ADMINS
from database import init_db, get_available_slots, book_slot, get_bookings_by_date
from keyboards import get_main_keyboard, get_time_keyboard

logging.basicConfig(level=logging.INFO)

bot = Bot(token=BOT_TOKEN)
dp = Dispatcher()

@dp.message(Command("start"))
async def cmd_start(message: Message):
    await message.answer("Добро пожаловать в Ari_massag_bot!\nВыберите действие:", reply_markup=get_main_keyboard())

@dp.callback_query(F.data == "book")
async def process_book(callback: CallbackQuery):
    today = datetime.now().strftime("%Y-%m-%d")
    kb = get_time_keyboard(today)
    await callback.message.edit_text("Выберите время:", reply_markup=kb)

@dp.callback_query(F.data.startswith("time_"))
async def process_time(callback: CallbackQuery):
    _, time, date = callback.data.split("_")
    user_id = callback.from_user.id
    username = callback.from_user.username or "Без имени"
    book_slot(user_id, username, time, date)
    await callback.message.edit_text(f"Вы записаны на {time} ({date})!")
    await bot.send_message(ADMIN_ID, f"Новая запись: @{username} на {time} ({date})")

@dp.callback_query(F.data == "view")
async def process_view(callback: CallbackQuery):
    today = datetime.now().strftime("%Y-%m-%d")
    bookings = get_bookings_by_date(today)
    if not bookings:
        await callback.message.edit_text("На сегодня ещё нет записей.")
    else:
        text = "📅 Записи на сегодня:\n\n" + "\n".join([f"{name} — {t}" for name, t in bookings])
        await callback.message.edit_text(text)

@dp.message(Command("admin"))
async def cmd_admin(message: Message):
    if message.from_user.id not in ADMINS:
        await message.answer("❌ Доступ запрещён.")
        return
    today = datetime.now().strftime("%Y-%m-%d")
    bookings = get_bookings_by_date(today)
    if not bookings:
        await message.answer("На сегодня нет записей.")
    else:
        text = "🔐 Админка — записи на сегодня:\n\n" + "\n".join([f"{name} — {t}" for name, t in bookings])
        await message.answer(text)

async def main():
    init_db()
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())