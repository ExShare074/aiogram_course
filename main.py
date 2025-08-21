from imports import *

bot = Bot(token=TOKEN)
dp = Dispatcher()
translator = Translator()
chatbot = Chatbot(CHATGPT_CONFIG)

try:
    chatbot = Chatbot(CHATGPT_CONFIG)
    print("Chatbot инициализирован успешно.")
except Exception as e:
    print(f"Ошибка инициализации ChatGPT: {str(e)}")
    raise

class ChatGPTStates(StatesGroup):
    waiting_for_query = State()

@dp.message(lambda message: message.text == "🤖 Помощник")
async def assistant_btn(message: types.Message, state: FSMContext):
    await message.answer("Напиши вопрос для ChatGPT:")
    await state.set_state(ChatGPTStates.waiting_for_query)

@dp.message(ChatGPTStates.waiting_for_query)
async def handle_query(message: types.Message, state: FSMContext):
    prompt = message.text
    try:
        response = ""
        for data in chatbot.ask(prompt):
            response += data["message"]
        await message.answer(response or "ChatGPT не вернул ответа.")
    except Exception as e:
        await message.answer(f"Ошибка при обращении к ChatGPT: {str(e)}")
    finally:
        await state.clear()

@dp.callback_query(F.data == 'video')
async def Video(callback: CallbackQuery):
    await callback.answer('Видео подгружается...', show_alert=True)
    await callback.message.edit_text('Тут профиль с видосом!', reply_markup=await kb.test_keyboard())


# ------------------------------
@dp.message(CommandStart())
async def start(message: Message):
    await message.answer(
        f'Привет, {message.from_user.first_name}! Выбери действие:',
        reply_markup=kb.main
    )

# ---------- КРИПТА ----------
@dp.message(F.text == "💰 Крипта")
async def crypto_btn(message: Message):
    await message.answer("Выберите валюту:", reply_markup=inline_coins)

# --- Функция запроса цены ---
async def fetch_coin(coin_id: str):
    url = f"https://api.coingecko.com/api/v3/coins/{coin_id}"
    async with aiohttp.ClientSession() as session:
        async with session.get(url) as response:
            if response.status == 200:
                data = await response.json()
                market_data = data.get("market_data", {})
                return {
                    "price": market_data.get("current_price", {}).get("usd", 0),
                    "change": market_data.get("price_change_percentage_24h", 0)
                }
    return None

@dp.callback_query(lambda c: c.data.startswith("coin_"))
async def coin_callback(query: CallbackQuery):
    coin_id = query.data.split("_", 1)[1]
    coin = await fetch_coin(coin_id)
    ticker = COINS.get(coin_id, coin_id)
    if coin:
        text = f"📊 {ticker}-USD\n💰 Цена: {coin['price']:.2f} USD\n📈 Изм. за 24ч: {coin['change']:.2f}%"
    else:
        text = f"⚠️ Не удалось получить данные по {ticker}"

    await query.message.answer(text)
    await query.answer()

# ---------- ПОГОДА ----------
@dp.message(F.text == "🌤 Погода")
async def weather_btn(message: Message):
    await message.answer("Выберите период:", reply_markup=weather_inline)

@dp.callback_query(F.data == "weather_tomorrow")
async def weather_tomorrow(callback):
    await callback.message.edit_text("☀ Завтра: солнечно +25°C")

@dp.callback_query(F.data == "weather_week")
async def weather_week(callback):
    await callback.message.edit_text("Прогноз на 5 дней: ☀🌧☁🌤🌧")

# ---------- ТРЕНИРОВКА ----------
@dp.message(F.text == "🏋️‍♂️ Тренировка")
async def training_btn(message: Message):
    await message.answer("Выбери тренировку:", reply_markup=training_inline)

@dp.callback_query(F.data.startswith("train_"))
async def training_choice(callback):
    trainings = {
    "train_1": "🏋️‍♂️ Понедельник — Грудь + Спина\n1. Жим штанги лёжа — 4×6–8\n2. Жим гантелей под углом — 3×8–10\n3. Тяга штанги в наклоне — 4×6–8\n4. Подтягивания — 3×макс\n5. Пуловер — 3×12",
    "train_2": "🏋️‍♂️ Среда — Ноги\n1. Приседания — 4×6–8\n2. Жим ногами — 3×10\n3. Выпады — 3×10\n4. Румынская тяга — 3×8–10\n5. Подъём на носки — 4×15–20",
    "train_3": "🏋️‍♂️ Пятница — Плечи + Руки\n1. Жим стоя — 4×6–8\n2. Разведения гантелей — 3×12\n3. Шраги — 3×12\n4. Сгибания штанги — 4×8\n5. Французский жим — 4×8\n6. Молотки — 3×10"
    }
    text = trainings.get(callback.data, "Нет такой тренировки 😢")
    await callback.message.edit_text(text)


