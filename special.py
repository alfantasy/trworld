import aiosqlite
import asyncio
import json
stats_for_weapon = {"damage": 1, "health": 10, "energy": 0.01, "speed": 0.5}

async def drop_users_tables(cursor):
    await cursor.execute('DROP TABLE IF EXISTS inventory_users;')
    await cursor.execute('DROP TABLE IF EXISTS user_skills;')
    await cursor.execute('DROP TABLE IF EXISTS users;')

def get_stats_for_weapon(damage: int, strength: int, energy: int, ammo: int, reload: int, spread: int, range: int, height: int):
    str_js = {
        "damage": damage,
        "strength": strength,
        "energy_use": energy,
        "ammo": ammo,
        "reload": reload,
        "spread": spread,
        "range": range,
        "height": height
    }
    return str_js

def get_stats_for_clothes(strength: int, effect: str, an_armor: int, height: int):
    str_js = {
        "strength": strength,
        "effect": effect,
        "an_armor": an_armor,
        "height": height
    }
    return str_js

def get_stats_for_armor(strength: int, height: int,armor_en: int, type_armor: str, armor_rebran: list = None):
    str_js = {
        "strength": strength,
        "height": height,
        "armor_en": armor_en,
        "type_armor": type_armor,
        "armor_rebran": armor_rebran
    }
    return str_js

def get_stats_for_medical(height: int, effect: str, health_to_heal: int):
    str_js = {
        "height": height,
        "effect": effect,
        "health_to_heal": health_to_heal
    }
    return str_js

def get_stats_for_food(height: int, effect: str, food_to_heal: int):
    str_js = {
        "height": height,
        "effect": effect,
        "food_to_heal": food_to_heal
    }
    return str_js

def get_stats_for_acs(strength: int, height: int, effect: str):
    str_js = {
        "strength": strength,
        "height": height,
        "effect": effect
    }
    return str_js

def get_stats_for_resources(height: int):
    str_js = {
        "height": height
    }
    return str_js

async def add_items(cursor):
    items = [                                                                          
    ]

    for item in items:
        ids = item[0]
        name = item[1]
        types = item[2]
        rarity = item[3]
        stats = json.dumps(item[4])
        caliber = item[5]
        description = item[6]
        can_sell = item[7]
        can_trade = item[8]
        can_craft = item[9]
        await cursor.execute('''INSERT OR IGNORE INTO items
                             (id, name, type, rarity, stats, caliber, description, can_sell, can_trade, can_craft)
                             VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?);''',
                             (ids, name, types, rarity, stats, caliber, description, can_sell, can_trade, can_craft))    

async def get_items_to_recipe(cursor):
    await cursor.execute('SELECT id FROM items WHERE can_craft = 1')
    craftable_ids = await cursor.fetchall()

    return [item_id[0] for item_id in craftable_ids]

async def add_craft_recipe(cursor, craft_ids):
    skills_to_required = [

    ]
    # if craft_ids != None:
    #     for item_id in craft_ids:
    #         await cursor.execute('INSERT INTO craft_recipes (result_item_id, required_skills_id, craft_time) VALUES (?, ?, ?)', (item_id))

async def add_skills(cursor):
    skills = [
    ]
    for skill in skills:
        name = skill[0]
        description = skill[1]
        type = skill[2]
        max_level = skill[3]
        price_upgrade = skill[4]
        price_get = skill[5]
        required_level = skill[6]
        await cursor.execute('''INSERT OR IGNORE INTO skills 
                            (name, description, type, max_level, price_exp_upgrade, 
                            price_exp_to_get, required_level) 
                            VALUES (?, ?, ?, ?, ?, ?, ?);''', 
                            (name, description, type, max_level, price_upgrade, 
                            price_get, required_level,))

async def add_quest_stage(cursor):
    await cursor.execute('''INSERT INTO quest_stages (quest_id, stage_number, name, description, trigger_type, trigger_target) 
                        VALUES (?, ?, ?, ?, ?);''',
                        (1, 1, "Пробуждение", "Первые минуты в абсолютно изменившимся мире", 'none', ''),
                        (1, 2, "Поиск живого", "Найдите выжившего на просторах Красной улицы", 'none', ''),
                        (1, 3, "Первая угроза", "Разберитесь с мутантом", 'kill', 'mutant_1'),
                        (1, 4, "Разговор с Виктором", "Узнайте, что здесь произошло", 
                        json.dumps(
                            {"npc_id": 1,
                            "required_node": "about_disaster"}
                            ),
                            'talk',
                            '1:safe_place'       
                        ),
                        (1, 5, "Дорога к Рембранда", "Доберитесь до улицы, о которой Вам рассказал Виктор"),
                        (1, 6, "Встреча с новыми людьми", "Решите конфликт."),
                        (1, 7, "Остаток военской службы...", "Поговорите с ветераном"),
                        (1, 8, "Бар Увикор", "Встретитесь в барменом"))

