# -*- coding: utf-8 -*-
import re

import aiohttp
import bcrypt

from starlette.applications import Starlette
from starlette.routing import Route

from starlette.responses import JSONResponse
from starlette.background import BackgroundTask

from aiotelegram import gram
from sendmail import  send_confirmation_mail, confirm_token
from secret import TG_API_TOKEN, BASE_URL


users = {}
steps = {}


class User:
    def __init__(self, email, password=None, city=None):
        self.email      = email
        self._password  = password
        self.salt       = None
        self.city       = city

    @property
    def password(self):
        return self._password

    @password.setter
    def password(self, password):
        self.salt = bcrypt.gensalt()
        self._password = bcrypt.hashpw(password.encode(), self.salt)

    def __str__(self):
        return f'email:{self.email}, pwd:{self._password}, salt:{self.salt}, city:{self.city}'


async def make_request(url, data):
    async with aiohttp.ClientSession() as session:
        async with session.post(url, data=data) as resp:
            pass


async def send_message(chat_id, text):
    method = "sendMessage"
    url = f"https://api.telegram.org/bot{TG_API_TOKEN}/{method}"
    data = {"chat_id": chat_id, "text": text}
    await make_request(url, data)


async def process_city(chat_id, city):
    # TODO: validate city.
    
    if city:
        user = users[chat_id]
        user.city = city
        
        await send_confirmation_mail(user.email, chat_id)
        await send_message(chat_id, 'На почту выслано письмо для активации вашего почтового адреса. После подтверждения вы сможете войти в личный кабинет.')
        print(user)
    else:
        await send_message(chat_id, 'Некорректный город. Введите заново.')
        steps[chat_id] = process_city


async def process_password(chat_id, password):
    if 6 <= len(password) <= 10:
        user = users[chat_id]
        user.password = password

        steps[chat_id] = process_city
        await send_message(chat_id, 'Введите город.')
    else:
        await send_message(chat_id, 'Некорректный пароль. Введите заново.')
        steps[chat_id] = process_password


async def process_email(chat_id, email):
    email_pattern = re.compile(r'[^@]+@[^@]+\.[^@]+')
    if re.match(email_pattern, email):
        users[chat_id] = User(email)
        steps[chat_id] = process_password
        await send_message(chat_id, 'Введите пароль. (Длина пароля должна быть от 6 до 10 символов)')
    else:
        await send_message(chat_id, 'Некорректный email. Введите заново.')
        steps[chat_id] = process_email


async def start(chat_id, message):
    await send_message(chat_id, 'Здравствуйте, зарегистрируйтесь и узнавайте погоду в вашем городе.')
    await send_message(chat_id, 'Введите email')
    steps[chat_id] = process_email


async def login_process(chat_id, message):
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
        # TODO: return success status 
        # TODO: next step: write user data to db 

        await send_message(chat_id, f'Email {email} успешно подтвержден.')
        await send_message(chat_id, 'Введите ваши логин и пароль через двоеточие (Пример: user:password')
        steps[chat_id] = login_process

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


gram.remove_webhook(BASE_URL, TG_API_TOKEN)
gram.set_webhook(BASE_URL, TG_API_TOKEN)

app = Starlette(routes=routes)  
