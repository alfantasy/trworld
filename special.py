import aiosqlite
import asyncio
import json
stats_for_weapon = {"damage": 1, "health": 10, "energy": 0.01, "speed": 0.5}
async def run():
    connection = await aiosqlite.connect('database.db')
    cursor = await connection.cursor()
    # await cursor.execute('''INSERT OR IGNORE INTO locations 
    #                     (id, name, description, danger, loc_to, 
    #                     loc_in, resources, enemies, is_hidden, level, photo) 
    #                     VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?);''', 
    #                     (1, 'Берег', 'Берег', 0, 'Улица Красная', 
    #                     'Улица Красная', 'Никаких', 'Нет', False, 1, 'photo'))
    await cursor.execute('DROP TABLE IF EXISTS inventory_users;')
    await cursor.execute('DROP TABLE IF EXISTS user_skills;')
    await cursor.execute('DROP TABLE IF EXISTS users;')
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
    #await cursor.execute('UPDATE locations SET description = ? WHERE id = 1;', (desc_loc,))
    # await cursor.execute('''INSERT OR IGNORE INTO items
    #                      (id, name, type, rarity, stats, description, can_sell, can_trade)
    #                      VALUES (?, ?, ?, ?, ?, ?, ?, ?);''',
    #                      (2, "Старый ржавый нож", 'Оружие', 'Низкий', json.dumps(stats_for_weapon), 'Старый ржавый нож, доставшийся случайно при непредвиденных обстоятельствах.', False, False))    
    await connection.commit()
    await connection.close()
asyncio.run(run())