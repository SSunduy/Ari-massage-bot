from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from database import get_available_slots
from datetime import datetime

def get_main_keyboard():
    kb = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="📅 Записаться", callback_data="book")],
        [InlineKeyboardButton(text="👀 Посмотреть записи", callback_data="view")]
    ])
    return kb

def get_time_keyboard(date=None):
    if date is None:
        date = datetime.now().strftime("%Y-%m-%d")
    slots = get_available_slots(date)
    buttons = [InlineKeyboardButton(text=slot, callback_data=f"time_{slot}_{date}") for slot in slots]
    kb = InlineKeyboardMarkup(inline_keyboard=[[btn] for btn in buttons])
    return kb