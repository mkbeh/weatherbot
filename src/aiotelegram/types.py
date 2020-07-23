# -*- coding: utf-8 -*-
try:
    import ujson as json
except ImportError:
    import json

from abc import ABCMeta, abstractmethod


class Dictionaryable(metaclass=ABCMeta):
    @abstractmethod
    async def to_dict(self):
        pass


class JsonDeserializable(metaclass=ABCMeta):
    @abstractmethod
    async def to_json(self):
        pass


class ReplyKeyboardRemove(JsonDeserializable):
    def __init__(self):
        pass

    async def to_json(self):
        return json.dumps(
            {'remove_keyboard': True}
        )


class ReplyKeyboardMarkup(JsonDeserializable):
    def __init__(self):
        self.keyboard = []

    async def add(self, *args):
        row = []

        for button in args:
            btn = await button.to_dict()
            row.append(btn)

        self.keyboard.append(row)

    async def to_json(self):
        return json.dumps(
            {'keyboard': self.keyboard}
        )


class KeyboardButton(Dictionaryable):
    def __init__(self, text):
        self.text = text

    async def to_dict(self):
        return {'text': self.text}
