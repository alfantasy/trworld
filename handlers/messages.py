## -- Главные импорты -- ##

from aiogram import Router, types # Роутеры (гл. хэндлеры) и типы сообщений
from aiogram.types import CallbackQuery, FSInputFile # Использование спец.типа реакции на нажатие по клавишам в сообщениях
from aiogram import F # Магический фильтр
from utils.texts import get_message_by, get_game_message_by # Функция по захвату текстовых переменных (сообщений)
from keyboards.builders import keyboard_return, game_keyboard # Билдер клавиатуры
import utils.special_massive as SMV # Нефункциональный скрипт, содержащий спец.массивы

from aiogram.filters import StateFilter # Фильтр состояний
from aiogram.fsm.context import FSMContext # Контекст FSM
from middlewares.storage import UserLoreRead # Состояния FSM

from config import db, config # База данных

## -- Главные импорты -- ##

router = Router()

@router.callback_query(F.data.startswith('welcome_start_'))
async def read_welcome_start(callback: CallbackQuery, state: FSMContext):
    user_id = callback.from_user.id
    cuser_id = callback.data.split('_')[2]
    data, check_reg = await db.get_info_user(user_id)
    if user_id == int(cuser_id):
        await state.set_state(state=None)
        user_data = await state.get_data()
        if check_reg == False:
            try:
                if user_data['lore_read']:
                    await callback.message.edit_text(get_message_by('welcome'), reply_markup=keyboard_return('welcome', user_id, 1))
                else:
                    await callback.message.edit_text(get_message_by('welcome'), reply_markup=keyboard_return('welcome', user_id))
            except KeyError:
                await callback.message.edit_text(get_message_by('welcome'), reply_markup=keyboard_return('welcome', user_id))
        else:
            await callback.message.edit_text(get_message_by('main', data), reply_markup=keyboard_return('main', user_id))
    else:
        await callback.answer('🚫 Это сообщение не для Вас.')

@router.callback_query(F.data.startswith('read_lore_game_'))
async def read_lore_game(callback: CallbackQuery, state: FSMContext):
    user_id = callback.from_user.id
    cuser_id = callback.data.split('_')[3]
    if user_id == int(cuser_id):
        await callback.message.edit_text(get_message_by('lore_0'), reply_markup=keyboard_return('lore_game', user_id, 1))
    else:
        await callback.answer('🚫 Это сообщение не для Вас.')

@router.callback_query(F.data.startswith('lore_game_1_'))
async def read_lore_game_1(callback: CallbackQuery, state: FSMContext):
    user_id = callback.from_user.id
    cuser_id = callback.data.split('_')[3]
    if user_id == int(cuser_id):
        await callback.message.edit_text(get_message_by('lore_0'), reply_markup=keyboard_return('lore_game', user_id, 1))
    else:
        await callback.answer('🚫 Это сообщение не для Вас.')

@router.callback_query(F.data.startswith('lore_game_2_'), StateFilter(None))
async def read_lore_game_2(callback: CallbackQuery, state: FSMContext):
    user_id = callback.from_user.id
    cuser_id = callback.data.split('_')[3]
    if user_id == int(cuser_id):
        await callback.message.edit_text(get_message_by('lore_1'), reply_markup=keyboard_return('lore_game', user_id, 2))
        await state.set_state(UserLoreRead.read)
    else:
        await callback.answer('🚫 Это сообщение не для Вас.')

@router.callback_query(F.data.startswith('confirm_lore_'), StateFilter(UserLoreRead.read))
async def read_confirm_lore(callback: CallbackQuery, state: FSMContext):
    user_id = callback.from_user.id
    cuser_id = callback.data.split('_')[2]
    if user_id == int(cuser_id):
        await callback.message.edit_text('✅ Вы успешно отметили, что прочитали лор. Теперь Вам доступна регистрация \n⚡ Также рекомендуется прочитать раздел <b>Игровые механики</b>, расположенный на Главной.', reply_markup=keyboard_return('lore_game', user_id, 3))
        await state.update_data(lore_read=True)
        await state.set_state(state=None)
    else:
        await callback.answer('🚫 Это сообщение не для Вас.')

@router.callback_query(F.data.startswith('game_mechanics_'))
async def read_game_mechanics(callback: CallbackQuery):
    user_id = callback.from_user.id
    cuser_id = callback.data.split('_')[2]
    if user_id == int(cuser_id):
        await callback.message.edit_text(get_message_by('game_mechanics'), reply_markup=keyboard_return('game_mechanics', user_id, 0))
    else:
        await callback.answer('🚫 Это сообщение не для Вас.')

@router.callback_query(F.data.in_(SMV.game_mechanics_ids))
async def read_game_mechanic_any(callback: CallbackQuery):
    user_id = callback.from_user.id
    cuser_id = callback.data.split('_')[3]
    if user_id == int(cuser_id):
        await callback.message.edit_text(get_message_by(callback.data), reply_markup=keyboard_return('game_mechanics', user_id, 1))
    else:
        await callback.answer('🚫 Это сообщение не для Вас.')

## Главный регистратор. Позволяет зарегистрировать пользователя и заносит данные в БД ##
@router.callback_query(F.data.startswith('registration_'))
async def read_registration(callback: CallbackQuery, state: FSMContext):
    user_id = callback.from_user.id
    user_data = await state.get_data()
    cuser_id = callback.data.split('_')[1]
    if user_id == int(cuser_id):
        try:
            data, check_reg = await db.get_info_user(user_id)
            if check_reg == False:
                tdata = callback.from_user.username
                await db.register_user(user_id=user_id, tg_username=tdata, nickname=callback.from_user.first_name)
                await callback.message.edit_text(get_message_by('complete_reg', tdata), reply_markup=keyboard_return('complete_reg', user_id))
            else:
                await callback.message.edit_text('Вы уже зарегистрированы.', reply_markup=keyboard_return('static', user_id))
        except KeyError:
            await callback.message.edit_text('В процессе разработки...\nСтатус прочтения лора: ❌', reply_markup=keyboard_return('static', user_id))
    else:
        await callback.answer('🚫 Это сообщение не для Вас.')

## Инвентарь
@router.callback_query(F.data.startswith('get_inventory_'))
async def read_inventory(callback: CallbackQuery, state: FSMContext):
    user_id = callback.from_user.id
    cuser_id = callback.data.split('_')[2]
    data, keys_items = await db.show_inventory(user_id)
    if user_id == int(cuser_id):
        await callback.message.edit_text(get_message_by('inventory', data), reply_markup=keyboard_return('inventory', user_id, 'reqitems', keys_items))
    else:
        await callback.answer('🚫 Это сообщение не для Вас.')

@router.callback_query(F.data.startswith('inventory_item_select_'))
async def read_inventory_item_select(callback: CallbackQuery, state: FSMContext):
    user_id = callback.from_user.id
    cuser_id = callback.data.split('_')[3]
    item_id = callback.data.split('_')[4]
    #data, keys_items = await db.show_inventory(user_id)
    data = await db.get_info_item(item_id)
    if user_id == int(cuser_id):
        await callback.message.edit_text(get_message_by('item_info_inv', data), reply_markup=keyboard_return('inventory', user_id, 'item_info', data))
        #await callback.message.edit_text(get_message_by('item_info', item_id), reply_markup=keyboard_return('item_info', user_id, item_id))
    else:
        await callback.answer('🚫 Это сообщение не для Вас.')