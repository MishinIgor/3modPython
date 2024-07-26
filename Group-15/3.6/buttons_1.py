import telebot
from telebot import types
with open('token_15gr.txt') as f:
    TOKEN = f.read()
my_chatid = -4137666167
bot = telebot.TeleBot(TOKEN)

markup = types.InlineKeyboardMarkup()
button = types.InlineKeyboardButton(text='Нажми меня!',
                                    callback_data='button1')
markup.add(button)

mnogo_knopok_vrodekak = telebot.types.ReplyKeyboardMarkup(resize_keyboard=True)
mnogo_knopok_vrodekak.add('Камень',"Ножницы","Бумага")
@bot.message_handler(commands=['start_inline','start_reply'])
def start(message):
    if message.text == '/start_inline':
        bot.send_message(message.chat.id,'Нажми кнопку',reply_markup=markup)
    elif message.text == '/start_reply':
        bot.send_message(message.chat.id,'Сделай свой выбор',reply_markup=mnogo_knopok_vrodekak)
@bot.callback_query_handler(func = lambda call: True)        
def callback_query(call):
    if call.data == 'button1':
        bot.answer_callback_query(call.id,'Вы нажали на кнопку 1')
        bot.send_message(call.message.chat.id,'Вы как бы нажали конечно, но можете лучше. Попробуй нажми снова.',reply_markup=markup)
@bot.message_handler(func=lambda message: True)
def echo_message(message):
    if message.text == 'Камень':
        bot.send_message(message.chat.id,'Вы нажали на кнопку "Камень"')
    elif message.text == 'Ножницы':
        bot.send_message(message.chat.id,'Вы нажали на кнопку "Ножницы"')
    elif message.text == 'Бумага':
        bot.send_message(message.chat.id,'Вы нажали на кнопку "Бумага"')

bot.polling(non_stop=True,interval=0)