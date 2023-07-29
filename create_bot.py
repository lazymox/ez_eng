import logging

from aiogram import Bot, types
from aiogram.dispatcher import Dispatcher
from config import TOKEN
from aiogram.contrib.fsm_storage.memory import MemoryStorage

storage = MemoryStorage()
# openai_token = "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"
bot = Bot(token=TOKEN, parse_mode=types.ParseMode.HTML)
dp = Dispatcher(bot, storage=storage)
logging.basicConfig(level=logging.INFO)
