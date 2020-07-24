# -*- coding: utf-8 -*-
import bcrypt

from tortoise.models import Model
from tortoise import fields


class User(Model):
    id         = fields.IntField(pk=True)
    email      = fields.CharField(max_length=255)
    _password  = fields.BinaryField(null=True)
    salt       = fields.BinaryField(null=True)
    city       = fields.CharField(max_length=255, null=True)

    timestamp  = fields.DatetimeField(auto_now_add=True)

    is_active  = fields.BooleanField(default=False)
    is_login   = fields.BooleanField(default=False)

    @property
    def password(self):
        return self._password

    @password.setter
    def password(self, password):
        self.salt = bcrypt.gensalt()
        self._password = bcrypt.hashpw(password.encode(), self.salt)

    def __str__(self):
        return ''.join(f'{key}:{val}, ' for key, val in self.__dict__.items())

