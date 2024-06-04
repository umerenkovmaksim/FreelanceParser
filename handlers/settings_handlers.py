from aiogram import Router, F, types
from aiogram.enums import ParseMode

from categories import *
from database import get_user_settings, set_user_settings
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

@router.callback_query(F.data.endswith('_state'))
async def change_categories_state(callback_query: types.CallbackQuery):
    await callback_query.message.delete()
    user_settings = await get_user_settings(callback_query.from_user.id)
    data = callback_query.data.split('_')
    cat_list = user_settings[f'{data[1]}_categories'].split(',')
    if user_settings[f'{data[1]}_categories'] == '-1':
        await set_user_settings(
            user_id=callback_query.from_user.id, 
            **{f'{data[1]}_categories': data[0]}
        )
    elif data[0] in cat_list:
        if len(cat_list) == 1:
            cat_list = ['-1']
        else:
            cat_list.remove(data[0])
        await set_user_settings(
            user_id=callback_query.from_user.id, 
            **{f'{data[1]}_categories': ','.join(cat_list)}
        )
    else:
        await set_user_settings(
            user_id=callback_query.from_user.id, 
            **{f'{data[1]}_categories': ','.join(cat_list + [data[0]])}
        )
    await callback_query.message.answer(
        text='Выберите категории которые будут использоваться при поиске заказов',
        reply_markup=await categories_keyboard(callback_query.from_user.id, 'habr'),
    )
    
