# -*- coding: utf-8 -*-
import re

from src import users, next_step_handler, bot, User
from src import sendmail


async def process_city(chat_id, city):
    # TODO: validate city.
    
    if city:
        user = users[chat_id]
        user.city = city
        
        await sendmail.send_confirmation_mail(user.email, chat_id)
        await bot.send_message(chat_id, 'На почту выслано письмо для активации вашего почтового адреса. После подтверждения вы сможете войти в личный кабинет.')
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
        users[chat_id] = User(email)
        next_step_handler[chat_id] = process_password
        await bot.send_message(chat_id, 'Введите пароль. (Длина пароля должна быть от 6 до 10 символов)')
    else:
        await bot.send_message(chat_id, 'Некорректный email. Введите заново.')
        next_step_handler[chat_id] = process_email


async def start(chat_id, message):
    await bot.send_message(chat_id, 'Здравствуйте, зарегистрируйтесь и узнавайте погоду в вашем городе.')
    await bot.send_message(chat_id, 'Введите email')
    next_step_handler[chat_id] = process_email


async def personal_area_process(chat_id, message):
    pass