async def add_quest(cursor):
    await cursor.execute('''INSERT INTO quests (id, name, description, npc_id, reward, reward_exp, reward_money, reward_skills, reward_items, min_level, is_repeat, time_limit)
                        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?);''',
                        (1, "Первые шаги", "Адаптация в постапокалиптическом мире. Нужно узнать, что случилось с страной? Что происходит в мире? Неужели все настолько плохо?",
                        None, "Деньги, опыт, базовые навыки, вещи", 10, 1000, "4", "74, strength=10", 1, False, 0)
                    )

async def add_mutant(cursor):
    await cursor.execute('''INSERT INTO mutants (name, description, location, health, damage, items_to_drop)
                        VALUES (?, ?, ?, ?, ?, ?);''',
                        ("Обычный зомби", "Когда-то был обычным человеком, но превратился в зомби из-за катастрофы.", "All", 50, 3, "Нет")
                        )
    
async def add_npc(cursor, name: str, description: str, location: int, items_on_person: list = None, items_on_sell: list = None, quests: list = None, dialogue: dict = None, hostility: int = 1, health: int = None):
    if name == None:
        return 'Не можем создать NPC без имени'
    if quests == None:
        quests = 'Нет'
    if dialogue == None:
        dialogue = 'Не разговорчив.'
    if health == None:
        health = 100
    if items_on_person == None:
        items_on_person = 'Нет'
    if items_on_sell == None:
        items_on_sell = 'Нет'
    
    await cursor.execute('''INSERT INTO npc (name, description, location, items_on_person, items_on_sell, quests, dialogue, hostility, health)
                        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?);''',
                        (name, 
                        description, 
                        location, 
                        json.dumps(items_on_person) if items_on_person != None else items_on_person, 
                        json.dumps(items_on_sell) if items_on_sell != None else items_on_sell, 
                        json.dumps(quests) if quests != None else quests, 
                        json.dumps(dialogue) if dialogue != None else dialogue, 
                        hostility, 
                        health)
                        )
    
async def add_enemies(cursor):
    dialog = {
        "default": {
            "text": "Эй, кореш! Проход: 1000 баксов",
            "answers": [
                {"text": "У меня есть деньги", "next": "pay", "condition": "has_item:money:1000"},
                {"text": "Я не буду платить, вообще!", "next": "refuse"},
                {"text": "Может еще как-то договоримся?", "next": "negotiate"},
            ]
        },
        "pay": {
            "text": "Отличный выбор, давай, дуй теперь отсюда!",
            "answers": [
                {"text": "[Продолжить путь]", "next": "end", "action": "remove_item:money:1000"},
            ]
        },
        "refuse": {
            "text": "Да ты что!? Значит получай по морде, ублюдок еб*нный!",
            "answers": [
                {"text": "[Сразиться]", "next": "end", "action": "fight"}
            ]
        },
        "negotiate": {
            "text": "И как же ты хочешь договориться?",
            "answers": [
                {"text": "Вы же вроде, парни, хорошие, может пропустите так? Я только недавно очнулся", "next": "negotiate_0"},
                {"text": "[Убежать]", "next": "end", "action": "escape"},
                {"text": "[Сразиться]", "next": "end", "action": "fight"}
            ]
        },
        "negotiate_0": {
            "text": "Ну валяй, что еще скажешь?",
            "answers": [
                {"text": "У меня нет желания с Вами драться, да и денег у меня нет, поймите", "next": "negotiate_1"},
                {"text": "Да, иди ты нах*й!", "next": "end", "action": "fight"},
                {"text": "[Убежать]", "next": "end", "action": "escape"}
            ]
        },
        "negotiate_1": {
            "text": "Да бл*ть... Устал я от тебя, иди отсюда.",
            "answers": [
                {"text": "[Продолжить путь]", "next": "end"},
            ]
        }
    }
    await cursor.execute('''INSERT INTO enemies (name, description, dialogue, location, health, damage, items_to_drop)
                        VALUES (?, ?, ?, ?, ?, ?, ?);''',
                        ("Мародер", "Не пытается даже проявить человечность. Просто натуральный идиот, пытающийся взять с Вас все.", json.dumps(dialog), "All", 75, 5, "Нет")
                        )