@dp.message(F.text == "🎥 Видео")
async def video_btn(message: Message):
    video = FSInputFile('video.mp4')
    await bot.send_video(message.chat.id, video)

@dp.message(F.text == "📄 Документ")
async def doc_btn(message: Message):
    doc = FSInputFile('training.pdf')
    await bot.send_document(message.chat.id, doc)

@dp.message(F.text == "🎙 Голос")
async def voice_btn(message: Message):
    tts = gTTS(text="Привет! Я голосовой помощник.", lang='ru')
    tts.save("voice.ogg")
    voice = FSInputFile("voice.ogg")
    await bot.send_audio(message.chat.id, voice)
    os.remove("voice.ogg")

from googletrans import Translator

@dp.message(F.text == "🔢 Факт о числе")
async def numfact_btn(message: Message):
    async with aiohttp.ClientSession() as session:
        async with session.get("http://numbersapi.com/random/trivia") as response:
            if response.status == 200:
                fact_en = await response.text()
                translator = Translator()
                fact_ru = translator.translate(fact_en, dest='ru').text
                await message.answer(f"🔢 Интересный факт:\n{fact_ru}")
            else:
                await message.answer("Не удалось получить факт 😢")





@dp.message(F.text == "📜 Цитата")
async def quote_btn(message: Message):
    async with aiohttp.ClientSession() as session:
        async with session.get("https://api.forismatic.com/api/1.0/?method=getQuote&format=json&lang=ru") as response:
            if response.status == 200:
                data = await response.json()
                quote = data['quoteText']
                author = data['quoteAuthor'] if data['quoteAuthor'] else "Неизвестный автор"
                await message.answer(f"📜 Цитата дня:\n\n«{quote}»\n— {author}")
            else:
                await message.answer("⚠️ Не удалось получить цитату.")



@dp.message(F.text == "😂 Шутка")
async def joke_btn(message: Message):
    async with aiohttp.ClientSession() as session:
        async with session.get("https://anekdotme.ru/random") as response:
            if response.status == 200:
                html = await response.text()
                # маленький парсинг (так как API в HTML)
                import re
                jokes = re.findall(r'<div class="anekdot_text">(.*?)</div>', html, re.S)
                if jokes:
                    joke = jokes[0].strip()
                    await message.answer(f"😂 Шутка дня:\n\n{joke}")
                else:
                    await message.answer("Не удалось найти шутку 😢")
            else:
                await message.answer("Не удалось получить шутку 😢")



@dp.message(F.text == "📷 Фото")
async def photo_btn(message: Message):
    photos = [
        'https://shmpmgu.ru/wp-content/uploads/2023/03/6-foto-iskusstvennyj-intellekt-i-devushka-930x620.png',
        'https://cdn.lifehacker.ru/wp-content/uploads/2023/02/11111_1676301611.jpg',
        'https://i.ytimg.com/vi/oQu9Ewb0cIQ/maxresdefault.jpg',
        'https://cloud.emcr.io/files/telegram/media/5918196181060667181/5918196181060667181_y_4.jpg'
    ]
    await message.answer_photo(random.choice(photos))

@dp.message(F.text == "🌐 Перевести текст")
async def translate_btn(message: Message):
    await message.answer("Напиши команду `/translate текст`, чтобы перевести его.")

@dp.message(Command("translate"))
async def translate_cmd(message: Message):
    text_to_translate = message.text.replace("/translate", "").strip()
    if not text_to_translate:
        await message.answer("Введите текст после команды. Пример:\n/translate Привет")
        return
    loop = asyncio.get_event_loop()
    detected = await loop.run_in_executor(None, lambda: translator.detect(text_to_translate))
    if detected.lang == 'en':
        translated = await loop.run_in_executor(None, lambda: translator.translate(text_to_translate, dest='ru'))
    else:
        translated = await loop.run_in_executor(None, lambda: translator.translate(text_to_translate, dest='en'))
    await message.answer(f"🗣 Перевод:\n{translated.text}")

# ------------------------------
async def main():
    await bot.delete_webhook()
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
