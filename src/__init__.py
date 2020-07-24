# -*- coding: utf-8 -*-
import bcrypt

from src.aiotelegram import GramBot
from src.secret import TG_API_TOKEN


# TODO: in future: remove users and next_step_handler and use redis.
users = {}
next_step_handler = {}

bot = GramBot(TG_API_TOKEN)
