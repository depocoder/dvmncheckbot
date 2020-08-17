import os
from dotenv import load_dotenv
import requests
from time import sleep
import telegram


def send_request(url, payload):
        AUTH_HEADERS = {'Authorization':DVMN_TOKEN}
        response = requests.get(url, headers=AUTH_HEADERS, params=payload)
        return response.json()


if __name__ == "__main__":
    url = 'https://dvmn.org/api/long_polling/'
    load_dotenv()
    DVMN_TOKEN = os.getenv('DVMN_TOKEN')
    bot = telegram.Bot(token=os.getenv("TG_TOKEN"))
    payload = {"timestamp":''}
    chat_id = 1077817560
    while True:
        try:
            api_mess = send_request(url, payload)
        except requests.exceptions.ReadTimeout:
            print ('Ошибка на сервере DevMan.')
        except ConnectionError:
            print('Проверьте соединение с интернетом.')
        print(api_mess)
        if api_mess['status'] == 'timeout':
            payload['timestamp'] = api_mess['timestamp_to_request']
        elif api_mess['status'] == 'found':
            bot.send_message(chat_id=chat_id, text=api_mess)
        sleep(1)