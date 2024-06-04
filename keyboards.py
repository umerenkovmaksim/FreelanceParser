from aiogram.utils.keyboard import InlineKeyboardBuilder, ReplyKeyboardBuilder
from aiogram.types import InlineKeyboardButton
from aiogram.types import KeyboardButton, ReplyKeyboardMarkup

from categories import *
from database import get_user_settings


async def auto_parse_menu_keyboard(user_id):
    user_settings = await get_user_settings(user_id)
    markup = InlineKeyboardBuilder()
    markup.add(
        InlineKeyboardButton(
            text='Отключить автоматический парсер Freelance Habr'
            if user_settings['auto_habr']
            else 'Запустить автоматический парсер Freelance Habr',
            callback_data='auto_habr',
        )
    )
    markup.add(
        InlineKeyboardButton(
            text='Отключить автоматический парсер Freelance.ru'
            if user_settings['auto_freelance']
            else 'Запустить автоматический парсер Freelance.ru',
            callback_data='auto_freelance',
        )
    )
    markup.add(
        InlineKeyboardButton(
            text='Отключить автоматический парсер Kwork'
            if user_settings['auto_kwork']
            else 'Запустить автоматический парсер Kwork',
            callback_data='auto_kwork',
        )
    )
    return markup.as_markup()


async def categories_keyboard(user_id, service):
    markup = InlineKeyboardBuilder()
    user_settings = await get_user_settings(user_id)
    user_categories = tuple(map(int, user_settings[f'{service}_categories'].split(',')))
    categories = habr_categories if service == 'habr' else freelance_categories
    for cat_id in categories:
        markup.add(InlineKeyboardButton(
            text=f'{"✅" if cat_id in user_categories else "❌"}{categories[cat_id]["ru"]}', 
            callback_data=f'{cat_id}_{service}_state'
        ))
    markup.adjust(1)

    return markup.as_markup()


single_parse_keyboard = InlineKeyboardBuilder()
single_parse_keyboard.add(InlineKeyboardButton(text='Freelance Habr', callback_data='single_parse_habr'))
single_parse_keyboard.add(InlineKeyboardButton(text='Freelance.ru', callback_data='single_parse_freelance'))
single_parse_keyboard.add(InlineKeyboardButton(text='Kwork', callback_data='single_parse_kwork'))

main_menu_keyboard = ReplyKeyboardBuilder()
main_menu_keyboard.add(KeyboardButton(text='Автоматический парсинг'))
main_menu_keyboard.add(KeyboardButton(text='Одиночный парсинг'))
main_menu_keyboard.add(KeyboardButton(text='Настройки'))
main_menu_keyboard.add(KeyboardButton(text='Обратная связь'))
main_menu_keyboard.adjust(2)

settings_keyboard = InlineKeyboardBuilder()
settings_keyboard.add(InlineKeyboardButton(text='Freelance Habr', callback_data='habr_settings'))
settings_keyboard.add(InlineKeyboardButton(text='Freelance.ru', callback_data='freelance_settings'))
settings_keyboard.add(InlineKeyboardButton(text='Kwork', callback_data='kwork_settings'))



