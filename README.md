# dvmncheckbot 

## Описание проекта.   
Этот проект позволяет отслеживать проверку работ на сайте [dvmn.org](dvmn.org) через [телеграм](https://telegram.org/) бота.    
   
## Подготовка к запуску.  
Уставновить Python 3+.
```
sudo apt-get install python3
```
Установить, создать и активировать виртуальное окружение.
```
pip3 install virtualenv
python3 -m venv env
source env/bin/activate
```
Установить библиотеки командой.  
```
pip install -r requirements.txt  
```
    
Создайте файл ".env" в него надо прописать ваши token'ы.   
В переменную **DVMN_TOKEN** его можно получить [**тут**](https://dvmn.org/api/docs/).   
В переменную **TG_TOKEN** его можно получить в отце всех ботов @botfather в телеграме.    
В переменную **CHAT_ID** его можно получить в боте @myidbot командой `/getid` в телеграме.
    
**Пример**  
```
TG_TOKEN=1374455275:AAHUcCsVfH_hDeFM-3icahluF6ajIWALVXw
DVMN_TOKEN=3505d87e2ed932f3e4a18f9a9ede592d53d9e888
CHAT_ID=107781750
```

## Запуск кода.  
```
python3 main.py
```
