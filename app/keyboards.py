from aiogram.types import (ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardButton, InlineKeyboardMarkup)
from aiogram.utils.keyboard import InlineKeyboardBuilder

main = ReplyKeyboardMarkup(
    keyboard=[
    [KeyboardButton(text="🔐 Купить VPN")],
    [KeyboardButton(text="ℹ️ Информация"),
     KeyboardButton(text="💬 Отзывы"), KeyboardButton(text="👤 Мой профиль"), KeyboardButton(text="⚙️ Поддержка")]
],resize_keyboard=True,
input_field_placeholder='Выберите пункт меню'
)

resize_keyboard=True,
input_field_placeholder='Выберите пункт меню'

info_menu = ReplyKeyboardMarkup( keyboard=[
    [KeyboardButton(text="🌍 О сервисе SpeedVPN"), KeyboardButton(text="🧠 Как подключиться")],
    [KeyboardButton(text="⬅️ Назад")]
],resize_keyboard=True,
input_field_placeholder='Выберите пункт меню'
)

help_menu = ReplyKeyboardMarkup( keyboard=[
    [KeyboardButton(text="👨‍💻 Написать в поддержку")],
    [KeyboardButton(text="⬅️ Назад")]
],resize_keyboard=True,
input_field_placeholder='Выберите пункт меню'
)

review_menu = ReplyKeyboardMarkup(
    keyboard=[
        [KeyboardButton(text="📝 Оставить отзыв"), KeyboardButton(text="⭐ Посмотреть отзывы")],
        [KeyboardButton(text="⬅️ Назад")]
    ],resize_keyboard=True,
input_field_placeholder='Выберите пункт меню'
)

buy_menu = ReplyKeyboardMarkup(
    keyboard=[
        [KeyboardButton(text="💳 Оплатить VPN"), KeyboardButton(text="📤 Отправить скрин оплаты")],
        [KeyboardButton(text="⬅️ Назад")]
    ],resize_keyboard=True,
input_field_placeholder='Выберите пункт меню'

)





