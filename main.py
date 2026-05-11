import asyncio
import logging
import sys

from aiogram import Bot, Dispatcher, BaseMiddleware
from aiogram.types import Message, CallbackQuery

import config
from handlers import general, media, system, file_manager, clipboard

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    handlers=[
        logging.FileHandler("bot.log", encoding="utf-8"),
        logging.StreamHandler(sys.stdout)
    ]
)

class AdminMiddleware(BaseMiddleware):
    async def __call__(self, handler, event, data):
        user = data.get("event_from_user")
        if not user:
            logging.debug("DEBUG: Не удалось получить пользователя из события.")
            return

        logging.info(f"Получен запрос от пользователя {user.id}. Ожидается админ {config.ADMIN_ID}.")
        
        if user.id == config.ADMIN_ID:
            logging.debug("Доступ разрешен. Передаем обработчику.")
            return await handler(event, data)
        else:
            logging.warning(f"Доступ запрещен для пользователя {user.id}!")
            if isinstance(event, Message):
                await event.answer("Отказано в доступе. Этот бот является приватным.")
            elif isinstance(event, CallbackQuery):
                await event.answer("Отказано в доступе.", show_alert=True)
            return

async def main():
    bot = Bot(token=config.BOT_TOKEN)
    dp = Dispatcher()

    admin_middleware = AdminMiddleware()
    dp.message.middleware(admin_middleware)
    dp.callback_query.middleware(admin_middleware)

    dp.include_router(general.router)
    dp.include_router(media.router)
    dp.include_router(system.router)
    dp.include_router(file_manager.router)
    dp.include_router(clipboard.router)

    logging.info("Бот успешно запущен!")
    
    try:
        await bot.delete_webhook(drop_pending_updates=True)
        await dp.start_polling(bot)
    except Exception as e:
        logging.error(f"Ошибка при запуске бота: {e}")

if __name__ == "__main__":
    try:
        asyncio.run(main())
    except (KeyboardInterrupt, SystemExit):
        logging.info("Бот остановлен.")
