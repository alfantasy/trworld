import asyncio
from config import bot, dp, db

async def on_shutdown(dispatcher):
    await db.close_base()

async def main():
    await bot.delete_webhook(drop_pending_updates=True)
    dp.shutdown.register(on_shutdown)
    await db.init_base()
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())