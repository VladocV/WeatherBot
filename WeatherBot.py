#https://api.openweathermap.org/data/2.5/weather?q=paris&appid=fe477a48de515ccf870a30058ad6df61&units=metric&lang=ru
import time as timer
#import datetime
import telebot
import requests
import json
from telebot import types

token = '6440819860:AAHfQZA4DzifIbI57hZUlT-0gXd1g-stgEg'
bot = telebot.TeleBot(token)
API = 'fe477a48de515ccf870a30058ad6df61'
city = ''


@bot.message_handler(commands=['start'])
def start(message):
    bot.send_message(message.chat.id,
'Приветствую, я могу сказать какая погода за окном! '
'Но для этого мне нужнознать в каком городе вы живете, напишите его название в чат')


@bot.message_handler(content_types=['text'])
def get_city(message):
    global city
    city = message.text.strip().lower()
    try:
        res200 = requests.get(f'https://api.openweathermap.org/data/2.5/weather?q={city}&appid={API}')
        if res200.status_code == 200:
            bot.reply_to(message, 'Спасибо, теперь я смогу всегда подсказать тебе погоду!')
            timer.sleep(0.5)
            markup = types.InlineKeyboardMarkup()
            btn1 = types.InlineKeyboardButton('Ежедневная погода', callback_data='WeatherED')
            btn2 = types.InlineKeyboardButton('Погода сейчас', callback_data='WeatherNow')
            markup.row(btn1, btn2)
            bot.send_message(message.chat.id,
            'Хочешь получить погоду сейчас или получать прогоноз каждый день(можно настроить под себя😉)',
            reply_markup=markup)
        else:
            bot.reply_to(message, '''Я не нашел такого населенного пункта😣...
Проверте написание или напишите ближайший более крупный город''')
    except requests.exceptions.Timeout:
        bot.send_message(message.chat.id, "Что-то пошло не так, гидрометцентр не отвечает, пожалуйста попробуйте позже")
    except:
        bot.send_message(message.chat.id, "Что-то пошло не так, пожалуйста попробуйте позже")


@bot.callback_query_handler(func=lambda callback: True)
def callback_mes(callback):
    print(100)
    if callback.data == 'WeatherNow':
        try:
            res = requests.get(f'https://api.openweathermap.org/data/2.5/weather?q={city}&appid={API}&units=metric&lang=ru')
            data = json.loads(res.text)
        except requests.exceptions.Timeout:
            try:
                res = requests.get(
                f'https://api.openweathermap.org/data/2.5/weather?q={city}&appid=e4571e219821a8b5fc265178a0b92be9&units=metric&lang=ru')
                data = json.loads(res.text)
            except requests.exceptions.Timeout:
                bot.send_message(callback.message.chat.id, "Что-то пошло не так, сервер не отвечает😣. Пожалуста попробуйте позже")
        clouds = data['clouds']['all']
        if clouds <= 20:
            icon_weath = '☀'
        elif clouds <= 40:
            icon_weath = '🌫'
        elif clouds <= 60:
            icon_weath = '🌤'
        elif clouds <= 80:
            icon_weath = '🌥️'
        else:
            icon_weath = '☁'
        temp = round(data['main']['temp'], 0)           # Температура
        feels = round(data['main']['feels_like'], 0)    # Ощущается
        pres = round(data['main']['pressure'], 0)       # Давление
        humid = round(data['main']['humidity'], 0)      # Влажность
        w_speed = round(data['wind']['speed'], 1)       # Скорость ветра
        visib = round(data['visibility'], 0)                # Видимость
        weather = data['weather'][0]['description'].capitalize() # Небо
        if 'gust' in data['wind']:
            w_gust = round(data['wind']['gust'], 1)     # Порывы
            w_gust_mc = str(w_gust) + 'м/с'
        else:
            w_gust = False
        visib_m = str(visib) + 'м'

        bot.send_message(callback.message.chat.id,
f'Сейчас в {city}:\n{weather}({icon_weath})\nТемпература🌡️: {temp}°C\n(Ощущается: {feels}°)\nСкорость ветра💨: {w_speed}м/с\n(Порывы: {w_gust_mc if w_gust == True else "Незначительны"})\nДавление🕛: {pres}мм р.с\nВлажность💧: {humid}%\nВидимость: {visib_m if float(visib) <= 3000 else "Полноценная"}')
        print(200)
    elif callback.data == 'WeatherED':
        bot.send_message(callback.message.chat.id, "Эта функция пока недоступна")
        print(300)
bot.polling(none_stop=True)
print(1000)