class Droping:
    async def drop(cursor, tb):
        if tb == 'qstages':
            await cursor.execute('DROP TABLE quest_stages;')

async def run():
    connection = await aiosqlite.connect('database.db')
    cursor = await connection.cursor()
    # await cursor.execute('''INSERT OR IGNORE INTO locations 
    #                     (id, name, description, danger, loc_to, 
    #                     loc_in, resources, enemies, is_hidden, level, photo) 
    #                     VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?);''', 
    #                     (1, 'Берег', 'Берег', 0, 'Улица Красная', 
    #                     'Улица Красная', 'Никаких', 'Нет', False, 1, 'photo'))
    # await cursor.execute('''INSERT INTO skills 
    #                      (id, name, description, type, level, 
    #                      exp, price_upgrade, price, required_level)
    #                      VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?);''',
    #                      (1, "Владение холодным оружием", "Позволяет использовать холодное оружие", "Умение", 1, 0, 5, 0, 1))
    # await cursor.execute('''INSERT INTO skills 
    #                      (id, name, description, type, level, 
    #                      exp, price_upgrade, price, required_level)
    #                      VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?);''',
    #                      (2, "Выносливость", "Повышает энергию. Позволяет быстрее восстанавливать энергию.", "Умение", 1, 0, 5, 0, 1))    
    # await cursor.execute('''INSERT OR IGNORE INTO items
    #                      (id, name, type, rarity, stats, description, can_sell, can_trade)
    #                      VALUES (?, ?, ?, ?, ?, ?, ?, ?);''',
    #                      (1, "Порванные тряпки", 'Одежда', 'Низкий', 'Нет', 'Порванные тряпки, которые больше непригодны.', False, False))
    #await cursor.execute('UPDATE items SET stats = ? WHERE id = 2;', (json.dumps(stats_for_weapon),))
    desc_loc = '''Ничем не примечательный берег. Вокруг морская тишина, не слышно ни одной живой души. Вдоль берега простилается "неживой пляж".
Казалось бы, что здесь такого? <b>Здесь нет ни единой души.</b>

Позади Вас выход на улицу Красная, не привлекающая особого внимания. Все-таки, край города.

Впереди Вас - бескрайний морской простор.
'''
        # [
        #     id, name, type, ratity, 
        #     stats, caliber,
        #     description, can_sell, can_trade
        # ],   
    #await cursor.execute('UPDATE locations SET description = ? WHERE id = 1;', (desc_loc,))
    # await cursor.execute('''INSERT OR IGNORE INTO items
    #                      (id, name, type, rarity, stats, description, can_sell, can_trade)
    #                      VALUES (?, ?, ?, ?, ?, ?, ?, ?);''',
    #                      (2, "Старый ржавый нож", 'Оружие', 'Низкий', json.dumps(stats_for_weapon), 'Старый ржавый нож, доставшийся случайно при непредвиденных обстоятельствах.', False, False))    

    #await add_craft_recipe(cursor, await get_items_to_recipe(cursor))
    #await add_skills(cursor)

    # dialog_for_victor = {
    #     "default": {
    #         "text": "Вы кто такой? Я никого не знаю здесь...",
    #         "answers": [
    #             {"text": "Что здесь произошло?", "next": "about_disaster"},
    #             {"text": "Ты знаешь безопасное место?", "next": "safe_place"},
    #             {"text": "У меня нет времени на разговоры.", "next": "end"}
    #         ]
    #     },
    #     "about_disaster": {
    #         "text": "Уже не помню. Перед моими глазами в мгновение ока все затмилось...",
    #         "answers": [
    #             {"text": "Кто это сделал?", "next": "who_did_it"},
    #             {"text": "Где теперь безопасно?", "next": "safe_place"},
    #             {"text": "Спасибо за информацию..", "next": "end"}
    #         ]
    #     },
    #     "who_did_it": {
    #         "text": "Как все говорят, точнее, у тех, у кого я спрашивал, это было правительство. Больше я ничего не знаю.",
    #         "answers": [
    #             {"text": "Ясно. Спасибо.", "next": "end"}
    #         ]
    #     },
    #     "safe_place": {
    #         "text": "Я и сам не знаю...",
    #         "answers": [
    #             {"text": "Ясно. Спасибо.", "next": "end"}
    #         ]
    #     }
    # }

    # await cursor.execute('''INSERT INTO npc (id, name, description, location, items_on_person, items_on_sell, quests, dialogue, hostility, health)
    #                         VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?);''',
    #                         (1, "Виктор", "Один из выживших, который стоит на нейтралитете и мало с кем разговаривает. От него можно узнать лишь то, что он жив.",
    #                         1, json.dumps([53, 74, 77, 79, 81]), "Нет", json.dumps([1]), json.dumps(dialog_for_victor), 1, 100)
    #                         )

    # await add_npc(cursor,
    #               "Мит",
    #               "Бывший ветеран войны, который и так мало того, что повидал многое, так еще и остался в живых после катастрофы",
    #               3,
    #               [21, 50, 51, 79, 81],
    #               None,
    #               [1],
    #               {
    #                   "default": {
    #                       "text": "Стой! Кто идет?",
    #                       "answers": [
    #                           {"text": "Простите, я только недавно очнулся. Не знаете, где здесь безопасное место?", "next": "info"},
    #                           {"text": "Что здесь вообще происходит?", "next": "info"},
    #                       ]
    #                   },
    #                   "info": {
    #                       "text": "Как бы тебе сказать... Правительство сделало, что хотело. Мало того, что запустили ядерные боеголовки и неудачно, так еще и вирус распространился. Здесь уже не стоит оставаться, нужно уходить. Я знаю безопасное место, это Бар Увикор, он находится впереди, не спутаешь, там вывеска стоит и охрана, но ты спокойно войдешь, раз живой...",
    #                       "answers": [
    #                           {"text": "Спасибо, я тогда пойду..", "next": "end"},
    #                       ]
    #                   }
    #               },
    #               1, 
    #               100)

    # await add_npc(cursor, 
    #               "Бармен Ник", 
    #               "Обычный бармен, который выжил после катастрофы и владеет Увикором. Добрый мужик, который не откажет в помощи", 
    #               4, 
    #               None, 
    #               None, 
    #               [1],
    #               {
    #                   "default_for_quest_0": {
    #                       "text": "Опа, привет! Я тебя что-то не припомню.. Как ты нашел нас?",
    #                       "answers": [
    #                           {"text": "Меня сюда военный направил, похож на ветерана.. ", "next": "welcome_to_bar"},
    #                           {"text": "Просто искал убежище..", "next": "welcome_to_bar"},
    #                       ]
    #                   },
    #                   "welcome_to_bar": {
    #                       "text": "Здесь ты в безопасности.. Подходи, если хочешь что-то узнать, купить или выпить..",
    #                       "answers": [
    #                           {"text": "Хорошо, спасибо..", "next": "end", "action": "complete_quest:1"}
    #                       ]
    #                   }
    #               },
    #               1,
    #               100)

    # await cursor.execute('SELECT * FROM npc WHERE id = 1;')
    # npc = await cursor.fetchone()
    # items = json.loads(npc[4])
    # for item in items:
    #     await cursor.execute('SELECT * FROM items WHERE id = ?;', (item,))
    #     item_info = await cursor.fetchone()
    #     print(item_info[1])
    # print(f'ID: {npc[0]}\nName: {npc[1]}\nDescription: {npc[2]}\nLocation: {npc[3]}\nItems on person: {npc[4]}\nItems on sell: {npc[5]}\nQuests: {npc[6]}\nDialogue: {npc[7]}\nHostility: {npc[8]}\nHealth: {npc[9]}')

    # await cursor.execute('''INSERT INTO quest_objectives (stage_id, objective_type, target_id, target_value)
    #                      VALUES (?, ?, ?, ?);''',
    #                      (3, 'kill', 1, 1))
    
    # await add_enemies(cursor)
    
    # await cursor.execute('''INSERT INTO dialog_options (quest_stage_id, is_enemy, npc_id, text, next_stage_id) 
    #                      VALUES 
    #                      (6, 1, 1, "Напасть на мародеров", 7),
    #                      (6, 1, 1, "Попытаться договориться", 7),
    #                      (6, 1, 1, "Дать взятку", 7);''')
    
    # await cursor.execute('''INSERT INTO quest_branches (quest_id, from_stage_id, to_stage_id, condition_type, condition_value)
    #                      VALUES
    #                      (1, 6, 7, "choice", "{"options": [1, 2, 3]}"),
    #                      (1, 6, 7, "combat", "{"enemy_id": 1, "win_stage": 7, "lose_stage": 5}");''')
    
    await connection.commit()
    await connection.close()
asyncio.run(run())