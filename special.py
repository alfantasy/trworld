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
        [
            "Владение холодным оружием",
            "Позволяет использовать холодное оружие. При улучшении уровня владения холодным оружием, меньше шанс промахнуться, упасть с более тяжелым оружием и выше шанс поставить критический урон.",
            "Активное умение",
            10,
            5,
            0,
            1
        ],
        [
            "Выносливость",
            "Увеличивает максимальное количество энергии, понижает время восстановления энергии.",
            "Пассивное умение",
            10,
            10,
            0,
            1
        ],
        [
            "Владение огнестрельным оружием",
            "Позволяет использовать огнестрельное оружие. При улучшении уровня владения оружием, меньше шанс промахнуться и выше шанс поставить критический урон.",
            "Активное умение",
            10,   
            20,
            10,
            5
        ],
        [
            "Максимальный вес",
            "Увеличивает максимальный вес, который персонаж способен унести.",
            "Пассивное умение",
            10,
            30,
            0,
            1
        ],
        [
            "Крепость",
            "Увеличивает здоровье персонажа.",
            "Пассивное умение",
            10,
            50,
            15,
            10
        ],
        [
            "Сила",
            "Увеличивает силу персонажа.",
            "Пассивное умение",
            10,
            50,
            15,
            10
        ],
        [
            "Берсерк",
            'Увеличивает урон в ближнем бою +2% за уровень, но снижается при этом навыки "Крепость" на неопределенное количество поинтов (единиц опыта/уровня).',
            "Пассивное умение",
            10,
            35,
            10,
            10
        ],
        [
            "Мастерство крафта",
            "Позволяет создавать более сложные предметы, увеличивая шанс создания предмета на +0.1% за уровень.",
            "Пассивное умение",
            10,
            50,
            25,
            15
        ],
        [
            "Инженер",
            "Позволяет более рационально пользоваться инструментами, а также увеличивает шанс создания предмета на +0.5% за уровень.",
            "Пассивное умение",
            10,
            75,
            25,
            15
        ],
        [
            "Разбор предметов",
            "Позволяет разбирать предметы.",
            "Пассивное умение",
            1,
            0,
            50,
            20
        ],
        [
            "Собиратель",
            "Увеличивает шанс найти более редкий предмет на +0.1% за уровень.",
            "Пассивное умение",
            15,
            50,
            25,
            8
        ],
        [
            "Боевая медицина",
            "Увеличивает восстановление здоровья в безопасной зоне на +0.5% за уровень.",
            "Пассивное умение",
            10,
            25,
            10,
            10
        ],
        [
            "Толстая кожа",
            "Понижает количество получаемой радиации на +1% за уровень.",
            "Пассивное умение",
            10,
            50,
            15,
            10
        ],
        [
            'Меткий выстрел',
            "Повышает шанс нанести критический урон на +0.5% за уровень.",
            "Активное умение",
            10,
            65,
            20,
            15
        ],
        [
            'Ремонт',
            "Дает возможность ремонтировать предметы с прочностью (первый уровень). Далее эффективность ремонта повышается на +1% за уровень.",
            "Пассивное умение",
            10,
            50,
            50,
            15
        ],
        [
            'Контроль',
            'Понижает отдачу на +0.5% за уровень.',
            "Пассивное умение",
            15,
            25,
            10,
            10
        ]
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
    await connection.commit()
    await connection.close()
asyncio.run(run())