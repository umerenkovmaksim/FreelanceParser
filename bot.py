import logging
from aiogram import Bot, Dispatcher

from config import bot_token


logging.basicConfig(level=logging.INFO)
bot = Bot(token=bot_token)
dp = Dispatcher()