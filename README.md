# Simple asynchronous "Weather telegram bot".


**Supports actions:**

* User registration/login/logout
* Send mail for confirm user email address
* Get weather today (temperature, humidity)
* Weather notifications for users every day at 10:00 AM


**Used stack:**

* Starlette
* Tortoise ORM
* MySQL
* Docker-Compose


**Third-party:**

* openweathermap.org API
* ngrok


## Setup

> git clone https://github.com/mkbeh/weatherbot && cd weatherbot

Create and fill in .env* files.
> Create 2 files in the same directory: .env_app , .env_mysql

**.env_app**
```
TELEGRAM_API_TOKEN=
OPENWEATHER_API_TOKEN=
NGROK_URL=
SECRET_KEY=random:secret:key
PWD_SALT=activation
GMAIL_USER=
GMAIL_PWD=
MYSQL_URL=mysql://<user>:<pwd>@db:3306/weatherbot
```

**.env_mysql**
```
MYSQL_ROOT_PASSWORD=root
MYSQL_DATABASE=weatherbot
MYSQL_USER=punk
MYSQL_PASSWORD=punk
MYSQL_HOST=db
```

## How to run

```
ngrok http 5000

docker-compose up
```
