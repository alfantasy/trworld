import json # Использование JSON как хранение данных
from aiogram import Bot, Dispatcher # Основной класс бота и главный диспатчер
from aiogram.fsm.storage.memory import MemoryStorage # Хранение состояний до перезапуска бота
from aiogram.client.default import DefaultBotProperties # Базовые опции
from aiogram.enums import ParseMode # Парсирование и форматирование
from utils.database import Database

with open('config.json', 'r') as f:
    config = json.load(f)

bot = Bot(token=config["BOT_TOKEN"], default=DefaultBotProperties(parse_mode=ParseMode.HTML))
storage = MemoryStorage()
dp = Dispatcher(storage=storage)
db = Database()

from handlers import commands, messages

dp.include_router(commands.router)
dp.include_router(messages.router)