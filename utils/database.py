import aiosqlite
import os

class Database:
    '''
    Основной класс по работе с базой данных.
    '''
    def __init__(self):
        self.db_name = 'database.db'
        self.connection = None
        self.cursor = None
        with open(self.db_name, 'a'):
            pass

    async def init_base(self):
        self.connection = await aiosqlite.connect(self.db_name)
        self.cursor = await self.connection.cursor()
        await self.cursor.execute("PRAGMA foreign_keys = ON;")
        await self.create_tables()
        await self.create_indexes()

    async def close_base(self):
        await self.connection.commit()
        await self.connection.close()
        
    async def create_tables(self):
        ## Создание таблицы с пользователями ##
        await self.cursor.execute('''CREATE TABLE IF NOT EXISTS users (
                                  id INTEGER PRIMARY KEY AUTOINCREMENT, 
                                  user_id INTEGER,
                                  tg_username TEXT,
                                  nickname TEXT,
                                  level INTEGER,
                                  level_exp INTEGER,
                                  money INTEGER,
                                  donate_money INTEGER,
                                  health INTEGER,
                                  max_health INTEGER,
                                  energy INTEGER,
                                  faction INTEGER,
                                  clan_id INTEGER,
                                  squad_id INTEGER,
                                  quest_current INTEGER,
                                  full_stats TEXT,
                                  current_location INTEGER NOT NULL,
                                  vip INTEGER,
                                  vip_time TEXT,
                                  reg_time DEFAULT CURRENT_TIMESTAMP,
                                  banned INTEGER,
                                  banned_time TEXT,
                                  FOREIGN KEY(clan_id) REFERENCES clans(id) ON DELETE SET NULL,
                                  FOREIGN KEY(squad_id) REFERENCES squads(id) ON DELETE SET NULL,
                                  FOREIGN KEY(current_location) REFERENCES locations(id));''')
        
        ## Создание таблицы с инвентарем ##
        await self.cursor.execute('''CREATE TABLE IF NOT EXISTS inventory_users (
                                  user_id INTEGER,
                                  item_id INTEGER,
                                  quantity INTEGER,
                                  FOREIGN KEY(user_id) REFERENCES users(id),
                                  FOREIGN KEY(item_id) REFERENCES items(id)
                                  );''')
        
        ## Создание таблицы с экипировкой персонажа
        await self.cursor.execute('''CREATE TABLE IF NOT EXISTS equipment_users (
                                  user_id INTEGER NOT NULL,
                                  item_id INTEGER NOT NULL,
                                  slot TEXT,
                                  FOREIGN KEY(user_id) REFERENCES users(id),
                                  FOREIGN KEY(item_id) REFERENCES items(id)
                                  );''')
        
        ## Создание таблицы с предметами на продажу игроком
        await self.cursor.execute('''CREATE TABLE IF NOT EXISTS sell_items_users (
                                  user_id INTEGER,
                                  item_id INTEGER,
                                  quantity INTEGER,
                                  FOREIGN KEY(user_id) REFERENCES users(id),
                                  FOREIGN KEY(item_id) REFERENCES items(id)
                                  );''')
        
        ## Создание таблицы с скиллами пользователей ##
        await self.cursor.execute('''CREATE TABLE IF NOT EXISTS user_skills (
                                  id INTEGER PRIMARY KEY AUTOINCREMENT,
                                  user_id INTEGER,
                                  skill_id INTEGER,
                                  skill_level INTEGER,
                                  FOREIGN KEY(user_id) REFERENCES users(id),
                                  FOREIGN KEY(skill_id) REFERENCES skills(id)
                                  );''')
        
        ## Создание таблицы с навыками ##
        await self.cursor.execute('''CREATE TABLE IF NOT EXISTS skills (
                                  id INTEGER PRIMARY KEY AUTOINCREMENT,
                                  name TEXT,
                                  description TEXT,
                                  type TEXT,
                                  level INTEGER,
                                  exp INTEGER,
                                  price_upgrade INTEGER,
                                  price INTEGER,
                                  required_level INTEGER);''')
        
        ## Создание таблицы с битвами ##
        await self.cursor.execute('''CREATE TABLE IF NOT EXISTS battles(
                                  id INTEGER PRIMARY KEY AUTOINCREMENT,
                                  user_id INTEGER,
                                  enemy_id INTEGER,
                                  enemy_type TEXT,
                                  battle_status TEXT,
                                  start_time DEFAULT CURRENT_TIMESTAMP,
                                  end_time TIMESTAMP,
                                  FOREIGN KEY(user_id) REFERENCES users(id),
                                  FOREIGN KEY(enemy_id) REFERENCES users(id));''')
        
        ## Создание таблицы с кланами ##
        await self.cursor.execute('''CREATE TABLE IF NOT EXISTS clans (
                                  id INTEGER PRIMARY KEY AUTOINCREMENT,
                                  name TEXT,
                                  leader_user_id INTEGER,
                                  clans_exp INTEGER,
                                  money INTEGER,
                                  level INTEGER,
                                  level_exp INTEGER,
                                  quests TEXT,
                                  quest_current INTEGER,
                                  full_stats TEXT,
                                  reg_time DEFAULT CURRENT_TIMESTAMP,
                                  delete_or_banned INTEGER);''')
        
        ## Создание таблицы с участниками клана ##
        await self.cursor.execute('''CREATE TABLE IF NOT EXISTS clan_members (
                                  user_id INTEGER NOT NULL,
                                  clan_id INTEGER NOT NULL,
                                  role TEXT,
                                  FOREIGN KEY(user_id) REFERENCES users(id),
                                  FOREIGN KEY(clan_id) REFERENCES clans(id),
                                  PRIMARY KEY (clan_id, user_id)
                                  );''')
        
        ## Создание таблицы с отрядами ##
        await self.cursor.execute('''CREATE TABLE IF NOT EXISTS squads (
                                  id INTEGER PRIMARY KEY AUTOINCREMENT,
                                  name TEXT,
                                  leader_user_id INTEGER,
                                  clan_id INTEGER,
                                  reg_time DEFAULT CURRENT_TIMESTAMP);''')
        
        ## Создание таблицы с участниками отряда ##
        await self.cursor.execute('''CREATE TABLE IF NOT EXISTS squad_members (
                                  user_id INTEGER NOT NULL,
                                  squad_id INTEGER NOT NULL,
                                  role TEXT,
                                  FOREIGN KEY(user_id) REFERENCES users(id),
                                  FOREIGN KEY(squad_id) REFERENCES squads(id),
                                  PRIMARY KEY (squad_id, user_id)
                                  );''')                
        
        ## Создание таблицы с аукционом ##
        await self.cursor.execute('''CREATE TABLE IF NOT EXISTS sell_place (
                                  id INTEGER PRIMARY KEY AUTOINCREMENT,
                                  items TEXT,
                                  user_id INTEGER);''')
        
        ## Создание таблицы с квестами ##
        await self.cursor.execute('''CREATE TABLE IF NOT EXISTS quests (
                                  id INTEGER PRIMARY KEY AUTOINCREMENT,
                                  name TEXT,
                                  description TEXT,
                                  npc_id INTEGER,
                                  reward TEXT,
                                  reward_exp INTEGER,
                                  reward_money INTEGER,
                                  reward_donate_money INTEGER,
                                  reward_items TEXT,
                                  reward_skills TEXT,
                                  min_level INTEGER,
                                  required_items TEXT,
                                  is_repeat BOOLEAN,
                                  time_limit TEXT,
                                  FOREIGN KEY(npc_id) REFERENCES npc(id));''')
        
        ## Создание таблицы с событиями ##
        await self.cursor.execute('''CREATE TABLE IF NOT EXISTS events (
                                  id INTEGER PRIMARY KEY AUTOINCREMENT,
                                  name TEXT,
                                  description TEXT,
                                  trigger_location INTEGER,
                                  trigger_time TIMESTAMP,
                                  is_active BOOLEAN);''')
        
        ## Создание таблицы с рецептами ##
        await self.cursor.execute('''CREATE TABLE IF NOT EXISTS craft_recipes (
                                  id INTEGER PRIMARY KEY AUTOINCREMENT,
                                  result_item_id INTEGER NOT NULL,
                                  required_skills_id INTEGER,
                                  craft_time INTEGER,
                                  FOREIGN KEY(result_item_id) REFERENCES items(id) ON DELETE CASCADE);''')
        
        ## Создание таблицы с требованиями к рецептам ##
        await self.cursor.execute('''CREATE TABLE IF NOT EXISTS recipe_requirements (
                                  recipe_id INTEGER NOT NULL,
                                  item_id INTEGER NOT NULL,
                                  quantity INTEGER NOT NULL,
                                  FOREIGN KEY(recipe_id) REFERENCES craft_recipes(id) ON DELETE CASCADE,
                                  FOREIGN KEY(item_id) REFERENCES items(id) ON DELETE CASCADE);''')        
        
        ## Создание таблицы с NPC ##
        await self.cursor.execute('''CREATE TABLE IF NOT EXISTS npc (
                                  id INTEGER PRIMARY KEY AUTOINCREMENT,
                                  name TEXT,
                                  description TEXT,
                                  location INTEGER,
                                  items_on_person TEXT,
                                  items_on_sell TEXT,
                                  quests TEXT,
                                  dialogue TEXT,
                                  hostility INTEGER,
                                  health INTEGER);''')
        
        ## Создание таблицы с локациями ## LOCATIONS
        await self.cursor.execute('''CREATE TABLE IF NOT EXISTS locations (
                                  id INTEGER PRIMARY KEY AUTOINCREMENT,
                                  name TEXT,
                                  description TEXT,
                                  loc_to TEXT,
                                  loc_in TEXT,
                                  danger INTEGER,
                                  resources TEXT,
                                  enemies TEXT,
                                  is_hidden BOOLEAN,
                                  level INTEGER,
                                  photo TEXT);''')
        
        ## Создание таблицы с вещами ## ITEMS
        await self.cursor.execute('''CREATE TABLE IF NOT EXISTS items (
                                  id INTEGER PRIMARY KEY AUTOINCREMENT,
                                  name TEXT,
                                  type TEXT,
                                  rarity TEXT,
                                  stats TEXT,
                                  caliber TEXT,
                                  description TEXT,
                                  can_sell BOOLEAN,
                                  can_trade BOOLEAN,
                                  can_craft BOOLEAN);''')

        await self.connection.commit()        

    async def create_indexes(self):
        await self.cursor.execute("CREATE INDEX IF NOT EXISTS idx_users_user_id ON users(user_id)")
        await self.cursor.execute("CREATE INDEX IF NOT EXISTS idx_users_clan_id ON clans(id)")
        await self.cursor.execute("CREATE INDEX IF NOT EXISTS idx_users_squad_id ON squads(id)")
        await self.cursor.execute("CREATE INDEX IF NOT EXISTS idx_users_location_id ON locations(id)")
        await self.cursor.execute("CREATE INDEX IF NOT EXISTS idx_battles_user_id ON battles(user_id)")
        await self.cursor.execute("CREATE INDEX IF NOT EXISTS idx_battles_enemy_id ON battles(enemy_id)")
        await self.cursor.execute("CREATE INDEX IF NOT EXISTS idx_quests_npc_id ON quests(npc_id)")
        await self.cursor.execute("CREATE INDEX IF NOT EXISTS idx_quests_min_level ON quests(min_level)")
        await self.cursor.execute("CREATE INDEX IF NOT EXISTS idx_inventory_user_item ON inventory_users(user_id, item_id)")
        await self.cursor.execute("CREATE INDEX IF NOT EXISTS idx_locations_danger ON locations(danger) WHERE danger > 0")
        await self.connection.commit()
        
    ## Работа с таблицей users ##
    async def register_user(self, user_id: int, tg_username: str, nickname: str):
        await self.cursor.execute("SELECT id FROM users WHERE user_id = ?", (user_id,))
        if await self.cursor.fetchone():
            return False
        
        START_CONFIG = {
            'location': 1,
            'health': 70,
            'max_health': 100,
            'money': 1000,
            'items': [(1, 1), (2, 1)],  # (item_id, quantity)
            'skills': [1, 2]  # skill_ids
        }
        await self.cursor.execute('''
            INSERT INTO users (
                user_id, tg_username, nickname, level, level_exp, money, health,
                max_health, energy, current_location
            ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?);
            ''', (user_id, tg_username, nickname, 1, 0, START_CONFIG['money'], 
            START_CONFIG['health'], START_CONFIG['max_health'], 10, START_CONFIG['location']))

        await self.cursor.execute("SELECT id FROM users WHERE user_id = ?", (user_id,))
        user_db_id = (await self.cursor.fetchone())[0]        

        for item_id, quantity in START_CONFIG['items']:
            print(item_id, quantity)
            await self.cursor.execute('''
                INSERT INTO inventory_users (user_id, item_id, quantity) VALUES (?, ?, ?);
                ''', (user_db_id, item_id, quantity))
        for skill_id in START_CONFIG['skills']:
            await self.cursor.execute('''
                INSERT INTO user_skills (user_id, skill_id, skill_level) VALUES (?, ?, ?);
                ''', (user_db_id, skill_id, 1))
        await self.connection.commit()
        return True
    
    async def get_info_user(self, user_id: int):
        await self.cursor.execute("SELECT * FROM users WHERE user_id = ?", (user_id,))
        data = await self.cursor.fetchone()
        if data:
            return data, True
        else:
            return None, False

    ## Работа с таблицей users ##

    ## Работа с таблицей inventory ##
    async def get_info_item(self, item_id: int):
        await self.cursor.execute("SELECT * FROM items WHERE id = ?", (item_id,))
        return await self.cursor.fetchone()

    async def show_inventory(self, user_id: int):
        fetch_userid_table = await self.cursor.execute("SELECT id FROM users WHERE user_id = ?", (user_id,))
        userid_table = (await fetch_userid_table.fetchone())[0]
        # Получаем предметы из инвентаря
        await self.cursor.execute('''
            SELECT i.id, i.name, i.type, i.rarity, inv.quantity 
            FROM inventory_users inv
            JOIN items i ON inv.item_id = i.id
            WHERE inv.user_id = ?
            ORDER BY i.type, i.name
        ''', (userid_table,))
        
        items = await self.cursor.fetchall()
        
        # Форматируем вывод
        inventory_text = "🎒 Ваш инвентарь:\n"
        if not items:
            inventory_text += "Пусто\n"
        else:
            for item in items:
                print(item)
                ids_item, name, item_type, rarity, quantity = item
                inventory_text += f"├ {name} ({rarity}) - {quantity} шт.\n"
                inventory_text += f"└ Тип: {item_type}\n\n"
        
        return inventory_text, items

    async def show_inventory_page(self, user_id: int, page: int = 1, page_size: int = 5):
        offset = (page - 1) * page_size
        await self.cursor.execute('''
            SELECT i.name, inv.quantity 
            FROM inventory_users inv
            JOIN items i ON inv.item_id = i.id
            WHERE inv.user_id = ?
            LIMIT ? OFFSET ?
        ''', (user_id, page_size, offset))
        
        items = await self.cursor.fetchall()
        
        return items
    ## Работа с таблицей inventory ##


    ## Работа с таблицей locations ##
    async def get_location(self, location_id: int):
        await self.cursor.execute("SELECT * FROM locations WHERE id = ?", (location_id,))
        return await self.cursor.fetchone()
    ## Работа с таблицей locations ##
