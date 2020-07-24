# -*- coding: utf-8 -*-
from datetime import datetime

from tortoise.models import Model
from tortoise import fields


class Weather(Model):
    id            = fields.IntField(pk=True)
    city          = fields.CharField(max_length=255)   
    date          = fields.DateField(unique=True, default=datetime.now().date)
    temperature   = fields.IntField()
    humidity      = fields.IntField()

    def __str__(self):
        return ''.join(f'{key}:{val}, ' for key, val in self.__dict__.items())
