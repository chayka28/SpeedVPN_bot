import asyncio
from aiogram import Router
from aiogram.filters import Command
from aiogram.types import Message, CallbackQuery, InlineKeyboardMarkup, InlineKeyboardButton
import database as db
import functions as fx
from config import ADMIN_USERNAME, ADMIN_ID

router = Router()

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
    await message.answer("Ваш скриншот получен. Ожидайте подтверждения админа.")

    try:
        bot = message.bot
        await resolve_admin_id(bot)
        admin_chat = ADMIN_ID if ADMIN_ID != 0 else ADMIN_USERNAME
        kb = InlineKeyboardMarkup(inline_keyboard=[
            [InlineKeyboardButton(text='✅ Подтвердить', callback_data=f'confirm_tx:{tx.id}')],
            [InlineKeyboardButton(text='❌ Отклонить', callback_data=f'reject_tx:{tx.id}')]
        ])
        await bot.send_photo(chat_id=admin_chat, photo=file_id, caption=f'Платеж от @{user.username} ({user.id}). TX id: {tx.id}', reply_markup=kb)
    except Exception as e:
        print('Не удалось отправить админу:', e)
        await message.answer('Не удалось отправить уведомление админу. Сообщите, пожалуйста, @' + ADMIN_USERNAME)

@router.callback_query(lambda c: c.data and c.data.startswith('confirm_tx:'))
async def cb_confirm_tx(query: CallbackQuery):
    await query.answer()
    tx_id = int(query.data.split(':')[1])
    tx = db.TransactionHelper.get_by_id(tx_id)
    if not tx:
        await query.message.edit_caption('Транзакция не найдена.')
        return
    try:
        profile = await fx.create_profile_for_user(tx.user_telegram_id, tx.id)
        db.TransactionHelper.mark_confirmed(tx.id, profile_id=profile.get('id') if isinstance(profile, dict) else None)
        bot = query.bot
        await bot.send_message(chat_id=tx.user_telegram_id, text=f'Оплата подтверждена. Ваша ссылка: {profile.get("link") if isinstance(profile, dict) else "ссылка недоступна"}')
        await query.message.edit_caption((query.message.caption or '') + '\\n\\n✅ Подтверждена')
    except Exception as e:
        print('Ошибка при создании профиля:', e)
        await query.message.reply('Ошибка при создании профиля: ' + str(e))

@router.callback_query(lambda c: c.data and c.data.startswith('reject_tx:'))
async def cb_reject_tx(query: CallbackQuery):
    await query.answer()
    tx_id = int(query.data.split(':')[1])
    tx = db.TransactionHelper.get_by_id(tx_id)
    if not tx:
        await query.message.edit_caption('Транзакция не найдена.')
        return
    db.TransactionHelper.mark_rejected(tx.id)
    bot = query.bot
    await bot.send_message(chat_id=tx.user_telegram_id, text=f'Ваш платеж отклонён. Пожалуйста, обратитесь к администратору: @{ADMIN_USERNAME}')
    await query.message.edit_caption((query.message.caption or '') + '\\n\\n❌ Отклонена')
