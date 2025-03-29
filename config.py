import json # Использование JSON как хранение данных
from aiogram import Bot, Dispatcher # Основной класс бота и главный диспатчер
from aiogram.fsm.storage.memory import MemoryStorage # Хранение состояний до перезапуска бота
from aiogram.client.default import DefaultBotProperties # Базовые опции
from aiogram.enums import ParseMode # Парсирование и форматирование
from utils.database import Database # Использование базы данных

## Загрузка конфигураций ## 
with open('config.json', 'r') as f:
    config = json.load(f)

## Инициализация класса бота
bot = Bot(token=config["BOT_TOKEN"], default=DefaultBotProperties(parse_mode=ParseMode.HTML))

## Инициализация хранения состояний
storage = MemoryStorage()

## Инициализация главного диспатчера
dp = Dispatcher(storage=storage)

## Инициализация базы данных
db = Database()

## Инициализация хэндлеров
from handlers import commands, messages, game

## Инициализация роутеров
dp.include_router(commands.router)
dp.include_router(messages.router)
dp.include_router(game.router)