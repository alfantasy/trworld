from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from aiogram.utils.keyboard import InlineKeyboardBuilder
from utils.special_massive import titems, tids_items_to_equip as tequip

def keyboard_return(id_keyboard, user_id, ids_request=None, data=None):
    '''
    :param id_keyboard -> str, int: id клавиатуры
    :param ids_request -> str, int, list: дополнительный id клавиатур при нахождении продолжительных Callback.
    :return: клавиатура

    Позволяет возвращать клавиши и Markup клавиатуры по специальному ID.
    
    Для просмотра ID, перейдите в файл keyboard/builders.py
    Функция возвратная - keyboard_return()
    '''
    keyboard = InlineKeyboardBuilder()
    if id_keyboard == 'welcome':
        if ids_request == 1:
            keyboard.row(
                InlineKeyboardButton(
                    text = '🔑 Зарегистрироваться',
                    callback_data = f'registration_{user_id}'
                )
            )
        keyboard.row(
            InlineKeyboardButton(
                text = '📖 Лор',
                callback_data = f'read_lore_game_{user_id}'
            )
        )
        keyboard.row(
            InlineKeyboardButton(
                text = '🎮 Игровые механики',
                callback_data = f'game_mechanics_{user_id}'
            )
        )
    elif id_keyboard == 'static':
        keyboard.row(
            InlineKeyboardButton(
                text = '🌐 На главную',
                callback_data = f'welcome_start_{user_id}'
            )
        )
    elif id_keyboard == 'main':
        keyboard.row(
            InlineKeyboardButton(
                text = 'Выйти в мир',
                callback_data = f'gotoworld_{user_id}'
            )
        )
        keyboard.row(
            InlineKeyboardButton(
                text = 'Инвентарь',
                callback_data = f'get_inventory_{user_id}'
            )
        )
    elif id_keyboard == 'lore_game':
        if ids_request == 1:
            keyboard.add(
                InlineKeyboardButton(
                    text = '➡️ Далее',
                    callback_data = f'lore_game_2_{user_id}'
                )
            )
            keyboard.row(
                InlineKeyboardButton(
                    text = '🌐 На главную',
                    callback_data = f'welcome_start_{user_id}'
                )
            )
        if ids_request == 2:
            keyboard.add(
                InlineKeyboardButton(
                    text = '🆗 Лор прочтен',
                    callback_data = f'confirm_lore_{user_id}'
                )
            )
            keyboard.row(
                InlineKeyboardButton(
                    text = '⬅️ Назад',
                    callback_data = f'lore_game_1_{user_id}'
                )
            )
        if ids_request == 3:
            keyboard.row(
                InlineKeyboardButton(
                    text = '🔑 Зарегистрироваться',
                    callback_data = f'registration_{user_id}'
                )
            )
            keyboard.row(
                InlineKeyboardButton(
                    text = '🌐 На главную',
                    callback_data = f'welcome_start_{user_id}'
                )
            )            
    elif id_keyboard == 'game_mechanics':
        if ids_request == 0:
            keyboard.row(
                InlineKeyboardButton(
                    text = '🌍 Игровой мир 🌍',
                    callback_data = f'game_mechanic_game_world_{user_id}'
                )
            )
            keyboard.row(
                InlineKeyboardButton(
                    text = '⚔️ PvP и PvE режимы ⚔️',
                    callback_data = f'game_mechanic_pvpe_mode_{user_id}'
                )
            )
            keyboard.row(
                InlineKeyboardButton(
                    text = '🛡️ Клановая система 🛡️',
                    callback_data = f'game_mechanic_clan_system_{user_id}'
                )
            )
            keyboard.row(
                InlineKeyboardButton(
                    text = '🧟 Боссы 🧟',
                    callback_data = f'game_mechanic_zombie_bosses_{user_id}'
                )
            )
            keyboard.row(
                InlineKeyboardButton(
                    text = '👑 Рейтинговая система 👑',
                    callback_data = f'game_mechanic_rating_system_{user_id}'
                )
            )
            keyboard.row(
                InlineKeyboardButton(
                    text = '📜 Система квестов 📜',
                    callback_data = f'game_mechanic_quests_system_{user_id}'
                )
            )
            keyboard.row(
                InlineKeyboardButton(
                    text = '⬅️ Назад',
                    callback_data = f'welcome_start_{user_id}'
                )
            )
        elif ids_request == 1:
            keyboard.row(
                InlineKeyboardButton(
                    text = '⬅️ Назад',
                    callback_data = f'game_mechanics_{user_id}'
                )
            )
            keyboard.row(
                InlineKeyboardButton(
                    text = '⏮️ Сразу на главную',
                    callback_data = f'welcome_start_{user_id}'
                )
            )
    elif id_keyboard == 'complete_reg':
        keyboard.row(
            InlineKeyboardButton(
                text = 'Начать игру...',
                callback_data = f'start_game_first_{user_id}'
            )
        )
    elif id_keyboard == 'inventory':
        if data is not None:
            if ids_request == 'back':
                keyboard.row(
                    InlineKeyboardButton(
                        text = '⬅️🗄️ Назад в инвентарь',
                        callback_data = f'get_inventory_{user_id}'
                    )
                )
            elif ids_request == 'reqitems':
                for item in data:
                    id_item, name, item_type, ratity, quantity = item
                    keyboard.row(
                        InlineKeyboardButton(
                            text = '📦 ' + name,
                            callback_data = f'inventory_item_select_{user_id}_{id_item}'
                        )
                    )
            elif ids_request == 'item_info':
                item_info = data
                if item_info[2] in tequip:
                    keyboard.row(
                        InlineKeyboardButton(
                            text = 'Экипировать',
                            callback_data = f'equip_item_{user_id}_{item_info[0]}'
                        )
                    )
                keyboard.row(
                    InlineKeyboardButton(
                        text = '⬅️🗄️ Назад в инвентарь',
                        callback_data = f'get_inventory_{user_id}'
                    )
                )
        keyboard.row(
            InlineKeyboardButton(
                text = '⬅️ Назад на главную',
                callback_data = f'welcome_start_{user_id}'
            )
        )
    return keyboard.as_markup()

def game_keyboard(id_keyboard, user_id, ids_request=None, data=None):
    '''
    :param id_keyboard -> str, int: id клавиатуры
    :param ids_request -> str, int, list: дополнительный id клавиатур при нахождении продолжительных Callback.
    :return: клавиатура

    Позволяет возвращать клавиши и Markup клавиатуры по специальному ID.
    
    Для просмотра ID, перейдите в файл keyboard/builders.py
    Функция возвратная - game_keyboard()
    '''
    keyboard = InlineKeyboardBuilder()
    if id_keyboard == 'start_game_first':
        if ids_request == None:
            keyboard.add(
                InlineKeyboardButton(
                    text = 'Проснуться и оглядеться',
                    callback_data = f'prology_0_{user_id}'
                )
            )
        elif ids_request == f'prology_0':
            keyboard.add(
                InlineKeyboardButton(
                    text = '⬅️ Назад',
                    callback_data = f'start_game_first_{user_id}'
                )
            )
    return keyboard.as_markup()