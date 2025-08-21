import asyncio
from aiogram import Bot, Dispatcher, types
from aiogram.filters import Command
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton, CallbackQuery
import aiohttp

from config import TOKEN

bot = Bot(token=TOKEN)
dp = Dispatcher()

# --- Список монет: {id CoinGecko: тикер} ---
COINS = {
    "bitcoin": "BTC",
    "ethereum": "ETH",
    "dogecoin": "DOGE",
    "binancecoin": "BNB",
    "solana": "SOL",
    "ripple": "XRP",
    "cardano": "ADA",
    "polkadot": "DOT",
    "tron": "TRX",
    "litecoin": "LTC"
}

# --- Inline кнопки для монет ---
inline_coins = InlineKeyboardMarkup(
    inline_keyboard=[
        [InlineKeyboardButton(text=ticker, callback_data=f"coin_{coin_id}")]
        for coin_id, ticker in COINS.items()
    ]
)

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

# --- Команда /start ---
@dp.message(Command("start"))
async def start(message: types.Message):
    await message.answer(
        "Привет! Выберите криптовалюту, чтобы узнать её актуальный курс 💰",
        reply_markup=inline_coins
    )

# --- Обработчик inline кнопок ---
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
    await query.answer()  # закрывает «часики» на кнопке



# --- Запуск бота ---
async def main():
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
