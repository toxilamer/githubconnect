# This is a sample Python script.

import telebot
import requests
import json
from telebot import types  # для указание типов

# Создаем экземпляр бота
bot = telebot.TeleBot('5666758445:AAFh8Rt879v1_w5kvokY5qoZ4RiFCE07JsM')

ALL_currencys = [
    'USD',
    'EUR',
    'TJS',
    'RUB',
    'THB'
]

my_currencys = [
    'RUB',
    'THB',
    'TJS',
    'USD',
    'EUR'
]


def add_button(message_chat_id):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    for my_currency in my_currencys:
        button_currency = types.KeyboardButton(my_currency)
        markup.add(button_currency)
    bot.send_message(message_chat_id, 'Choise currency:', reply_markup=markup)


# Функция, обрабатывающая команду /start
@bot.message_handler(commands=['start'])
def start(message):
    add_button(message.chat.id)


# Проверка курса
@bot.message_handler(content_types=['text'])
def handle_text(message):
    result = requests.get('https://cdn.cur.su/api/latest.json')
    if result.status_code == 200:
        dict_result = json.loads(result.text)
        my_currency = message.text
        rates = dict_result['rates']
        if my_currency in rates:
            my_kurs = rates[my_currency]
            str_message_1 = ''
            str_message_1000 = ''
            for cur in ALL_currencys:
                if cur == my_currency:
                    continue
                elif cur != 'USD':
                    kurs2 = dict_result['rates'][cur]
                    kurs = my_kurs / kurs2
                else:
                    kurs = my_kurs
                str_message_1 += f'{cur} to {my_currency}: {kurs:0.2f}\n'
                str_message_1000 += f'{cur} to {my_currency} (1000 {my_currency}): {1000 / kurs:0.0f}\n'
            bot.send_message(message.chat.id, str_message_1 + str_message_1000)
        else:
            bot.send_message(message.chat.id, f'Currency <{my_currency}> not found')
    else:
        bot.send_message(message.chat.id, f'Ошибка {result.status_code}')
    add_button(message.chat.id)


# Запускаем бота

bot.infinity_polling()
