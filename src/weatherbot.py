# -*- coding: utf-8 -*-
from starlette.applications import Starlette
from starlette.routing import Route

from starlette.responses import JSONResponse

from tortoise.contrib.starlette import register_tortoise

from uvicorn.main import run

from src import users, next_step_handler, bot
from src import sendmail, steps
from src.aiotelegram import types as bot_types
from src.secret import BASE_URL, DB_URL


app = Starlette()

register_tortoise(app, db_url=DB_URL, modules={"models": ["src.models"]}, generate_schemas=True)

bot.delete_webhook()
bot.set_webhook(BASE_URL)


async def send_email_confirmation_success_msg(email, chat_id):
    await bot.send_message(chat_id, f'Email {email} успешно подтвержден.')
    await bot.send_message(chat_id, 'Для того , чтобы войти в личный кабинет введите email и пароль через двоеточие (Пример: email:password')
    next_step_handler[chat_id] = steps.login


@app.route('/confirm/{token}')
async def email_confirmation(request):
    token = request.path_params['token']
    try:
        email, chat_id = await sendmail.confirm_token(token)
        chat_id = int(chat_id)
    except:
        # NOTE: need to send error to user into Telegram.
        return JSONResponse({'ok': 'Ошибка активации.'})
    else:
        user = users[chat_id]
        user.is_active = True
        await user.save()    
    
        await send_email_confirmation_success_msg(email, chat_id)

        return JSONResponse({'ok': 'Активация почты прошла успешно'})


@app.route('/', methods=['GET', 'POST'])
async def receive_update(request):
    if request.method == 'POST':
        data = await request.json()
        text = data['message']['text']
        chat_id = data['message']['chat']['id']

        if text == '/start':
            handler = steps.start
        else:
            try:
                handler = next_step_handler[chat_id]
            except KeyError:
                handler = steps.start

        await handler(chat_id, text)

    return JSONResponse({'ok': True})
