from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup

from config import my_themes_link, portfolio_link


def start_kb():
    kb = [
        [
            InlineKeyboardButton(text='Мои темы', url=my_themes_link),
            InlineKeyboardButton(text='Портфолио', url=portfolio_link)
        ],
        [
            InlineKeyboardButton(text='Сделать заказ', callback_data='make_order')
        ]
    ]
    return InlineKeyboardMarkup(inline_keyboard=kb)


def return_kb():
    kb = [
        [
            InlineKeyboardButton(text='Назад', callback_data='start')
        ]
    ]
    return InlineKeyboardMarkup(inline_keyboard=kb)