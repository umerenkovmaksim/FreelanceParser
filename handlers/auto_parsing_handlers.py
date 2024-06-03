import asyncio

from aiogram import types, md, Router, F
from aiogram.fsm.state import State, StatesGroup
from aiogram.fsm.context import FSMContext
from aiogram.enums import ParseMode

from database import get_user_settings, set_user_settings, set_user_last_task, get_user_last_tasks
from keyboards import *
from bot import *
from Freelances.habrParser import habr_parser
from Freelances.freelanceParser import freelance_parser
from Freelances.kworkParser import kwork_parser

router = Router()

last_task_habr=None

@router.message(F.text.lower() == 'автоматический парсинг')
async def auto_parse_menu(message: types.Message):
    await message.answer(
        text='Выберите для каких сервисов вы хотите включить автоматический парсинг',
        reply_markup=await auto_parse_menu_keyboard(message.from_user.id),
    )


@router.callback_query(F.data == 'auto_habr')
async def habr_parser_automode(callback_query: types.CallbackQuery):
    await callback_query.message.delete()
    user_settings = await get_user_settings(callback_query.from_user.id)
    if not user_settings['auto_habr']:
        await set_user_settings(callback_query.from_user.id, auto_habr=True)
        parsed_task_habr = asyncio.create_task(parse_and_process_habr(callback_query.from_user.id))
        await callback_query.message.answer(
            text='Автоматический парсинг <b>Freelance Habr</b> был запущен',
            reply_markup=await auto_parse_menu_keyboard(callback_query.from_user.id),
            parse_mode=ParseMode.HTML,
        )
    else:
        await set_user_settings(callback_query.from_user.id, auto_habr=False)
        await callback_query.message.answer(
            text='Автоматический парсинг <b>Freelance Habr</b> был остановлен',
            reply_markup=await auto_parse_menu_keyboard(callback_query.from_user.id),
            parse_mode=ParseMode.HTML,
        )


async def parse_and_process_habr(user_id):
    while True:
        user_settings = await get_user_settings(user_id)
        if not user_settings['auto_habr']:
            break
        tasks = await habr_parser(tasks_count=1)
        task = tasks[0]

        task_text = f'{task["title"]} ({task["url"]})\nОткликов: {task["resp_count"]}, Время: {task["time_ago"]}'
        last_tasks = await get_user_last_tasks(user_id)
        if last_tasks is None or last_tasks['last_habr'] != task['title']:
            await set_user_last_task(user_id, last_habr=task['title'])
            await bot.send_message(
                chat_id=user_id,
                text=task_text,
            )

        await asyncio.sleep(30)


@router.callback_query(F.data == 'auto_freelance')
async def freelance_parser_automode(callback_query: types.CallbackQuery):
    await callback_query.message.delete()
    user_settings = await get_user_settings(callback_query.from_user.id)
    if not user_settings['auto_freelance']:
        await set_user_settings(callback_query.from_user.id, auto_freelance=True)
        asyncio.create_task(parse_and_process_freelance(callback_query.from_user.id))
        await callback_query.message.answer(
            text='Автоматический парсинг <b>Freelance</b> был запущен',
            reply_markup=await auto_parse_menu_keyboard(callback_query.from_user.id),
            parse_mode=ParseMode.HTML,
        )
    else:
        await set_user_settings(callback_query.from_user.id, auto_freelance=False)
        await callback_query.message.answer(
            text='Автоматический парсинг <b>Freelance</b> был остановлен',
            reply_markup=await auto_parse_menu_keyboard(callback_query.from_user.id),
            parse_mode=ParseMode.HTML,
        )


async def parse_and_process_freelance(user_id):
    while True:
        user_settings = await get_user_settings(user_id)
        if not user_settings['auto_freelance']:
            break
        tasks = await freelance_parser(tasks_count=1)
        task = tasks[0]

        task_text = f'{task["title"]} ({task["url"]})\nОткликов: {task["resp_count"]}, Время: {task["time_ago"]}'
        last_tasks = await get_user_last_tasks(user_id)
        if last_tasks is None or last_tasks['last_freelance'] != task['title']:
            await set_user_last_task(user_id, last_freelance=task['title'])
            await bot.send_message(
                chat_id=user_id,
                text=task_text,
            )

        await asyncio.sleep(30)
            

@router.callback_query(F.data == 'auto_kwork')
async def kwork_parser_automode(callback_query: types.CallbackQuery):
    await callback_query.message.delete()
    user_settings = await get_user_settings(callback_query.from_user.id)
    if not user_settings['auto_kwork']:
        await set_user_settings(callback_query.from_user.id, auto_kwork=True)
        asyncio.create_task(parse_and_process_kwork(callback_query.from_user.id))
        await callback_query.message.answer(
            text='Автоматический парсинг <b>Kwork</b> был запущен',
            reply_markup=await auto_parse_menu_keyboard(callback_query.from_user.id),
            parse_mode=ParseMode.HTML,
        )
    else:
        await set_user_settings(callback_query.from_user.id, auto_kwork=False)
        await callback_query.message.answer(
            text='Автоматический парсинг <b>Kwork</b> был остановлен',
            reply_markup=await auto_parse_menu_keyboard(callback_query.from_user.id),
            parse_mode=ParseMode.HTML,
        )


async def parse_and_process_kwork(user_id):
    global last_task_habr
    while True:
        user_settings = await get_user_settings(user_id)
        if not user_settings['auto_kwork']:
            break
        tasks = await kwork_parser(tasks_count=1)
        task = tasks[0]

        task_text = f'{task["title"]}\n{task["url"]}\nОткликов: {task["resp_count"]}'
        last_tasks = await get_user_last_tasks(user_id)
        if last_tasks is None or last_tasks['last_kwork'] != task['title']:
            await set_user_last_task(user_id, last_kwork=task['title'])
            await bot.send_message(id)
            await bot.send_message(
                chat_id=user_id,
                text=task_text,
            )

        await asyncio.sleep(30)