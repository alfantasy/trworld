## -- Главные импорты -- ##

from aiogram import Router, types ## Роутеры (гл. хэндлеры) и типы сообщений
from aiogram.types import CallbackQuery # Использование спец.типа реакции на Callback
from aiogram.types import FSInputFile # Поддержка загрузки файлов
from aiogram import F # Магический фильтр
from utils.texts import get_game_message_by, get_message_by # Функция по захвату текстовых переменных
from keyboards.builders import game_keyboard, keyboard_return # Билдер клавиатуры

import utils.special_massive as SMV # Нефункциональный скрипт, содержащий спец.массивы

from aiogram.filters import StateFilter # Фильтр состояний
from aiogram.fsm.context import FSMContext # Контекст FSM

from config import db, config # База данных

## -- Главные импорты -- ##

router = Router()

## Игровой процесс ##

@router.callback_query(F.data.startswith('gotoworld_'))
async def read_gotoworld(callback: CallbackQuery, state: FSMContext):
    user_id = callback.from_user.id
    cuser_id = callback.data.split('_')[1]
    current_quest_id = await db.get_current_quest_id(user_id)
    if user_id == int(cuser_id):
        if current_quest_id == 0 or current_quest_id == None:
            #await callback.message.edit_text(get_message_by('gotoworld'), reply_markup=keyboard_return('gotoworld', user_id))
            await callback.message.answer(get_message_by('start_game_first'), reply_markup=game_keyboard('start_game_first', user_id, None))
        else:
            ...
    else:
        await callback.answer('🚫 Это сообщение не для Вас.')

@router.callback_query(F.data.startswith('start_game_first_'))
async def read_start_game_first(callback: CallbackQuery, state: FSMContext):
    user_id = callback.from_user.id
    cuser_id = callback.data.split('_')[3]
    if user_id == int(cuser_id):
        await callback.message.delete()
        await callback.message.answer(get_message_by('start_game_first'), reply_markup=game_keyboard('start_game_first', user_id, None))
    else:
        await callback.answer('🚫 Это сообщение не для Вас.')

@router.callback_query(F.data.startswith('prology_0_'))
async def read_prology_0(callback: CallbackQuery, state: FSMContext):
    user_id = callback.from_user.id
    cuser_id = callback.data.split('_')[2]
    data = await db.get_location(1)
    if user_id == int(cuser_id):
        await callback.message.delete()
        msg_id = await callback.message.answer_photo(photo=config["IMAGES"]["bereg"], caption=get_game_message_by('prology_0', data), reply_markup=game_keyboard('start_game_first', user_id, 'prology_0'))
        #await callback.message.edit_text(get_game_message_by('prology_0'), reply_markup=game_keyboard('prology_0', user_id))
    else:
        await callback.answer('🚫 Это сообщение не для Вас.')

## Игровой процесс ##