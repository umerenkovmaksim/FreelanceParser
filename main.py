import asyncio
import aiogram.utils.markdown as md
from aiogram import Bot, Dispatcher, types
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.dispatcher import filters, FSMContext
from aiogram.dispatcher.filters.state import StatesGroup, State
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton
from aiogram.types.message import ContentTypes

from Freelances.habrParser import *
from config import bot_token


class Form(StatesGroup):
    count = State()


bot = Bot(token=bot_token)
dp = Dispatcher(bot, storage=MemoryStorage())


@dp.message_handler(commands=['start'])
async def send_welcome(message: types.Message):
    markup = ReplyKeyboardMarkup(resize_keyboard=True)
    markup.add(KeyboardButton('Спарсить заказы'))

    await message.answer(
        md.text(
            md.text('Привет! Я бот для парсинга заказов.'),
            md.text('Нажмите кнопку ниже, чтобы начать парсинг.')
        ),
        reply_markup=markup
    )


@dp.message_handler(filters.Text(equals='Спарсить заказы'))
async def process_parse_request(message: types.Message):
    await message.reply('Сколько заказов вы хотите спарсить?')
    await Form.count.set()


@dp.message_handler(state=Form.count)
async def process_parse_count(message: types.Message, state: FSMContext):
    try:
        count = int(message.text)
        if count <= 0:
            raise ValueError()
    except ValueError:
        await message.reply('Количество заказов должно быть положительным числом!')
        return

    tasks = await habr_parser(tasks_count=count)

    for task in tasks:
        task_text = md.text(
            md.text(f'{task["title"]} ({task["url"]})'),
            md.text(f'Откликов: {task["resp_count"]}, Время: {task["time_ago"]}')
        )
        await message.answer(task_text)

    await message.reply(f'Найдено {len(tasks)} заказов!')
    await state.finish()


if __name__ == '__main__':
    asyncio.run(dp.start_polling())
