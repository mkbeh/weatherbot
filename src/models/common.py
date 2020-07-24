# -*- coding: utf-8 -*-
from src.models import User


async def get_user(chat_id):
    return await User.filter(id=chat_id).first()
