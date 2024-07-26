import telebot

with open('token_5gr.txt') as f:
    TOKEN = f.read() # В файле записан только токен бота

bot = telebot.TeleBot(TOKEN)

markup = telebot.types.InlineKeyboardMarkup()
button1 = telebot.types.InlineKeyboardButton(text = 'нажми меня!', callback_data='button1',url='https://pytba.readthedocs.io/ru/latest/types.html#telebot.types.InlineKeyboardButton')
button2 = telebot.types.InlineKeyboardButton(text = 'И меня!', callback_data='button2', url='https://pytba.readthedocs.io/ru/latest/types.html#telebot.types.InlineKeyboardMarkup')
markup.add(button1,button2)

keyboard = telebot.types.ReplyKeyboardMarkup(resize_keyboard=True)
keyboard.add('Камень', "Ножницы", "Бумага")

@bot.message_handler(commands=['start_inline','start_reply'])
def start(message):
    if message.text == '/start_inline':
        bot.send_message(message.chat.id,'Нажми на кнопку:',reply_markup=markup)
    elif message.text == '/start_reply':
        bot.send_message(message.chat.id,'Сделай свой выбор',reply_markup=keyboard)
@bot.callback_query_handler(func=lambda call:True)
def callback_query(call):
    if call.data == 'button1':
        bot.answer_callback_query(call.id,'Вы нажали на кнопку 1 из чата')
    elif call.data == 'button2':
        bot.answer_callback_query(call.id,'Вы нажали на кнопку 2 из чата')
    bot.send_message(call.id,'Была нажата кнопка')
@bot.message_handler(func= lambda message:True)
def echo_message(message):
    bot.send_message(message.chat.id,f'Вы нажали на кнопку {message.text}')
bot.polling(non_stop=True, interval=0)