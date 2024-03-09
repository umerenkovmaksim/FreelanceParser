import aiogram.utils.markdown as md
from aiogram import Bot, Dispatcher, types
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import StatesGroup, State
from aiogram.utils.callback_data import CallbackData

from Freelances.freelanceParser import *
from Freelances.habrParser import *
from Freelances.kworkParser import *
from config import bot_token, chat_id
from keyboards import *


class HabrParserCount(StatesGroup):
    count = State()


class FreelanceParserCount(StatesGroup):
    count = State()


class KworkParserCount(StatesGroup):
    count = State()


bot = Bot(token=bot_token)
dp = Dispatcher(bot, storage=MemoryStorage())
command = CallbackData('function')

auto_parse_habr, auto_parse_freelance, auto_parse_kwork = False, False, False
last_message_id, stop_event_habr, parsed_task_habr, last_task_habr = None, None, None, None
stop_event_freelance, parsed_task_freelance, last_task_freelance = None, None, None
stop_event_kwork, parsed_task_kwork, last_task_kwork = None, None, None


async def parse_and_process_habr(stop_event: asyncio.Event):
    global last_task_habr
    while not stop_event.is_set():
        tasks = await habr_parser(tasks_count=1)
        task = tasks[0]

        task_text = md.text(
            md.text(f'{task["title"]} ({task["url"]})'),
            md.text(f'Откликов: {task["resp_count"]}, Время: {task["time_ago"]}')
        )
        if last_task_habr is None or last_task_habr['title'] != task['title']:
            last_task_habr = task
            await bot.send_message(text=task_text, chat_id=chat_id)

        await asyncio.sleep(30)


async def parse_and_process_freelance(stop_event: asyncio.Event):
    global last_task_freelance
    while not stop_event.is_set():
        tasks = await freelance_parser(tasks_count=1)
        task = tasks[0]

        task_text = md.text(
            md.text(f'{task["title"]} ({task["url"]})'),
            md.text(f'Откликов: {task["resp_count"]}, Время: {task["time_ago"]}')
        )
        if last_task_freelance is None or last_task_freelance['title'] != task['title']:
            last_task_freelance = task
            await bot.send_message(text=task_text, chat_id=chat_id)

        await asyncio.sleep(30)


async def parse_and_process_kwork(stop_event: asyncio.Event):
    global last_task_kwork
    while not stop_event.is_set():
        tasks = kwork_parser(tasks_count=1)
        task = tasks[0]

        task_text = md.text(
            md.text(f'{task["title"]}\n'),
            md.text(f'{task["url"]}\n'),
            md.text(f'Откликов: {task["resp_count"]}')
        )
        if last_task_kwork is None or last_task_kwork['title'] != task['title']:
            last_task_kwork = task
            await bot.send_message(text=task_text, chat_id=chat_id)

        await asyncio.sleep(30)


@dp.message_handler(commands=['start'])
async def send_welcome(message: types.Message):
    await message.answer(
        md.text(
            md.text('Привет! Я бот для парсинга заказов.'),
            md.text('Выберите что вы хотите сделать.')
        ),
        reply_markup=main_menu_keyboard
    )


@dp.message_handler(text='Одиночный парсинг')
async def single_parse_menu(message: types.Message):
    await message.answer(
        md.text('Выберите с какого сервиса вы хотите запарсить заказы'),
        reply_markup=single_parse_keyboard

    )


@dp.callback_query_handler(text='single_parse_habr')
async def process_habr_parse_request(callback_query: types.CallbackQuery):
    await bot.answer_callback_query(callback_query.id)
    await callback_query.message.delete()
    await bot.send_message(callback_query.from_user.id, 'Сколько заказов хотите запарсить?')
    await HabrParserCount.count.set()


@dp.callback_query_handler(text='single_parse_freelance')
async def process_habr_parse_request(callback_query: types.CallbackQuery):
    await bot.answer_callback_query(callback_query.id)
    await callback_query.message.delete()
    await bot.send_message(callback_query.from_user.id, 'Сколько заказов хотите запарсить?')
    await FreelanceParserCount.count.set()


@dp.callback_query_handler(text='single_parse_kwork')
async def process_habr_parse_request(callback_query: types.CallbackQuery):
    await bot.answer_callback_query(callback_query.id)
    await callback_query.message.delete()
    await bot.send_message(callback_query.from_user.id, 'Сколько заказов хотите запарсить?')
    await KworkParserCount.count.set()


@dp.message_handler(text='Автоматический парсинг')
async def auto_parse_menu(message: types.Message):
    await message.answer(
        text='Выберите для каких сервисов включить автоматический парсинг',
        reply_markup=auto_parse_menu_keyboard(auto_parse_habr, auto_parse_freelance, auto_parse_kwork)
    )


