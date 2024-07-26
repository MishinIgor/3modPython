# При вводе команды /start необходимо создать inline клавиатуру с 5 кнопками 
# (визуально одинаковыми, но в callback_data должны быть разные значения от 0 до 4, в зависимости от кнопки). 
# При нажатии на любую из кнопок будет вызываться обработчик, в котором с помощью модуля random будем определять 
# победное значение (от 0 до 4). Далее с помощью условия сравнивается ответ пользователя и победное значение и 
# выводится результат. 

import telebot, random
with open('token_9gr.txt') as f:
    TOKEN = f.read()

bot = telebot.TeleBot(TOKEN)

keyboard = telebot.types.InlineKeyboardMarkup()
lst = []
for i in range(5):
    lst.append(telebot.types.InlineKeyboardButton(text='🔥',callback_data=str(random.randint(0,4))))
keyboard.add(*lst)
@bot.message_handler(commands=['start'])
def start(message):
    bot.send_message(message.chat.id,'Выбирай:',reply_markup=keyboard)

@bot.callback_query_handler(func=lambda call: True)
def call_back(call):
    pobednoe = random.randint(0,4)
    bot.answer_callback_query(call.id,f"Вам выпало число {call.data}, победное {pobednoe}")
    if pobednoe == int(call.data):
        bot.send_message(call.message.chat.id,f'Победа!')
    else:
        bot.send_message(call.message.chat.id,f'Поражение!')
bot.polling(non_stop=True,interval=0)
