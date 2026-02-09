import asyncio
import logging
from datetime import datetime, timedelta, timezone
from aiogram import Bot, Dispatcher

from config import TOKEN, ADMIN_USERNAME, ADMIN_ID
from app import handlers
from app.handlers import router
import database
from notifer import start_notifier 

# Настройка логов
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
)

bot = Bot(token=TOKEN)
dp = Dispatcher()


async def schedule_notifications():
    """
    Фоновая задача — проверяет подписки каждый день в 10:00 UTC.
    """
    while True:
        now = datetime.now(timezone.utc)
        target_time = now.replace(hour=10, minute=0, second=0, microsecond=0)
        if now > target_time:
            target_time += timedelta(days=1)

        wait_time = (target_time - now).total_seconds()
        logging.info(f"🕒 Следующая проверка подписок через {wait_time / 3600:.1f} часов")
        await asyncio.sleep(wait_time)

        try:
            logging.info("⏰ Запускаем проверку подписок...")
            await notify_expiring_users()
        except Exception as e:
            logging.error(f"Ошибка в проверке подписок: {e}")


async def run_polling():
    """
    Основной цикл polling с автоматическим перезапуском при сбое.
    """
    while True:
        try:
            logging.info("🚀 Запуск polling...")
            await dp.start_polling(bot)
        except Exception as e:
            logging.error(f"Polling crashed: {e}")
            logging.info("⏳ Перезапуск через 5 секунд...")
            await asyncio.sleep(5)


async def main():
    # Инициализация базы данных
    database.init_db()

    # Подключаем роутеры
    dp.include_router(router)

    # Запускаем фоновую задачу проверки подписок
    asyncio.create_task(schedule_notifications())

    # Разрешаем ADMIN_ID
    try:
        await handlers.resolve_admin_id(bot)
    except Exception as e:
        logging.error(f"resolve_admin_id error: {e}")

    await start_notifier()

    # Запускаем polling
    await run_polling()


if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        logging.info("🚪 Бот остановлен вручную.")
