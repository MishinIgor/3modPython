import requests,telebot
from pogoda import *
with open('token_8gr.txt') as f:
    TOKEN = f.read()
bot = telebot.TeleBot(TOKEN)

comands = ['help','pogoda','location']
text_comands = '/' + (',/').join(comands)
@bot.message_handler(commands=comands)
def universal(message):
    if message.text == '/help':
        bot.send_message(message.chat.id,f'Я умею выполнять команды: {text_comands}')
    elif message.text == '/location':
        keyboard = telebot.types.ReplyKeyboardMarkup(row_width=1,resize_keyboard=True)
        button_geo = telebot.types.KeyboardButton(text='Поделиться местоположением',request_location=True)
        keyboard.add(button_geo)
        bot.send_message(message.chat.id,'Поделиться местоположением',reply_markup=keyboard)
def info_pogoda(message):
    a = telebot.types.ReplyKeyboardRemove()
    bot.send_message(message.chat.id,pogoda(message.location.latitude,message.location.longitude),reply_markup=a)
bot.polling(non_stop=True, interval=0)