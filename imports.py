from revChatGPT.V1 import Chatbot
import asyncio
from aiogram.types import Message, FSInputFile, InlineKeyboardMarkup, InlineKeyboardButton, CallbackQuery, ReplyKeyboardMarkup, KeyboardButton
from aiogram import Bot, Dispatcher, F, types
from aiogram.filters import CommandStart, Command
from aiogram.fsm.storage.memory import MemoryStorage
from config import TOKEN, WEATHER_API_KEY, WEATHER_CITY, CHATGPT_CONFIG
import random
import aiohttp
import sqlite3
from datetime import datetime
import requests
import logging
import os
from gtts import gTTS
from googletrans import Translator
import keyboards as kb
from keyboards import weather_inline, training_inline, inline_coins, COINS
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup

