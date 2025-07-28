import asyncio
from aiogram.types import Message, FSInputFile
from config import TOKEN, WEATHER_API_KEY, WEATHER_CITY
from aiogram import Bot, Dispatcher, F
from aiogram.filters import CommandStart, Command
import random
import aiohttp
from datetime import datetime
import os
from gtts import gTTS


bot = Bot(token=TOKEN)
dp = Dispatcher()

@dp.message(Command('weather'))
async def weather(message: Message):
    url = f"http://api.openweathermap.org/data/2.5/weather?q={WEATHER_CITY}&appid={WEATHER_API_KEY}&units=metric&lang=ru"

    async with aiohttp.ClientSession() as session:
        async with session.get(url) as response:
            if response.status == 200:
                data = await response.json()
                temp = data['main']['temp']
                description = data['weather'][0]['description']
                forecast = f"🌤 Погода в {WEATHER_CITY}: {description}, {temp}°C"
            else:
                forecast = "Не удалось получить погоду 😢"
    await message.answer(forecast)

@dp.message(Command('video'))
async def video(message:Message):
    await bot.send_chat_action(message.chat.id, "upload_video")
    video = FSInputFile('video.mp4')
    await bot.send_video(message.chat.id, video)

@dp.message(Command('doc'))
async def doc(message: Message):
    await bot.send_chat_action(message.chat.id, "upload_document")
    doc = FSInputFile('training.pdf')
    await bot.send_document(message.chat.id, doc)

@dp.message(Command('voice'))
async def voice(message: Message):
    await bot.send_chat_action(message.chat.id, "upload_audio")
    voice = FSInputFile('sample.ogg')
    await message.answer_voice(voice)
    os.remove('sample.ogg')

@dp.message(Command('numberfact'))
async def number_fact(message: Message):
    async with aiohttp.ClientSession() as session:
        async with session.get("http://numbersapi.com/random/trivia") as response:
            if response.status ==200:
                fact = await response.text()
                await message.answer(f"{fact}")
            else:
                if response.status == 404:
                    await message.answer("Не удалось получить факты о цифрах 😢")
                else:
                    await message.answer("Неизвестная ошибка 😢")

@dp.message(Command('facts'))
async  def all_facts(message:Message):
    async with aiohttp.ClientSession() as session:
        async with session.get("https://uselessfacts.jsph.pl/api/v2/facts/random?language=en") as response:
            if response.status ==200:
                data = await response.json()
                fact = data['text']
                await message.answer(fact)
            else:
                if response.status == 404:
                    await message.answer("Не удалось получить факты 😢")
                else:
                    await message.answer("Неизвестная ошибка 😢")


@dp.message(Command('quotable'))
async def quotable(message:Message):
    async with aiohttp.ClientSession() as session:
        async with session.get("https://zenquotes.io/api/random") as response:
                if response.status ==200:
                    data = await response.json()
                    quote = data['quote']
                    movie = data['movie']
                    await message.answer(f"🎬 {quote}\n— {movie}")
                else:
                    if response.status == 404:
                        await message.answer("Не удалось получить цитату 😢")
                    else:
                        await message.answer("Неизвестная ошибка 😢")

@dp.message(Command('trivia'))
async def trivia(message: Message):
    async with aiohttp.ClientSession() as session:
        async with session.get("https://opentdb.com/api.php?amount=1&type=multiple") as response:
            if response.status ==200:
                data = await response.json()
                question = data["results"][0]["question"]
                answer = data["results"][0]["correct_answer"]
                await message.answer(f"🧠 Вопрос: {question}\n✅ Ответ: {answer}")
            else:
                await message.answer("Не удалось получить вопрос-викторину 😢")


@dp.message(Command("quote"))
async def send_quote(message: Message):
    async with aiohttp.ClientSession() as session:
        async with session.get("https://zenquotes.io/api/random") as response:
            if response.status == 200:
                data = await response.json()
                quote = data[0]['q']
                author = data[0]['a']
                await message.answer(f"💬 {quote}\n— {author}")
            else:
                await message.answer("⚠️ Не удалось получить цитату.")


@dp.message(Command('joke'))
async def send_joke(message:Message):
    async with aiohttp.ClientSession() as session:
        async with session.get("https://official-joke-api.appspot.com/jokes/random") as response:
            if response ==200:
                data = await response.json()
                joke = f"😂 {data['setup']} \n {data['punchline']}"
            else:
                if response.status == 404:
                    joke = "Не удалось получить шутку 😢"
                else:
                    joke = "Неизвестная ошибка 😢"


@dp.message(Command('meme'))
async def meme(message:Message):
    async with aiohttp.ClientSession() as session:
        async with session.get("https://api.imgflip.com/get_memes") as response:
            if response.status ==200:
                data  = await response.json()
                await message.answer_photo(photo=data['url'], caption=data['title'])
            else:
                if response.status == 404:
                    await message.answer("Не удалось получить мем 😢")
                else:
                    await message.answer("Неизвестная ошибка 😢")


