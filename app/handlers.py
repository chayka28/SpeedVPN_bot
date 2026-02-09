import asyncio
from aiogram import F, Router
from aiogram.filters import CommandStart, Command
from aiogram.types import (
    Message,
    CallbackQuery,
    InlineKeyboardMarkup,
    InlineKeyboardButton,
)
import app.keyboards as kb
import database as db
import functions as fx
from config import ADMIN_USERNAME, ADMIN_ID
from datetime import datetime, timedelta
from aiogram.utils.text_decorations import markdown_decoration as md

router = Router()


# =======================
# 📍 Базовые команды
# =======================

@router.message(CommandStart())
async def cmd_start(message: Message):
    db.UserHelper.get_or_create(
        telegram_id=message.from_user.id,
        full_name=message.from_user.full_name,
        username=message.from_user.username
    )
    await message.answer(
        f"""🔐 Привет, {message.from_user.first_name}!

Ты попал в официальный бот VPN-сервиса **SpeedVPN** — надёжного способа оставаться онлайн без ограничений.

💡 Возможности:
• Быстрые сервера в Европе (Рига, Латвия)
• Без потери скорости
• Доступ к YouTube, TikTok, Instagram, Telegram и другим сервисам
• Простое подключение и моментальная активация

👇 Выберите действие в меню, чтобы начать.""",
        reply_markup=kb.main,
        parse_mode="Markdown"
    )


@router.message(Command('help'))
async def get_help(message: Message):
    await message.answer("Это команда /help")


@router.message(F.text == "инструкция")
async def how(message: Message):
    await message.answer('''Чтобы начать пользоваться SpeedVPN, выполните всего несколько шагов:

1️⃣ Скопируйте ссылку, которую вы получили после покупки.  
2️⃣ Установите приложение V2Ray Tun:  
   - Android: https://play.google.com/store/apps/details?id=com.v2raytun.android  
   - iOS: https://apps.apple.com/ru/app/v2raytun/id6476628951  
3️⃣ Откройте приложение и нажмите ➕ в правом верхнем углу.  
4️⃣ Выберите "Добавить профиль из буфера обмена".  
5️⃣ Подключайтесь и пользуйтесь безопасным интернетом!  

💡 Всё просто, быстро и надёжно.
''')


# =======================
# 💳 Оплата
# =======================

@router.message(F.text == "🔐 Купить VPN")
async def buy(message: Message):
    await message.answer(
        '''🚀 Вы готовы к безопасному и свободному интернету с SpeedVPN?

💳 Стоимость: 100 ₽ / месяц

Что вы получите после покупки:
• Ссылку для подключения к VPN  
• Доступ к серверам в Европе (Рига, Латвия)  
• Возможность использовать TikTok, YouTube, Instagram, Telegram и WhatsApp  
• Защиту данных и приватность соединения
''',
        reply_markup=kb.buy_menu
    )


@router.message(F.text == "💳 Оплатить VPN")
async def pay(message: Message):
    await message.answer(
        '''💳 Отправьте перевод по реквизитам 2200701901781135 (т.банк)
После оплаты загрузите скриншот сюда — администратор подтвердит, и будет оформлена подписка на 30 дней ✅'''
    )


@router.message(F.text == "📤 Отправить скрин оплаты")
async def send_screen(message: Message):
    await message.answer(
        "Загрузите скриншот с подтверждением оплаты. После проверки администратором вам будет выдана ссылка."
    )


# =======================
# ℹ️ Информация
# =======================

@router.message(F.text == "ℹ️ Информация")
async def info(message: Message):
    await message.answer(
        "🔍 Узнайте всё о SpeedVPN: быстрые сервера, безопасность и доступ к любимым сервисам! 🌍🔐",
        reply_markup=kb.info_menu
    )


@router.message(F.text == "🌍 О сервисе SpeedVPN")
async def about(message: Message):
    await message.answer('''🔐 SpeedVPN — это быстрый и надёжный доступ к интернету без ограничений.

🌍 Серверы в Европе (Рига, Латвия) обеспечивают стабильное соединение без потери скорости.

📱 С SpeedVPN вы можете использовать TikTok, YouTube, Instagram, Telegram, WhatsApp и другие приложения без блокировок.

🚀 Просто подключайтесь и пользуйтесь безопасным интернетом!''', reply_markup=kb.info_menu)


@router.message(F.text == "🧠 Как подключиться")
async def how_connect(message: Message):
    await message.answer('''Чтобы начать пользоваться SpeedVPN:

1️⃣ Скопируйте ссылку, которую вы получили после покупки.  
2️⃣ Установите приложение V2Ray Tun:  
   - Android: https://play.google.com/store/apps/details?id=com.v2raytun.android  
   - iOS: https://apps.apple.com/ru/app/v2raytun/id6476628951  
3️⃣ Откройте приложение и нажмите ➕ в правом верхнем углу.  
4️⃣ Выберите "Добавить профиль из буфера обмена".  
5️⃣ Подключайтесь и пользуйтесь безопасным интернетом!
''', reply_markup=kb.info_menu)


