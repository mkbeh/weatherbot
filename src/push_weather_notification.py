# -*- coding: utf-8 -*-

# TODO: use uvloop

import asyncio

import aiohttp

from tortoise import Tortoise
from tortoise.contrib.starlette import register_tortoise

from src import bot, NGROK_URL, MYSQL_URL
from src import stepsutils
from src.messages import *
from src.models import User


async def push_weather_notification(city, chat_id):
    weather_data = await stepsutils.get_weather_data(city)
    await bot.send_notification(
        chat_id, 'Ежедневное уведомление\n' + TEMPLATE_WEATHER_TODAY.format(city, *weather_data.values())
        )


async def notification_handler():
    users = await User.filter(is_login=True).all().values('id', 'city')
    await asyncio.gather(
        *(push_weather_notification(user['city'], user['id']) for user in users)
    )


async def main_loop():
    await bot.set_webhook(NGROK_URL)
    await Tortoise.init(db_url=MYSQL_URL, modules={"models": ["src.models"]})
    await notification_handler()


if __name__ == "__main__":
    asyncio.get_event_loop().run_until_complete(
        main_loop()
    )
