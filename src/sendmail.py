# -*- coding: utf-8 -*-
import aiosmtplib

from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

from itsdangerous import URLSafeTimedSerializer

from src import GMAIL_USER, GMAIL_PWD, SECRET_KEY, PWD_SALT, NGROK_URL


HTML_MSG = """
<p>Здравствуйте! Благодарим Вас за регистрацию. Пожалуйста пройдите по следующей ссылке , чтобы активировать ваш акканут:</p>
<p><a href="{0}">{1}</a></p>
<br>
<p>Cheers!</p>
"""


async def confirm_token(token, expiration=3600):
    """[summary]

    Args:
        token ([str]): [Confirm email confirmation token]
        chat_id ([str]): [chat id]
        expiration (int, optional): [Confirmation token expiration time]. Defaults to 3600.

    Returns:
        [tuple]: [email, chat_id]
    """
    serializer = URLSafeTimedSerializer(SECRET_KEY)
    try:
        data = serializer.loads(
            token,
            salt=PWD_SALT,
            max_age=expiration
        )
    except:
        return False

    return data.split(':')


async def _create_msg(activation_url, email):
    message = MIMEMultipart("alternative")
    message["From"] = GMAIL_USER
    message["To"] = email
    message["Subject"] = 'Подтверждение регистрации в WeatherBot'

    html_message = MIMEText(HTML_MSG.format(activation_url, activation_url), "html", "utf-8")
    message.attach(html_message)

    return message


async def _generate_confirmation_token(email, chat_id):
    serializer = URLSafeTimedSerializer(SECRET_KEY)
    return serializer.dumps(f'{email}:{chat_id}', salt=PWD_SALT)


async def send_confirmation_mail(email, chat_id):
    token = await _generate_confirmation_token(email, chat_id)
    activation_url = f'{NGROK_URL}/confirm/{token}'
    message = await _create_msg(activation_url, email)

    await aiosmtplib.send(
        message, 
        hostname="smtp.gmail.com", 
        port=465,
        username=GMAIL_USER,
        password=GMAIL_PWD,
        use_tls=True,
    )
