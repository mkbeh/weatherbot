# -*- coding: utf-8 -*-
import bcrypt

from src import bot
from src.aiotelegram import types as bot_types


async def is_pwd_valid(password, hash):
    return bcrypt.checkpw(password.encode(), hash)


async def create_reply_markup(buttons_names):
    markup = bot_types.ReplyKeyboardMarkup()
    buttons = [bot_types.KeyboardButton(text) for text in buttons_names]
    await markup.add(*buttons)

    return markup
