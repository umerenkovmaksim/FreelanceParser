from aiogram import types, md, Router, F
from aiogram.fsm.state import State, StatesGroup
from aiogram.fsm.context import FSMContext
from aiogram.enums import ParseMode

from keyboards import *
from Freelances.habrParser import habr_parser
from Freelances.freelanceParser import freelance_parser
from Freelances.kworkParser import kwork_parser


router = Router()


class HabrCount(StatesGroup):
    count = State()

class FreelanceCount(StatesGroup):
    count = State()

class KworkCount(StatesGroup):
    count = State()


@router.message(F.text.lower() == 'одиночный парсинг')
async def single_parse_menu(message: types.Message):
    await message.answer(
        'Выберите с какого сервиса вы хотите запарсить заказы',
        reply_markup=single_parse_keyboard.as_markup(),
    )

@router.callback_query(F.data == 'single_parse_habr')
async def process_habr_parse_request(callback_query: types.CallbackQuery, state: FSMContext):
    await callback_query.message.delete()
    await callback_query.message.answer('Сколько заказов хотите запарсить?')
    await state.set_state(HabrCount.count)


@router.callback_query(F.data == 'single_parse_freelance')
async def process_freelance_parse_request(callback_query: types.CallbackQuery, state: FSMContext):
    await callback_query.message.delete()
    await callback_query.message.answer('Сколько заказов хотите запарсить?')
    await state.set_state(FreelanceCount.count)

@router.callback_query(F.data == 'single_parse_kwork')
async def process_kwork_parse(callback_query: types.CallbackQuery, state: FSMContext):
    await callback_query.message.delete()
    await callback_query.message.answer('Сколько заказов хотите запарсить?')
    await state.set_state(KworkCount.count)

@router.message(HabrCount.count)
async def process_habr_parse_count(message: types.Message, state: FSMContext):
    try:
        count = int(message.text)
        if count <= 0:
            raise ValueError()
    except ValueError:
        await message.reply('Количество заказов должно быть положительным числом!')
        return

    tasks = await habr_parser(tasks_count=count)

    for task in tasks:
        task_text = f'{task["title"]} ({task["url"]})\nОткликов: {task["resp_count"]}, Время: {task["time_ago"]}'
        await message.answer(
            task_text,
            parse_mode=ParseMode.HTML,
        )

    await message.reply(f'Найдено {len(tasks)} заказов!', reply_markup=single_parse_keyboard.as_markup())
    await state.clear()

@router.message(FreelanceCount.count)
async def process_freelance_parse_count(message: types.Message, state: FSMContext):
    try:
        count = int(message.text)
        if count <= 0:
            raise ValueError()
    except ValueError:
        await message.reply('Количество заказов должно быть положительным числом!')
        return

    tasks = await freelance_parser(tasks_count=count)

    for task in tasks:
        task_text = f'{task["title"]} \n({task["url"]})\nОткликов: {task["resp_count"]}, Время: {task["time_ago"]}'
        await message.answer(task_text)

    await message.reply(f'Найдено {len(tasks)} заказов!', reply_markup=single_parse_keyboard.as_markup())
    await state.clear()


@router.message(KworkCount.count)
async def process_kwork_parse_count(message: types.Message, state: FSMContext):
    try:
        count = int(message.text)
        if count <= 0:
            raise ValueError()
    except ValueError:
        await message.reply('Количество заказов должно быть положительным числом!')
        return

    tasks = kwork_parser(tasks_count=count)

    for task in tasks:
        task_text = f'{task["title"]}\n{task["url"]}\nОткликов: {task["resp_count"]}'
        await message.answer(task_text)

    await message.reply(f'Найдено {len(tasks)} заказов!', reply_markup=single_parse_keyboard.as_markup())
    await state.clear()
