import telebot
from telebot import types
with open('token_15gr.txt') as f:
    TOKEN = f.read()
my_chatid = -4137666167
bot = telebot.TeleBot(TOKEN)
button_name = ['Камень',"Ножницы","Бумага"]
@bot.message_handler(commands=['start'])
def start(message):
    keyboard = telebot.types.InlineKeyboardMarkup()
    lst = []
    for i in button_name:
        lst.append(telebot.types.InlineKeyboardButton(text=str(i),callback_data=str(i)))
    keyboard.row(*lst)
    bot.send_message(message.chat.id,'Сделай свой выбор',reply_markup=keyboard)
@bot.callback_query_handler(func= lambda call: True)
def callback_query(call):
    bot.send_message(call.message.chat.id,f'Ты выбрал {call.data}')
bot.polling(non_stop=True,interval=0)