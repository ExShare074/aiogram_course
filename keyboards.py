from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.utils.keyboard import InlineKeyboardBuilder, ReplyKeyboardBuilder

main = ReplyKeyboardMarkup(
    keyboard=[
        [KeyboardButton(text="🌤 Погода")],
        [KeyboardButton(text="🎥 Видео"), KeyboardButton(text="📄 Документ")],
        [KeyboardButton(text="🎙 Голос"), KeyboardButton(text="🔢 Факт о числе")],
        [KeyboardButton(text="📜 Цитата"), KeyboardButton(text="😂 Шутка")],
        [KeyboardButton(text="📷 Фото"), KeyboardButton(text="🏋️‍♂️ Тренировка")],
        [KeyboardButton(text="🌐 Перевести текст")],
    ],
    resize_keyboard=True
)

inline_hw = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text="Видео", url="https://www.youtube.com/shorts/PMnL5kgLwr0")],
    [InlineKeyboardButton(text="Новости", url="https://lenta.ru/rubrics/world/")],
    [InlineKeyboardButton(text="Музыка", url="https://music.yandex.ru/")]
    ])


test = ["кнопка1", "кнопка2", "кнопка3", "кнопка4"]

async def test_keyboard():
    keyboard = InlineKeyboardBuilder()
    for key in test:
        keyboard.add(InlineKeyboardButton(text=key, url = "https://www.youtube.com/shorts/6_u_gcLOyKk"))
    return keyboard.adjust(2).as_markup()


# Inline-кнопки для погоды
weather_inline = InlineKeyboardMarkup(
    inline_keyboard=[
        [InlineKeyboardButton(text="Погода на завтра", callback_data="weather_tomorrow")],
        [InlineKeyboardButton(text="Погода на 5 дней", callback_data="weather_week")],
    ]
)

# Inline-кнопки для тренировок
training_inline = InlineKeyboardMarkup(
    inline_keyboard=[
        [InlineKeyboardButton(text="Понедельник", callback_data="train_1")],
        [InlineKeyboardButton(text="Среда", callback_data="train_2")],
        [InlineKeyboardButton(text="Пятница", callback_data="train_3")],
    ]
)
