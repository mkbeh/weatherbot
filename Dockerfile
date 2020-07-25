FROM python:3.8


WORKDIR /weatherbot

RUN apt-get update && \
    apt-get install -y \
     netcat \ 
     cron

RUN service cron start

COPY push_weather_notifications_cron /etc/cron.d/push_weather_notifications_cron

RUN chmod 0644 /etc/cron.d/push_weather_notifications_cron

RUN crontab /etc/cron.d/push_weather_notifications_cron

COPY . .

RUN pip install -r requirements.txt

RUN chmod +x docker-entrypoint.sh

CMD ["./docker-entrypoint.sh"]
