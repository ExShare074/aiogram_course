import asyncio
from aiogram.types import Message, FSInputFile, InlineKeyboardMarkup, InlineKeyboardButton, CallbackQuery
from aiogram import Bot, Dispatcher, F
from aiogram.filters import CommandStart, Command
from aiogram.utils.keyboard import ReplyKeyboardBuilder

from config import TOKEN
import random
import aiohttp
from datetime import datetime
import os
from gtts import gTTS
from googletrans import Translator
import keyboards as kb
from keyboards import weather_inline, training_inline

bot = Bot(token=TOKEN)
dp = Dispatcher()

#Задание 1: Создание простого меню с кнопками
#При отправке команды /start бот будет показывать меню с кнопками "Привет" и "Пока". При нажатии на кнопку "Привет" бот должен
# отвечать "Привет, {имя пользователя}!", а при нажатии на кнопку "Пока" бот должен отвечать "До свидания, {имя пользователя}!".

@dp.message(Command("start"))
async def start(message: Message):
    builder = ReplyKeyboardBuilder()
    builder.button(text="Привет")
    builder.button(text="Пока")
    builder.adjust(2)  # две кнопки в одном ряду
    await message.answer(
        "Выбери кнопку:",
        reply_markup=builder.as_markup(resize_keyboard=True)
    )


@dp.message(Command("links"))
async def links(message: Message):
    await message.answer("🔗 Ссылки:", reply_markup=kb.inline_hw)


@dp.message(F.text.in_(["Привет", "Пока"]))
async def handle_buttons(message: Message):
    if message.text == "Привет":
        await message.answer(f"Привет, {message.from_user.full_name}!")
    elif message.text == "Пока":
        await message.answer(f"До свидания, {message.from_user.full_name}!")


# Кнопка "Показать больше"
show_more_kb = InlineKeyboardMarkup(
    inline_keyboard=[
        [InlineKeyboardButton(text="Показать больше", callback_data="dynamic")]
    ]
)

# Две кнопки "Опция 1" и "Опция 2"
options_kb = InlineKeyboardMarkup(
    inline_keyboard=[
        [InlineKeyboardButton(text="Опция 1", callback_data="option_1")],
        [InlineKeyboardButton(text="Опция 2", callback_data="option_2")]
    ]
)

# Хендлер команды /dynamic
@dp.message(Command("dynamic"))
async def cmd_dynamic(message: Message):
    await message.answer("Нажми кнопку ниже:", reply_markup=show_more_kb)

# Хендлер для кнопки "Показать больше"
@dp.callback_query(F.data == "dynamic")
async def show_options(callback: CallbackQuery):
    await callback.message.edit_text("Выбери опцию:", reply_markup=options_kb)

# Хендлеры для опций
@dp.callback_query(F.data.in_(["option_1", "option_2"]))
async def option_selected(callback: CallbackQuery):
    if callback.data == "option_1":
        await callback.message.answer("Ты выбрал: Опция 1")
    elif callback.data == "option_2":
        await callback.message.answer("Ты выбрал: Опция 2")
    await callback.answer()  # убирает "часики" на кнопке




async def main():
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
