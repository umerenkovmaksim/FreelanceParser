from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup


def auto_parse_menu_keyboard(auto_habr, auto_freelance):
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
    markup.add(InlineKeyboardButton('Меню', callback_data='menu'))
    return markup


main_menu_keyboard = InlineKeyboardMarkup()
main_menu_keyboard.add(InlineKeyboardButton('Спарсить заказы с "Freelance Habr"', callback_data='single_parse_habr'))
main_menu_keyboard.add(InlineKeyboardButton('Спарсить заказы с "Freelance.ru"', callback_data='single_parse_freelance'))
main_menu_keyboard.add(InlineKeyboardButton('Автоматический парсинг', callback_data='auto_parse'))

single_parser_keyboard = InlineKeyboardMarkup()
single_parser_keyboard.add(InlineKeyboardButton(''))
