# -*- coding: utf-8 -*-
import os

import bcrypt

from src.aiotelegram import GramBot


TELEGRAM_API_TOKEN      = os.environ.get('TELEGRAM_API_TOKEN')
OPENWEATHER_API_TOKEN   = os.environ.get('OPENWEATHER_API_TOKEN')

NGROK_URL               = os.environ.get('NGROK_URL')

SECRET_KEY              = os.environ.get('SECRET_KEY')
PWD_SALT                = os.environ.get('PWD_SALT')

GMAIL_USER              = os.environ.get('GMAIL_USER')
GMAIL_PWD               = os.environ.get('GMAIL_PWD')

MYSQL_URL               = os.environ.get('MYSQL_URL')


# TODO: in future: remove users and next_step_handler and use redis.
users = {}
next_step_handler = {}

bot = GramBot(TELEGRAM_API_TOKEN)