@dp.callback_query_handler(text='auto_habr')
async def habr_parser_automode(callback_query: types.CallbackQuery):
    global auto_parse_habr, stop_event_habr, parsed_task_habr
    await bot.answer_callback_query(callback_query.id)
    await callback_query.message.delete()
    if auto_parse_habr := not auto_parse_habr:
        stop_event_habr = asyncio.Event()
        parsed_task_habr = asyncio.create_task(parse_and_process_habr(stop_event_habr))
        await bot.send_message(callback_query.from_user.id, 'Автоматический парсинг "Freelance Habr" был запущен',
                               reply_markup=auto_parse_menu_keyboard(auto_parse_habr, auto_parse_freelance,
                                                                     auto_parse_kwork))
    else:
        stop_event_habr.set()
        await bot.send_message(callback_query.from_user.id, 'Автоматический парсинг "Freelance Habr" был остановлен',
                               reply_markup=auto_parse_menu_keyboard(auto_parse_habr, auto_parse_freelance,
                                                                     auto_parse_kwork))
        await parsed_task_habr


@dp.callback_query_handler(text='auto_freelance')
async def freelance_parser_automode(callback_query: types.CallbackQuery):
    global stop_event_freelance, parsed_task_freelance, auto_parse_freelance
    await bot.answer_callback_query(callback_query.id)
    await callback_query.message.delete()
    if auto_parse_freelance := not auto_parse_freelance:
        stop_event_freelance = asyncio.Event()
        parsed_task_freelance = asyncio.create_task(parse_and_process_freelance(stop_event_freelance))
        await bot.send_message(callback_query.from_user.id, 'Автоматический парсинг "Freelance Habr" был запущен',
                               reply_markup=auto_parse_menu_keyboard(auto_parse_habr, auto_parse_freelance,
                                                                     auto_parse_kwork))
    else:
        stop_event_freelance.set()
        await bot.send_message(callback_query.from_user.id, 'Автоматический парсинг "Freelance Habr" был остановлен',
                               reply_markup=auto_parse_menu_keyboard(auto_parse_habr, auto_parse_freelance,
                                                                     auto_parse_kwork))
        await parsed_task_freelance


@dp.callback_query_handler(text='auto_kwork')
async def kwork_parser_automode(callback_query: types.CallbackQuery):
    global stop_event_kwork, parsed_task_kwork, auto_parse_kwork
    await bot.answer_callback_query(callback_query.id)
    await callback_query.message.delete()
    if auto_parse_kwork := not auto_parse_kwork:
        stop_event_kwork = asyncio.Event()
        parsed_task_kwork = asyncio.create_task(parse_and_process_kwork(stop_event_kwork))
        await bot.send_message(callback_query.from_user.id, 'Автоматический парсинг "Kwork" был запущен',
                               reply_markup=auto_parse_menu_keyboard(auto_parse_habr, auto_parse_freelance,
                                                                     auto_parse_kwork))
    else:
        stop_event_kwork.set()
        await bot.send_message(callback_query.from_user.id, 'Автоматический парсинг "Kwork" был остановлен',
                               reply_markup=auto_parse_menu_keyboard(auto_parse_habr, auto_parse_freelance,
                                                                     auto_parse_kwork))
        await parsed_task_kwork


@dp.message_handler(state=HabrParserCount.count)
async def process_habr_parse_count(message: types.Message, state: FSMContext):
    print(message.text)
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

    await message.reply(f'Найдено {len(tasks)} заказов!', reply_markup=single_parse_keyboard)
    await state.finish()


@dp.message_handler(state=FreelanceParserCount.count)
async def process_freelance_parse_count(message: types.Message, state: FSMContext):
    print(message.text)
    try:
        count = int(message.text)
        if count <= 0:
            raise ValueError()
    except ValueError:
        await message.reply('Количество заказов должно быть положительным числом!')
        return

    tasks = await freelance_parser(tasks_count=count)

    for task in tasks:
        task_text = md.text(
            md.text(f'{task["title"]} ({task["url"]})'),
            md.text(f'Откликов: {task["resp_count"]}, Время: {task["time_ago"]}')
        )
        await message.answer(task_text)

    await message.reply(f'Найдено {len(tasks)} заказов!', reply_markup=single_parse_keyboard)
    await state.finish()


@dp.message_handler(state=KworkParserCount.count)
async def process_kwork_parse_count(message: types.Message, state: FSMContext):
    print(message.text)
    try:
        count = int(message.text)
        if count <= 0:
            raise ValueError()
    except ValueError:
        await message.reply('Количество заказов должно быть положительным числом!')
        return

    tasks = kwork_parser(tasks_count=count)

    for task in tasks:
        task_text = md.text(
            md.text(f'{task["title"]}\n'),
            md.text(f'{task["url"]}\n'),
            md.text(f'Откликов: {task["resp_count"]}')
        )
        await message.answer(task_text)

    await message.reply(f'Найдено {len(tasks)} заказов!', reply_markup=single_parse_keyboard)
    await state.finish()


@dp.message_handler()
async def process_parse_request(message: types.Message):
    tasks = await freelance_parser(tasks_count=1)
    print(tasks)


if __name__ == '__main__':
    asyncio.run(dp.start_polling())
