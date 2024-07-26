import telebot
from telebot import types

with open('token_8gr.txt') as f:
    TOKEN = f.read()
bot = telebot.TeleBot(TOKEN)



markup = types.InlineKeyboardMarkup()
button = types.InlineKeyboardButton(text='Нажми меня!', callback_data='button1')
markup.add(button)
@bot.message_handler(commands=['start'])
def but_start(message):
    bot.send_message(message.chat.id, 'Нажми кнопку:', reply_markup=markup)
@bot.callback_query_handler(func=lambda call: True)
def callback_query(call):
    if call.data == 'button1':
        bot.answer_callback_query(call.id, 'Вы нажали кнопку 1')
        bot.send_message(call.message.chat.id,'123')
bot.polling(non_stop=True, interval=0)