from aiogram import Router, types # Роутеры (гл хэндлеры)
from aiogram.filters import Command # Парс-команды
from keyboards.builders import keyboard_return # Билдер клавиатуры
from utils.texts import get_message_by # Функция по захвату текстовых переменных
from config import db # База данных

router = Router()

@router.message(Command("start"))
async def cmd_start(message: types.Message):
    user_id = message.from_user.id
    data, check_reg = await db.get_info_user(user_id)
    print(data, check_reg)
    if check_reg == False:
        await message.reply(get_message_by('welcome'), reply_markup=keyboard_return('welcome', user_id))
    else:
        await message.reply(get_message_by('main', data), reply_markup=keyboard_return('main', user_id))

@router.message(Command("help"))
async def cmd_help(message: types.Message):
    await message.reply("Список команд: /start, /help")

@router.message(Command("inventory"))
async def cmd_inventory(message: types.Message):
    data, keys_items = await db.show_inventory(message.from_user.id)
    await message.reply(get_message_by('inventory', data), reply_markup=keyboard_return('inventory', message.from_user.id, 'reqitems', keys_items))

@router.message(Command("test"))
async def cmd_test(message: types.Message):
    await db.register_user(user_id=message.from_user.id, tg_username=message.from_user.username, nickname=message.from_user.first_name)
    await message.reply("Тестовая команда")
