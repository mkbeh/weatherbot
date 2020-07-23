# -*- coding: utf-8 -*-
import bcrypt

from src.aiotelegram import GramBot
from src.secret import TG_API_TOKEN


# TODO: in future: remove users and next_step_handler and use redis.
users = {}
next_step_handler = {}

bot = GramBot(TG_API_TOKEN)


class User:
    def __init__(self, email, password=None, city=None):
        self.email       = email
        self.is_active   = False            # email confirmed activation
        self._password   = password
        self.salt        = None
        self.city        = city
        self.is_login    = False

    @property
    def password(self):
        return self._password

    @password.setter
    def password(self, password):
        self.salt = bcrypt.gensalt()
        self._password = bcrypt.hashpw(password.encode(), self.salt)

    def __str__(self):
        return ''.join(f'{key}:{val}, ' for key, val in self.__dict__.items())
