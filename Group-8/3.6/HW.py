# При вводе команды /start необходимо создать inline клавиатуру с 5 кнопками 
# (визуально одинаковыми, но в callback_data должны быть разные значения от 0 до 4, в зависимости от кнопки). 
# При нажатии на любую из кнопок будет вызываться обработчик, в котором с помощью модуля random будем определять 
# победное значение (от 0 до 4). Далее с помощью условия сравнивается ответ пользователя и победное значение и 
# выводится результат. 
import telebot,random
with open('token_8gr.txt') as f:
    TOKEN = f.read()
bot = telebot.TeleBot(TOKEN)
pobednoe = random.randint(0,4)
# создаем клавиатуру ##########################################
keyboard = telebot.types.InlineKeyboardMarkup()
lst = []
for i in range(5):
    # добавляем кнопки с вариантами ответов
    lst.append(telebot.types.InlineKeyboardButton(text='Выбери меня', callback_data=str(random.randint(0,4))))
keyboard.row(*lst)
############################################
@bot.message_handler(commands=['start'])
def start(message):
    bot.send_message(message.chat.id,'Сделай свой выбор: ',reply_markup=keyboard)

@bot.callback_query_handler(func=lambda call: True)
def callback_query(call):
    if pobednoe == int(call.data):
        bot.send_message(call.message.chat.id, f'Значение в кнопке {call.data}, победное {pobednoe}. Победа')
    else:
        bot.send_message(call.message.chat.id, f'Значение в кнопке {call.data}, победное {pobednoe}. Поражение')
    
bot.polling(non_stop=True, interval=0)