# This is a sample Python script.

import telebot
import requests
import json

# Создаем экземпляр бота
bot = telebot.TeleBot('5666758445:AAFh8Rt879v1_w5kvokY5qoZ4RiFCE07JsM')

ALL_currencys = [
    'USD',
    'EUR',
    'TJS',
    'THB'
]


# Функция, обрабатывающая команду /start
@bot.message_handler(commands=['start'])
def start(message):
    str_curs = '\n/'.join(ALL_currencys)
    bot.send_message(message.chat.id, f'/Courses')


# Проверка курса
@bot.message_handler(content_types=['text'])
def handle_text(message):
    result = requests.get('https://cdn.cur.su/api/latest.json')
    if result.status_code == 200:
        dict_result = json.loads(result.text)
        currencyRUB = 'RUB'
        kursRUB = dict_result['rates'][currencyRUB]
        if message.text == '/Courses':
            str_message = ''
            for cur in ALL_currencys:
                if cur != 'USD':
                    kurs2 = dict_result['rates'][cur]
                    kurs = kursRUB / kurs2
                else:
                    kurs = kursRUB
                str_message += f'{cur} to {currencyRUB}: {kurs:0.2f}\n'
            bot.send_message(message.chat.id, str_message)
    else:
        bot.send_message(message.chat.id, f'Ошибка {result.status_code}')


# Запускаем бота

bot.infinity_polling()
