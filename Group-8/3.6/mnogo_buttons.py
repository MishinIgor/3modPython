import telebot
with open('token_8gr.txt') as f:
    TOKEN = f.read()
bot = telebot.TeleBot(TOKEN)

@bot.message_handler(commands=['start'])
def start(message):
    # создаем клавиатуру
    keyboard = telebot.types.InlineKeyboardMarkup()
    lst = []
    for i in range(5):
        # добавляем кнопки с вариантами ответов
        lst.append(telebot.types.InlineKeyboardButton(text=str(i), callback_data=str(i)))
    keyboard.row(*lst)
@bot.callback_query_handler(func=lambda call: True)
def callback_query(call):
    bot.send_message(call.message.chat.id, f'Ты выбрал кнопку номер {call.data}')
    
bot.polling(non_stop=True, interval=0)