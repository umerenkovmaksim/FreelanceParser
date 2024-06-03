import asyncio
import logging
import sqlite3
from aiogram import Bot, Dispatcher, types, F
from aiogram.enums import ParseMode
from aiogram.filters import Command

from bot import *
from config import bot_token, database
from database import init_db, get_user, add_user, get_active_automode_users
from keyboards import *
from handlers import single_parsing_handlers, auto_parsing_handlers


logging.basicConfig(level=logging.INFO)
bot = Bot(token=bot_token)
dp = Dispatcher()

conn = sqlite3.connect(database)
cursor = conn.cursor()

dp.include_routers(single_parsing_handlers.router, auto_parsing_handlers.router)

@dp.message(Command('start'))
async def start(message: types.Message):
    if await get_user(message.from_user.id):
        message.answer("")
        await message.answer(
            f'С возвращением, [{message.from_user.first_name}](tg://user?id={str(message.from_user.id)}).\nЧто вас привело сюда сегодня?',
            reply_markup=main_menu_keyboard.as_markup(resize_keyboard=True),
            parse_mode=ParseMode.MARKDOWN,
        )
    else:
        await message.answer(
            f'Привет, [{message.from_user.first_name}](tg://user?id={str(message.from_user.id)})!\n'
            'Я бот для парсинга большинства популярных фриланс бирж.\n'
            'Если вы используете его впервые, то советуем пройти небольшое обучение, в котором мы подключим одну из доступных бирж\n\n'
            '**Пройти обучение?**\n\n'
            'P.S. Вы всегда сможете настроить биржи или подключить новые в разделе "Настройки"',
            reply_markup=educate_ask_keyboard.as_markup(),
            parse_mode=ParseMode.MARKDOWN,
        )
        await add_user(message.from_user.id)


@dp.callback_query(F.data == 'educate_accept')
async def education_accept(callback_query=types.CallbackQuery):
    await callback_query.message.answer("Accept")
    

@dp.callback_query(F.data == 'educate_denied')
async def education_accept(callback_query=types.CallbackQuery):
    await callback_query.message.answer("Denied")

async def main():
    active_automode_users = cursor.execute('''SELECT * FROM users WHERE auto_habr = TRUE OR auto_freelance = TRUE OR auto_kwork = TRUE''')
    for user in active_automode_users.fetchall():
        if user[1]:
            asyncio.create_task(auto_parsing_handlers.parse_and_process_habr(user[0]))
        if user[2]:
            asyncio.create_task(auto_parsing_handlers.parse_and_process_freelance(user[0]))
        if user[3]:
            asyncio.create_task(auto_parsing_handlers.parse_and_process_kwork(user[0]))

    await dp.start_polling(bot)

if __name__ == '__main__':
    loop = asyncio.get_event_loop()
    loop.run_until_complete(init_db())

    asyncio.run(main())




