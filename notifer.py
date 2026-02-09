import asyncio
import logging
from datetime import datetime, timedelta
from aiogram import Bot
from config import TOKEN
import database as db

logger = logging.getLogger(__name__)

bot = Bot(token=TOKEN)

async def daily_subscription_check():
    """Проверяет окончание подписок и отправляет уведомления."""
    while True:
        now = datetime.utcnow()
        tomorrow = now + timedelta(days=1)

        with db.Session() as session:
            users = session.query(db.User).filter(
                db.User.subscription_end != None,
                db.User.subscription_end.between(now, tomorrow)
            ).all()

            for user in users:
                try:
                    logger.info(f"🔔 Уведомление пользователю {user.telegram_id} о скором окончании подписки")
                    await bot.send_message(
                        chat_id=user.telegram_id,
                        text=(
                            "⏳ *Напоминание!* Ваша подписка SpeedVPN заканчивается завтра.\n\n"
                            "Продлите её, чтобы не потерять доступ к VPN 🔐\n"
                            "Нажмите кнопку ниже 👇"
                        ),
                        parse_mode="Markdown"
                    )
                except Exception as e:
                    logger.error(f"Не удалось отправить уведомление {user.telegram_id}: {e}")

        # ждём до следующей проверки
        await asyncio.sleep(24 * 60 * 60)

async def start_notifier():
    """Запускает планировщик проверки подписок"""
    logger.info("🕒 Проверка подписок запущена (ежедневно)")
    asyncio.create_task(daily_subscription_check())
