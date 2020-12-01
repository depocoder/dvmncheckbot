import os
import time
import logging
import textwrap
from urllib.parse import urljoin
from dotenv import load_dotenv
import requests
import telegram


class MyLogsHandler(logging.Handler):
    def send_nessage(self, record, bot, tg_chat_id):
        bot.send_message(
                chat_id=tg_chat_id, text=record)


def send_request(url, payload):
    dvmn_token = os.getenv('DVMN_TOKEN')
    auth_headers = {'Authorization': "TOKEN " + dvmn_token}
    response = requests.get(
        url, headers=auth_headers, timeout=91, params=payload)
    response.raise_for_status()
    return response.json()


if __name__ == "__main__":
    logger = logging.getLogger("Название логера")
    logger.setLevel(logging.INFO)
    logger.addHandler(MyLogsHandler())
    logger.info("Я новый логер!")
    url = 'https://dvmn.org/api/long_polling/'
    load_dotenv()
    bot = telegram.Bot(token=os.getenv("TG_TOKEN"))
    payload = {}
    tg_chat_id = os.getenv("TG_CHAT_ID")
    while True:
        try:
            api_message = send_request(url, payload)
        except requests.exceptions.ReadTimeout:
            print('Ошибка на сервере Devman')
            continue
        except requests.exceptions.ConnectionError:
            print('Проверьте соединение с интернетом.')
            time.sleep(10)
            continue
        if api_message['status'] == 'timeout':
            payload['timestamp'] = api_message['timestamp_to_request']
        elif api_message['status'] == 'found':
            payload['timestamp'] = api_message['last_attempt_timestamp']
            important_message = api_message["new_attempts"][0]
            link = urljoin(
                'https://dvmn.org/', important_message['lesson_url'])
            if important_message['is_negative']:
                status_mode = 'К сожалению в работе нашлись ошибки.'
            else:
                status_mode = '''Преподователю все понравилось,
                можете проходить следующий модуль.'''
            text_mess = (
                f'''\
                У вас проверили работу.
                <<{important_message["lesson_title"]}>>.
                {status_mode} Ссылка на модуль - {link}''')
            bot.send_message(
                chat_id=tg_chat_id, text=textwrap.dedent(text_mess))
