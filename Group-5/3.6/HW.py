import telebot,random
from telebot import types
with open('token_5gr.txt') as f:
    TOKEN = f.read()

bot = telebot.TeleBot(TOKEN)
pobednoe = random.randint(0,4)
keyboard = telebot.types.InlineKeyboardMarkup()
lst = []
for i in range(5):
    lst.append(telebot.types.InlineKeyboardButton(text='🎩',callback_data=str(random.randint(0,4))))
keyboard.row(*lst)

@bot.message_handler(commands=['start'])
def start(message):
    bot.send_message(message.chat.id,'Сделай свой выбор',reply_markup=keyboard)
@bot.callback_query_handler(func= lambda call: True)
def callback_query(call):
    if int(call.data) == pobednoe:
        bot.send_message(call.message.chat.id,f'Ты победил! Твоё число: {call.data} Победное: {pobednoe}')
    else:
        bot.send_message(call.message.chat.id,f'Ты проиграл!Твоё число: {call.data} Победное: {pobednoe}')
bot.polling(non_stop=True,interval=0)