# =======================
# 💬 Отзывы
# =======================

@router.message(F.text == "💬 Отзывы")
async def review(message: Message):
    await message.answer(
        "💬 Реальные отзывы наших клиентов — честно и открыто 🚀", reply_markup=kb.review_menu
    )


@router.message(F.text == "📝 Оставить отзыв")
async def send_review(message: Message):
    await message.answer(
        '''Чтобы оставить отзыв, перейдите по ссылке:  
📩 https://t.me/anonaskbot?start=kbeu3ylc''',
        reply_markup=kb.review_menu
    )


@router.message(F.text == "⭐ Посмотреть отзывы")
async def look_review(message: Message):
    await message.answer(
        "⭐ Отзывы доступны в канале:\nhttps://t.me/review_SpeedVPN",
        reply_markup=kb.review_menu
    )


# =======================
# 👤 Мой профиль
# =======================

@router.message(F.text == "👤 Мой профиль")
async def my_profile(message: Message):
    """Показывает информацию о пользователе."""
    user = db.UserHelper.get_or_create(
        telegram_id=message.from_user.id,
        full_name=message.from_user.full_name,
        username=message.from_user.username
    )

    now = datetime.utcnow()
    is_active = user.subscription_end and user.subscription_end > now
    reg_date = user.registration_date.strftime("%d.%m.%Y")
    exp_date = user.subscription_end.strftime("%d.%m.%Y") if user.subscription_end else "—"

    session = db.Session()
    tx = session.query(db.Transaction).filter_by(
        user_telegram_id=user.telegram_id, status="confirmed"
    ).order_by(db.Transaction.updated_at.desc()).first()

    profile_link = None
    if tx and tx.profile_id:
        profile = session.query(db.StaticProfile).filter_by(id=tx.profile_id).first()
        if profile:
            profile_link = profile.vless_url
    session.close()

    text = (
        f"👤 *Ваш профиль SpeedVPN*\n\n"
        f"📅 Дата регистрации: *{reg_date}*\n"
        f"⏳ Подписка до: *{exp_date}*\n"
        f"📌 Статус: {'🟢 Активна' if is_active else '🔴 Не активна'}\n\n"
    )

    if profile_link:
        text += f"🔗 Ваша ссылка для подключения:\n```\n{profile_link}\n```"

    kb_profile = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="🔁 Продлить подписку", callback_data="renew_subscription")],
        [InlineKeyboardButton(text="⬅️ Назад", callback_data="back_to_main")]
    ])

    await message.answer(text, reply_markup=kb_profile, parse_mode="Markdown")


@router.callback_query(F.data == "renew_subscription")
async def cb_renew_subscription(query: CallbackQuery):
    await query.answer()
    await query.message.answer(
        "💳 Чтобы продлить подписку, отправьте 100₽ на реквизиты: *2200701901781135 (т.банк)*\n\n"
        "После оплаты загрузите скриншот сюда — администратор подтвердит, и подписка продлится ещё на 30 дней ✅",
        parse_mode="Markdown",
        reply_markup=kb.buy_menu
    )


@router.callback_query(F.data == "back_to_main")
async def cb_back_to_main(query: CallbackQuery):
    await query.answer()
    await query.message.answer("Вы вернулись в главное меню 👇", reply_markup=kb.main)


# =======================
# ⚙️ Поддержка
# =======================

@router.message(F.text == "⚙️ Поддержка")
async def help(message: Message):
    await message.answer(
        "Если у вас возникли вопросы, напишите администратору: @SpeedVPN_help",
        reply_markup=kb.main
    )


@router.message(F.text == "⬅️ Назад")
async def back_to_main(message: Message):
    await message.answer("Вы вернулись в главное меню 👇", reply_markup=kb.main)


# =======================
# 💰 Обработка оплаты
# =======================

async def resolve_admin_id(bot):
    global ADMIN_ID
    try:
        if ADMIN_ID == 0 and ADMIN_USERNAME:
            chat = await bot.get_chat(ADMIN_USERNAME)
            ADMIN_ID = chat.id
    except Exception as e:
        print("Не удалось разрешить ADMIN_ID:", e)


