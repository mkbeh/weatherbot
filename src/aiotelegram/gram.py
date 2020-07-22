# -*- coding: utf-8 -*-
import asyncio

import requests
import aiohttp


TELEGRAM_BASE_URL = 'https://api.telegram.org/bot{token}/{method}'


def make_sync_request(url, data):
    try:
        requests.post(url, data=data)
    except:
        pass


def remove_webhook(url, token):
    api_url = TELEGRAM_BASE_URL.format(token=token, method='deleteWebhook')
    data = {'url': url}

    make_sync_request(api_url, data)


def set_webhook(url, token):
    api_url = TELEGRAM_BASE_URL.format(token=token, method='setWebhook')
    data = {'url': url}

    make_sync_request(api_url, data)
