# -*- coding: utf-8 -*-
import re

from src import users, next_step_handler, bot
from src import sendmail
from src import stepsutils
from src.aiotelegram import types as bot_types

from src.models import User, common


async def weather(chat_id, text):
    pass


async def login(chat_id, credentials):
    try:
        _, password = credentials.split(':')
    except ValueError:
        await bot.send_message(chat_id, 'Некорректные учетные данные. Введите заново.')
        next_step_handler[chat_id] = login
    else:
        user = await common.get_user(chat_id)
        if await stepsutils.is_pwd_valid(password, user.password):
            user.is_login = True
            await user.save()

            markup = await stepsutils.create_reply_markup(('Погода сегодня', 'Погода на неделю', 'Выйти'))
            await bot.send_message(chat_id, 'Вы успешно авторизировались. Теперь вам открыт доступ в личный кабинет.', reply_markup=markup)

            next_step_handler[chat_id] = weather
        else:
            await bot.send_message(chat_id, 'Некорректные учетные данные. Введите заново.')
            next_step_handler[chat_id] = login


async def process_city(chat_id, city):
    # TODO: validate city.
    
    if city:
        user = users[chat_id]
        user.city = city
        
        await sendmail.send_confirmation_mail(user.email, chat_id)
        await bot.send_message(chat_id, 'На почту выслано письмо для активации вашего почтового адреса. После подтверждения вы сможете войти в личный кабинет.')

        # next_step_handler[chat_id] = login
    else:
        await bot.send_message(chat_id, 'Некорректный город. Введите заново.')
        next_step_handler[chat_id] = process_city


async def process_password(chat_id, password):
    if 6 <= len(password) <= 10:
        user = users[chat_id]
        user.password = password

        next_step_handler[chat_id] = process_city
        await bot.send_message(chat_id, 'Введите город.')
    else:
        await bot.send_message(chat_id, 'Некорректный пароль. Введите заново.')
        next_step_handler[chat_id] = process_password


async def process_email(chat_id, email):
    email_pattern = re.compile(r'[^@]+@[^@]+\.[^@]+')
    if re.match(email_pattern, email):
        users[chat_id] = User(id=chat_id, email=email)
        next_step_handler[chat_id] = process_password
        await bot.send_message(chat_id, 'Введите пароль. (Длина пароля должна быть от 6 до 10 символов)')
    else:
        await bot.send_message(chat_id, 'Некорректный email. Введите заново.')
        next_step_handler[chat_id] = process_email


async def start(chat_id, message):
    markup = bot_types.ReplyKeyboardRemove()
    await bot.send_message(chat_id, 'Здравствуйте, зарегистрируйтесь и узнавайте погоду в вашем городе.', reply_markup=markup)
    await bot.send_message(chat_id, 'Введите email')
    next_step_handler[chat_id] = process_email
