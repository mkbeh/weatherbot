# -*- coding: utf-8 -*-
import aiohttp
import bcrypt

from datetime import datetime

from src import bot
from src.models import Weather, common
from src.aiotelegram import types as bot_types

from src import OPENWEATHER_API_TOKEN


async def is_pwd_valid(password, hash):
    return bcrypt.checkpw(password.encode(), hash)


async def create_reply_markup(buttons_names):
    markup = bot_types.ReplyKeyboardMarkup()
    buttons = [bot_types.KeyboardButton(text) for text in buttons_names]
    await markup.add(*buttons)

    return markup


async def _make_request(url):
    async with aiohttp.ClientSession() as session:
        async with session.get(url) as resp:
           return await resp.json()


async def _get_weather_today(city):
    url = f'http://api.openweathermap.org/data/2.5/weather?q={city}&appid={OPENWEATHER_API_TOKEN}'

    json_data = await _make_request(url)
    temperature = int(json_data['main']['temp']) - 273
    humidity = int(json_data['main']['humidity'])
    
    return {'temperature': temperature, 'humidity': humidity}


async def get_weather_data(city):
    weather = await common.get_weather(city)
    if weather:
        weather_data = weather[0]
    else:
        weather_data = await _get_weather_today(city)
        await common.create_weather(city=city, **weather_data)

    return weather_data
