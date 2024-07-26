import telebot, random
with open('token_9gr.txt') as f:
    TOKEN = f.read()
bot = telebot.TeleBot(TOKEN)

keyboard = telebot.types.ReplyKeyboardMarkup(resize_keyboard=True)
keyboard.add('Кнопка 1','Кнопка 2', "Кнопка 3")
@bot.message_handler(commands=['start'])
def start_message(message):
    bot.send_message(message.chat.id,'Нажми на кнопку: ',reply_markup=keyboard)
@bot.message_handler(commands=['del'])
def del_buttons(message):
    a = telebot.types.ReplyKeyboardRemove()
    bot.send_message(message.chat.id,'Кнопки очищены',reply_markup=a)
bot.polling(non_stop=True,interval=0)
