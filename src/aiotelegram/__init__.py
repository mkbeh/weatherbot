# -*- coding: utf-8 -*-
from . import apihelper


class GramBot:
    """
    This is Gram Class.
    
    Methods:
        sendMessage

        set_webhook
        delete_webhook
    """

    def __init__(self, token):
        self.token = token

    def set_webhook(self, url):
        apihelper.set_webhook(self.token, url)

    def delete_webhook(self):
        apihelper.delete_webhook(self.token)

    async def send_message(self, chat_id, text, reply_markup=None):
        await apihelper.send_message(self.token, chat_id, text, reply_markup)