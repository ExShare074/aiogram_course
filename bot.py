from imports import *

bot = Bot(token=TOKEN)
dp = Dispatcher()

logging.basicConfig(level=logging.INFO)

button_register = KeyboardButton(text="Регистрация в телеграмм боте")
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

@dp.message(Command('start'))
async def send_start(message: Message):
    await message.answer("Привет! Я твой финансовый помощник. Выбери подходящее действие!", reply_markup=keyboard)

@dp.message(F.text == "Регистрация в телеграмм боте")
async def registration(message: Message):
    telegram_id = message.from_user.id
    name = message.from_user.full_name
    cursor.execute('''SELECT * FROM users WHERE telegram_id = ?''', (telegram_id,))
    user = cursor.fetchone()
    if user:
        await message.answer("Вы уже зарегистрированы!")
    else:
        cursor.execute('''INSERT INTO users (telegram_id, name) VALUES (?, ?)''', (telegram_id, name))
        conn.commit()
        await message.answer(f"Вы успешно зарегистрированы! Ваш id: {telegram_id}.\n")

@dp.message(F.text == "Курс валют")
async def exchange (message: Message):
    url = "https://v6.exchangerate-api.com/v6/e0a1c85b4f6339fc181e9a53/latest/USD"
    try:
        response = requests.get(url)
        data = response.json()
        if response.status_code != 200:
            await message.answer("Ошибка при получении данных. Попробуйте позже.")
            return
        usd_to_rub = data['conversion_rates']['RUB']
        eur_to_usd = data['conversion_rates']['EUR']

        eur_to_rub = usd_to_rub * eur_to_usd

        await message.answer(f"1 USD = {usd_to_rub:.2f} руб.\n"
                            f"1 EUR = {eur_to_usd:.2f} USD\n"
                            f"1 EUR = {eur_to_rub:.2f} руб.")
    except:
        await message.answer("Ошибка при получении данных. Попробуйте позже.")

@dp.message(F.text == "Советы о экономии")
async def tips(message: Message):
    tips = [
        "1. Покупайте только то, что вам действительно нужно.",
        "2. Не покупайте слишком много.",
        "3. Не покупайте вещи, которые не нужны.",
    ]
    tip = random.choice(tips)
    await message.answer(tip)

@dp.message(F.text == "Финансы")
async def finance(message: Message, state: FSMContext):
    await state.set_state(FinancesForm.category1)
    await message.answer("Введите первую категорию расходов:")

@dp.message(FinancesForm.category1)
async def finance(message: Message, state: FSMContext):
    await state.update_data(category1 = message.text)
    await state.set_state(FinancesForm.expenses1)
    await message.answer("Введите расходы для категории 1:")

@dp.message(FinancesForm.expenses1)
async def finance(message: Message, state: FSMContext):
    await state.update_data(expenses1 = float(message.text))
    await state.set_state(FinancesForm.category2)
    await message.answer("Введите вторую категорию расходов:")

@dp.message(FinancesForm.category2)
async def finance(message: Message, state: FSMContext):
    await state.update_data(category2 = message.text)
    await state.set_state(FinancesForm.expenses2)
    await message.answer("Введите расходы для категории 2:")

@dp.message(FinancesForm.expenses2)
async def finance(message: Message, state: FSMContext):
    await state.update_data(expenses2 = float(message.text))
    await state.set_state(FinancesForm.category3)
    await message.answer("Введите третью категорию расходов:")

@dp.message(FinancesForm.category3)
async def finance(message: Message, state: FSMContext):
    await state.update_data(category3 = message.text)
    await state.set_state(FinancesForm.expenses3)
    await message.answer("Введите расходы для категории 3:")

@dp.message(FinancesForm.expenses3)
async def finance(message: Message, state: FSMContext):
    data = await state.get_data()
    telegram_id = message.from_user.id
    cursor.execute('''
    UPDATE users SET category1 = ?, expenses1 = ?, category2 = ?, expenses2 = ?, category3 = ?, expenses3 = ? WHERE telegram_id = ?
    ''', (data['category1'], data['expenses1'], data['category2'], data['expenses2'], data['category3'], float(message.text), telegram_id))
    conn.commit()
    await state.clear()

    await message.answer("Категории и расходы сохранены!")


async def main():
    await dp.start_polling(bot)


if __name__ == '__main__':
    asyncio.run(main())
