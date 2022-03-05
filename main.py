import os
import time
import logging
import textwrap
from urllib.parse import urljoin

from dotenv import load_dotenv
import requests
import telegram

from logger_handler import BotLogsHandler

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)


def send_request(url, payload, dvmn_token):
    auth_headers = {'Authorization': "Token " + dvmn_token}
    response = requests.get(
        url, headers=auth_headers, timeout=91, params=payload)
    response.raise_for_status()
    return response.json()


if __name__ == "__main__":
    load_dotenv()
    dvmn_token = os.getenv('DVMN_TOKEN')
    tg_token = os.getenv("TG_TOKEN")
    tg_chat_id = os.getenv("TG_CHAT_ID")
    if not all((dvmn_token, tg_chat_id, tg_token)):
        raise ValueError('Please check your env vars in .env file.')

    bot = telegram.Bot(token=tg_token)
    logger.addHandler(BotLogsHandler(bot, tg_chat_id))
    url = 'https://dvmn.org/api/long_polling/'
    payload = {}

    logger.info("Бот запущен!")
    while True:
        try:
            api_message = send_request(url, payload, dvmn_token)
        except requests.exceptions.ReadTimeout:
            logger.info('Ошибка на сервере Devman')
            continue
        except requests.exceptions.ConnectionError:
            logger.info('Проверьте соединение с интернетом.')
            time.sleep(10)
            continue
        except Exception as e:
            logger.warning(f'Бот упал с ошибкой: {e}')
            logger.info('Засыпаю на 1 минуту.')
            time.sleep(60)
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
            logger.info(textwrap.dedent(text_mess))
