from aiogram import Router, F, types
from aiogram.enums import ParseMode

from categories import *
from database import get_user_settings
from keyboards import *


router = Router()


@router.message(F.text.lower() == 'настройки')
async def settings_menu(message: types.Message):
    await message.answer(
        'Это меню настроек, здесь вы можете изменить данные об аккаунте, а также настроить парсинг фриланс бирж\n'
        '**Выберите нужный вам раздел:**',
        parse_mode=ParseMode.MARKDOWN, 
        reply_markup=settings_keyboard.as_markup()
    )

@router.callback_query(F.data == 'habr_settings')
async def habr_settings(callback_query: types.CallbackQuery):
    await callback_query.message.delete()
    await callback_query.message.answer(
        text='Выберите категории которые будут использоваться при поиске заказов',
        reply_markup=await categories_keyboard(callback_query.from_user.id, 'habr'),
    )


    
