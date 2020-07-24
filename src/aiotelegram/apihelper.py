# -*- coding: utf-8 -*-
import asyncio

import aiohttp
import requests

from .types import JsonDeserializable


API_URL = 'https://api.telegram.org/bot{token}/{method_name}'


# TODO: need to save client session in var.
    

async def _make_request(token, method_name, method='get', params=None):
    request_url = API_URL.format(token=token, method_name=method_name)

    async with aiohttp.ClientSession() as session:
        async with session.post(request_url, data=params) as resp:
           pass


def set_webhook(token, url):
    method_url = 'setWebhook'
    payload = {'url': url}
    asyncio.ensure_future(
        _make_request(token, method_url, method='post', params=payload)
    )


def delete_webhook(token):
    method_url = 'deleteWebhook'
    asyncio.ensure_future(
        _make_request(token, method_url)
    )


async def send_message(token, chat_id, text, 
                       reply_markup=None):
    method_url = 'sendMessage'
    payload = {'chat_id': chat_id, 'text': text}
    if reply_markup:
        payload['reply_markup'] = await _convert_markup(reply_markup)

    await _make_request(token, method_url, method='post', params=payload)


async def _convert_markup(markup):
    if isinstance(markup, JsonDeserializable):
        return await markup.to_json()
    
    return markup
