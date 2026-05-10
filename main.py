import asyncio
import logging
import sys

from aiogram import Bot, Dispatcher, BaseMiddleware
from aiogram.types import Message, CallbackQuery

import config
from handlers import general, media, system, file_manager

logging.basicConfig(level=logging.INFO)

class AdminMiddleware(BaseMiddleware):
    async def __call__(self, handler, event, data):
        user = data.get("event_from_user")
        if not user:
            print("DEBUG: Не удалось получить пользователя из события.")
            return

        print(f"DEBUG: Получен запрос от пользователя {user.id}. Ожидается админ {config.ADMIN_ID}.")
        
        if user.id == config.ADMIN_ID:
            print("DEBUG: Доступ разрешен. Передаем обработчику.")
            return await handler(event, data)
        else:
            print("DEBUG: Доступ запрещен!")
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

    print("Бот успешно запущен! Нажмите Ctrl+C для остановки.")
    
    try:
        await bot.delete_webhook(drop_pending_updates=True)
        await dp.start_polling(bot)
    except Exception as e:
        print(f"Ошибка при запуске бота: {e}")

if __name__ == "__main__":
    try:
        asyncio.run(main())
    except (KeyboardInterrupt, SystemExit):
        print("Бот остановлен.")
