from imports import *

bot = Bot(token=TOKEN)
dp = Dispatcher()

logging.basicConfig(level=logging.INFO)

button_register = KeyboardButton(text="Регистрация")
button_exchange = KeyboardButton(text="Курс валют")
button_tips = KeyboardButton(text="Советы о экономии")
button_finance = KeyboardButton(text="Финансы")

keyboard = ReplyKeyboardMarkup(keyboard=[
    [button_register, button_exchange],
    [button_tips, button_finance]
    ], resize_keyboard=True)

conn = sqlite3.connect('user.db')
cursor = conn.cursor()

cursor.execute('''CREATE TABLE IF NOT EXISTS users (
    id INTEGER PRIMARY KEY,
    telegram_id INTEGER UNIQUE,
    name TEXT,
    category1 TEXT,
    category2 TEXT,
    category3 TEXT,
    expenses1 REAL,
    expenses2 REAL,
    expenses3 REAL
    )''')

conn.commit()

class FinancesForm(StatesGroup):
    category1 = State()
    expenses1 = State()
    category2 = State()
    expenses2 = State()
    category3 = State()
    expenses3 = State()

async def main():
    if __name__ == '__main__':
        await dp.start_polling(bot)


if __name__ == '__main__':
    asyncio.run(main())