@dp.message(Command('photo', prefix='&'))
async def answ_photo(message: Message):
    list = ['https://shmpmgu.ru/wp-content/uploads/2023/03/6-foto-iskusstvennyj-intellekt-i-devushka-930x620.png',
            'https://cdn.lifehacker.ru/wp-content/uploads/2023/02/11111_1676301611.jpg',
            'https://i.ytimg.com/vi/oQu9Ewb0cIQ/maxresdefault.jpg',
            'https://cloud.emcr.io/files/telegram/media/5918196181060667181/5918196181060667181_y_4.jpg']
    rand_photo = random.choice(list)
    await message.answer_photo(photo=rand_photo, caption='Это фото, сгенерированное супер ИИ')

@dp.message(Command('help'))
async def help(message: Message):
    await message.answer('этот бот умеет выполнять команды:\n /start \n /help \n /photo \n /weather \n /numberfact \n '
                         '/quote \n /meme \n /trivia \n /joke \n /facts \n /quotable \n /video \n /movie \n /training')


@dp.message(Command('movie'))
async def random_movie(message:Message):
    async with aiohttp.ClientSession() as session:
        async with session.get("https://fake-movie-database-api.herokuapp.com/api?s=random") as response:
            if response ==200:
                data = await response.json()
                movie = random.choice(data['series'])
                title = data['title']
                year = data['year']
                poster = data['poster']

                await message.answer_photo(photo=poster, caption=f"🎬 {title} ({year})")
            else:
                if response.status == 404:
                    await message.answer("Не удалось получить фильм 😢")
                else:
                    await message.answer("Неизвестная ошибка 😢")


@dp.message(F.photo)
async def react_photo(message: Message):
    list = ['классная фотка', 'фото так себе', 'не отправляй больше такое фото']
    rand_answer = random.choice(list)
    await message.answer(rand_answer)
    os.makedirs('tmp', exist_ok=True)
    file_path = f'tmp/{message.photo[-1].file_id}.jpg'
    await bot.download(message.photo[-1], destination=file_path)


@dp.message(F.text == 'Что такое ИИ?')
async def ai_text(message: Message):
    await message.answer('Это искусственный интеллект. Это компьютерная программа, которая способна обучаться и выполнять задачи, '
                         'не имея никакого вмешательства человека.')


from aiogram.types import FSInputFile
from gtts import gTTS
import os
import random

@dp.message(Command("training"))
async def training(message: Message):
    weekday = datetime.now().weekday()

    if weekday in (0, 1):
        training_num = 1
    elif weekday in (2, 3):
        training_num = 2
    elif weekday in (4, 5):
        training_num = 3
    else:
        await message.answer("Сегодня воскресенье — день отдыха 🧘‍♂️")
        return

    trainings = {
        1: "🏋️‍♂️ Тренировка 1 (Грудь + Спина):\n"
           "1. Жим штанги лёжа – 4×6–8\n"
           "2. Жим гантелей под углом – 3×8–10\n"
           "3. Тяга штанги в наклоне – 4×6–8\n"
           "4. Подтягивания – 3×макс\n"
           "5. Пуловер – 3×12",

        2: "🏋️‍♂️ Тренировка 2 (Ноги):\n"
           "1. Приседания – 4×6–8\n"
           "2. Жим ногами – 3×10\n"
           "3. Выпады с гантелями – 3×10\n"
           "4. Румынская тяга – 3×8–10\n"
           "5. Подъём на носки – 4×15–20",

        3: "🏋️‍♂️ Тренировка 3 (Плечи + Руки):\n"
           "1. Жим гантелей или штанги вверх – 4×6–8\n"
           "2. Разведения гантелей в стороны – 3×12\n"
           "3. Шраги – 3×12\n"
           "4. Сгибания штанги на бицепс – 4×8\n"
           "5. Французский жим – 4×8\n"
           "6. Молотки – 3×10",
    }

    selected_training = trainings[training_num]
    await message.answer(f"📅 Сегодня: {datetime.now().strftime('%A, %d %B')}\n\n{selected_training}")


    plain_text = selected_training.replace("×", " по ").replace("–", " — ").replace("макс", "максимум")
    tts = gTTS(text=plain_text, lang='ru')
    tts.save("training.ogg")

    audio = FSInputFile("training.ogg")
    await bot.send_voice(message.chat.id, audio)
    os.remove("training.ogg")


@dp.message(CommandStart())
async def start(message: Message):
    await message.answer(f'Привет, {message.from_user.first_name}')

@dp.message()
async def start(message:Message):
    if message.text.lower() == 'тест':
        await message.answer('тестируем')

async def main():
    await dp.start_polling(bot)

if __name__ == '__main__':
    asyncio.run(main())