import telebot
with open('token_5gr.txt') as f:
    TOKEN = f.read() # В файле записан только токен бота
bot = telebot.TeleBot(TOKEN)

keyboard = telebot.types.InlineKeyboardMarkup()
lst = []
for i in range(5):
    lst.append(telebot.types.InlineKeyboardButton(text=str(i), callback_data=str(i)))
keyboard.add(*lst)
@bot.message_handler(commands=['start'])
def start(message):
    bot.send_message(message.chat.id,'Выбирайте кнопку из предложенных: ',reply_markup=keyboard)
@bot.callback_query_handler(func=lambda call:True)
def callback_query(call):
    if call.data != '':
        bot.answer_callback_query(call.id,f'Ты выбрал кнопку номер {call.data}')
        bot.send_message(call.message.chat.id,f'Ты выбрал кнопку номер {call.data}')
bot.polling(non_stop=True, interval=0)