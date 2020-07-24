# -*- coding: utf-8 -*-
from datetime import datetime

from src.models import User, Weather


async def get_user(chat_id: int) -> User:
    return await User.filter(id=chat_id).first()


async def get_weather(city):
    return await Weather.filter(
        city=city, date=datetime.now().date()
    ).first().values("temperature", "humidity")


async def save_data(user: User, key, value) -> None:
    user.__setattr__(key, value)
    await user.save()


async def create_weather(**kwargs):
    await Weather(**kwargs).save()
