# -*- coding: utf-8 -*-
import re

import aiohttp
import bcrypt

from starlette.applications import Starlette
from starlette.routing import Route

from starlette.responses import JSONResponse
from starlette.background import BackgroundTask

from src import users, steps, next_step_handler, bot
from src import sendmail
from src.aiotelegram import types as bot_types
from src.secret import TG_API_TOKEN, BASE_URL


async def email_confirmation(request):
    token = request.path_params['token']
    try:
        email, chat_id = await sendmail.confirm_token(token)
    except:
        # NOTE: need to send error to user into Telegram.
        return JSONResponse({'ok': False})
    else:
        # TODO: next step: write user data to db 

        await bot.send_message(chat_id, f'Email {email} успешно подтвержден.')

        markup = bot_types.ReplyKeyboardMarkup()
        buttons = [bot_types.KeyboardButton(text) for text in ('Погода сегодня', 'Погода на неделю', 'Выйти')]
        await markup.add(*buttons)

        await bot.send_message(chat_id, 'Доступ в личный кабинет теперь открыт.', markup)
        next_step_handler[chat_id] = steps.personal_area_process

        user = users[int(chat_id)]
        user.is_login = True

        return JSONResponse({'status': 'Активация почты прошла успешно'})


async def receive_update(request):
    if request.method == 'POST':
        data = await request.json()
        text = data['message']['text']
        chat_id = data['message']['chat']['id']

        if text == '/start':
            handler = steps.start
        else:
            try:
                handler = next_step_handler[chat_id]
            except KeyError:
                handler = steps.start

        await handler(chat_id, text)

    return JSONResponse({'ok': True})


routes = [
    Route('/', endpoint=receive_update, methods=['GET', 'POST']),
    Route('/confirm/{token}', endpoint=email_confirmation),
]


bot.delete_webhook()
bot.set_webhook(BASE_URL)

app = Starlette(routes=routes)  
