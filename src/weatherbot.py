# -*- coding: utf-8 -*-
import re

import aiohttp
import bcrypt

from starlette.applications import Starlette
from starlette.routing import Route

from starlette.responses import JSONResponse
from starlette.background import BackgroundTask

from aiotelegram import GramBot, types 
from sendmail import  send_confirmation_mail, confirm_token
from secret import TG_API_TOKEN, BASE_URL


users = {}
steps = {}

bot = GramBot(TG_API_TOKEN)


class User:
    def __init__(self, email, password=None, city=None):
        self.email      = email
        self._password  = password
        self.salt       = None
        self.city       = city
        self.is_login   = False

    @property
    def password(self):
        return self._password

    @password.setter
    def password(self, password):
        self.salt = bcrypt.gensalt()
        self._password = bcrypt.hashpw(password.encode(), self.salt)

    def __str__(self):
        return f'email:{self.email}, pwd:{self._password}, salt:{self.salt}, city:{self.city}'


async def process_city(chat_id, city):
    # TODO: validate city.
    
    if city:
        user = users[chat_id]
        user.city = city
        
        await send_confirmation_mail(user.email, chat_id)
        await bot.send_message(chat_id, 'На почту выслано письмо для активации вашего почтового адреса. После подтверждения вы сможете войти в личный кабинет.')
    else:
        await bot.send_message(chat_id, 'Некорректный город. Введите заново.')
        steps[chat_id] = process_city


async def process_password(chat_id, password):
    if 6 <= len(password) <= 10:
        user = users[chat_id]
        user.password = password

        steps[chat_id] = process_city
        await bot.send_message(chat_id, 'Введите город.')
    else:
        await bot.send_message(chat_id, 'Некорректный пароль. Введите заново.')
        steps[chat_id] = process_password


async def process_email(chat_id, email):
    email_pattern = re.compile(r'[^@]+@[^@]+\.[^@]+')
    if re.match(email_pattern, email):
        users[chat_id] = User(email)
        steps[chat_id] = process_password
        await bot.send_message(chat_id, 'Введите пароль. (Длина пароля должна быть от 6 до 10 символов)')
    else:
        await bot.send_message(chat_id, 'Некорректный email. Введите заново.')
        steps[chat_id] = process_email


async def start(chat_id, message):
    await bot.send_message(chat_id, 'Здравствуйте, зарегистрируйтесь и узнавайте погоду в вашем городе.')
    await bot.send_message(chat_id, 'Введите email')
    steps[chat_id] = process_email


async def personal_area_process(chat_id, message):
    pass


async def email_confirmation(request):
    token = request.path_params['token']
    try:
        email, chat_id = await confirm_token(token)
    except:
        # NOTE: need to store chat_id of user temporary in key-value storage
        #       to send error message to user in Telegram.
        return JSONResponse({'ok': False})
    else:
        # TODO: next step: write user data to db 

        await bot.send_message(chat_id, f'Email {email} успешно подтвержден.')

        markup = types.ReplyKeyboardMarkup()
        buttons = [types.KeyboardButton(text) for text in ('Погода сегодня', 'Погода на неделю', 'Выйти')]
        await markup.add(*buttons)

        await bot.send_message(chat_id, 'Доступ в личный кабинет теперь открыт.', markup)
        steps[chat_id] = personal_area_process

        user = users[chat_id]
        user.is_login = True

        return JSONResponse({'status': 'Активация почты прошла успешно'})


async def receive_update(request):
    if request.method == 'POST':
        data = await request.json()
        text = data['message']['text']
        chat_id = data['message']['chat']['id']

        if text == '/start':
            next_step_handler = start
        else:
            try:
                next_step_handler = steps[chat_id]
            except KeyError:
                next_step_handler = start

        await next_step_handler(chat_id, text)

    return JSONResponse({'ok': True})


routes = [
    Route('/', endpoint=receive_update, methods=['GET', 'POST']),
    Route('/confirm/{token}', endpoint=email_confirmation),
]


bot.delete_webhook()
bot.set_webhook(BASE_URL)

app = Starlette(routes=routes)  