@router.message(lambda message: message.photo and not message.from_user.is_bot)
async def handle_payment_screenshot(message: Message):
    user = message.from_user
    photo = message.photo[-1]
    file_id = photo.file_id
    tx = db.TransactionHelper.create_pending(user.id, user.full_name or user.username, file_id)

    await message.answer("Ожидайте подтверждения администратора 🙌")

    try:
        bot = message.bot
        await resolve_admin_id(bot)

        kb_admin = InlineKeyboardMarkup(inline_keyboard=[
            [InlineKeyboardButton(text="✅ Подтвердить", callback_data=f"confirm_tx:{tx.id}")],
            [InlineKeyboardButton(text="❌ Отклонить", callback_data=f"reject_tx:{tx.id}")]
        ])

        await bot.send_photo(
            chat_id=ADMIN_ID,
            photo=file_id,
            caption=f'💰 Платёж от @{user.username or user.full_name} (ID {user.id})\nTX id: {tx.id}',
            reply_markup=kb_admin
        )
    except Exception as e:
        print("Не удалось отправить админу:", e)
        await message.answer(f"Не удалось уведомить администратора. Напишите @{ADMIN_USERNAME}")

@router.message(Command("users"))
async def list_users(message: Message):
    """Показывает список пользователей администратору."""
    if message.from_user.username != ADMIN_USERNAME:
        await message.answer("❌ У вас нет прав для этой команды.")
        return

    session = db.Session()
    users = session.query(db.User).all()
    session.close()

    if not users:
        await message.answer("📭 В базе пока нет пользователей.")
        return

    text = "📋 *Список пользователей SpeedVPN:*\n\n"
    for u in users:
        sub_status = (
            f"🟢 Активна до {u.subscription_end.strftime('%d.%m.%Y')}"
            if u.subscription_end and u.subscription_end > datetime.utcnow()
            else "🔴 Не активна"
        )

        full_name = md.quote(u.full_name or "—")
        username = md.quote(u.username or "—")
        telegram_id = md.quote(str(u.telegram_id))

        text += (
            f"👤 *{full_name}* (@{username})\n"
            f"ID: `{telegram_id}`\n"
            f"{sub_status}\n\n"
        )

    await message.answer(text, parse_mode="MarkdownV2")



# =======================
# ✅ Подтверждение / ❌ Отклонение
# =======================

@router.callback_query(lambda c: c.data and c.data.startswith("confirm_tx:"))
async def cb_confirm_tx(query: CallbackQuery):
    await query.answer()
    tx_id = int(query.data.split(":")[1])
    tx = db.TransactionHelper.get_by_id(tx_id)
    if not tx:
        await query.message.edit_caption("❌ Транзакция не найдена.")
        return

    bot = query.bot

    try:
        expiry_time = datetime.utcnow() + timedelta(days=30)
        profile = await fx.create_profile_for_user(tx.user_telegram_id, tx.id, expiry_days=30)
        db.TransactionHelper.mark_confirmed(tx.id, profile_id=profile.get("id"))
        
        with db.Session() as session:
            user = session.query(db.User).filter_by(telegram_id=tx.user_telegram_id).first()
            if user:
                if user.subscription_end and user.subscription_end > datetime.utcnow():
                    user.subscription_end += timedelta(days=30)
                else:
                    user.subscription_end = datetime.utcnow() + timedelta(days=30)
                session.commit()

        await bot.send_message(
            chat_id=tx.user_telegram_id,
            text=(
                f"✅ *Оплата подтверждена!* Ваша подписка активна до *{expiry_time.strftime('%d.%m.%Y')}*\n\n"
                '''1️⃣ Скопируйте ссылку, которую вы получили после покупки. 
2️⃣ Установите приложение V2Ray Tun:  
- Android: https://play.google.com/store/apps/details?id=com.v2raytun.android  
- iOS: https://apps.apple.com/ru/app/v2raytun/id6476628951  
3️⃣ Откройте приложение и нажмите ➕ в правом верхнем углу.  
4️⃣ Выберите "Добавить профиль из буфера обмена".  
5️⃣ Подключайтесь и пользуйтесь безопасным интернетом!'''
            ),
            parse_mode="Markdown"
        )

        await bot.send_message(
            chat_id=tx.user_telegram_id,
            text=f"```\n{profile.get('link')}\n```",
            parse_mode="Markdown"
        )

        await query.message.edit_caption((query.message.caption or "") + "\n\n✅ Подтверждена")

    except Exception as e:
        print("Ошибка при создании профиля:", e)
        await query.message.reply(f"Ошибка при создании профиля: {e}")


@router.callback_query(lambda c: c.data and c.data.startswith("reject_tx:"))
async def cb_reject_tx(query: CallbackQuery):
    await query.answer()
    tx_id = int(query.data.split(":")[1])
    tx = db.TransactionHelper.get_by_id(tx_id)
    if not tx:
        await query.message.edit_caption("❌ Транзакция не найдена.")
        return

    db.TransactionHelper.mark_rejected(tx.id)
    await query.bot.send_message(
        chat_id=tx.user_telegram_id,
        text=f"❌ Ваш платёж отклонён. Пожалуйста, обратитесь к администратору: @{ADMIN_USERNAME}"
    )
    await query.message.edit_caption((query.message.caption or '') + "\n\n❌ Отклонена")
