from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from aiogram.types import KeyboardButton, ReplyKeyboardMarkup


def auto_parse_menu_keyboard(auto_habr, auto_freelance, auto_kwork):
    markup = InlineKeyboardMarkup()
    markup.add(
        InlineKeyboardButton(
            'Отключить автоматический парсер "Freelance Habr"'
            if auto_habr
            else 'Запустить автоматический парсер "Freelance Habr"',
            callback_data='auto_habr',
        )
    )
    markup.add(
        InlineKeyboardButton(
            'Отключить автоматический парсер "Freelance.ru"'
            if auto_freelance
            else 'Запустить автоматический парсер "Freelance.ru"',
            callback_data='auto_freelance',
        )
    )
    markup.add(
        InlineKeyboardButton(
            'Отключить автоматический парсер "Kwork"'
            if auto_kwork
            else 'Запустить автоматический парсер "Kwork"',
            callback_data='auto_kwork',
        )
    )
    return markup


single_parse_keyboard = InlineKeyboardMarkup()
single_parse_keyboard.add(InlineKeyboardButton('Спарсить заказы с "Freelance Habr"', callback_data='single_parse_habr'))
single_parse_keyboard.add(InlineKeyboardButton('Спарсить заказы с "Freelance.ru"', callback_data='single_parse_freelance'))
single_parse_keyboard.add(InlineKeyboardButton('Спарсить заказы с "Kwork"', callback_data='single_parse_kwork'))

main_menu_keyboard = ReplyKeyboardMarkup(resize_keyboard=True)
main_menu_keyboard.add(KeyboardButton('Автоматический парсинг'))
main_menu_keyboard.add(KeyboardButton('Одиночный парсинг'))


