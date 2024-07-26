import telebot, random
with open('token_9gr.txt') as f:
    TOKEN = f.read()
button_name = ['Камень',"Ножницы","Бумага"]
bot = telebot.TeleBot(TOKEN)
user_id1, user_id2 = 0, 0
call_result = ''
choise1, choise2 = '', ''
markup = telebot.types.InlineKeyboardMarkup()
button1 = telebot.types.InlineKeyboardButton(text='Да',callback_data='Да')
button2 = telebot.types.InlineKeyboardButton(text='Нет',callback_data='Нет')
markup.add(button1,button2)

keyboard = telebot.types.InlineKeyboardMarkup()
lst = []
for i in button_name:
    lst.append(telebot.types.InlineKeyboardButton(text=str(i),callback_data=str(i)))
keyboard.add(*lst)
@bot.message_handler(commands=['start','id'])
def start(message):
    if message.text == '/start':
        global user_id1
        with open('choise1.txt', 'w') as f:
            f.write('')
        with open('choise2.txt', 'w') as f:
            f.write('')
        user_id1 = message.from_user.id
        bot.send_message(user_id1,'С каким пользователем хотите сыграть? Введите его id')
        bot.register_next_step_handler(message,get_ans)
    elif message.text == '/id':
        bot.send_message(message.chat.id,f'Ваш id: {message.from_user.id}')
def get_ans(message):
    global user_id2
    user_id2 = int(message.text)
    bot.send_message(user_id2,'Хотите сыграть в КМБ?',reply_markup=markup)
def result(choise1,choise2):
    if choise1 == choise2:
        bot.send_message(user_id1,'Ничья')
        bot.send_message(user_id2,'Ничья')
    elif (choise1 == 'Ножницы' and choise2 == 'Бумага') or (choise1 == 'Бумага' and choise2 == 'Камень') or (choise1 == 'Камень' and choise2 == 'Ножницы'):
        bot.send_message(user_id1,f'Вы победили! Вы выбрали {choise1}, соперник выбрал {choise2}')
        bot.send_message(user_id2,f'Вы проиграли! Вы выбрали {choise2}, соперник выбрал {choise1}')
    else:
        bot.send_message(user_id1,f'Вы проиграли! Вы выбрали {choise1}, соперник выбрал {choise2}')
        bot.send_message(user_id2,f'Вы победили! Вы выбрали {choise2}, соперник выбрал {choise1}')
@bot.callback_query_handler(func=lambda call: True) 
def call_back(call):
    global call_result,choise1,choise2
    if call.data == 'Да' and call_result == '':
        bot.send_message(user_id2,'Сделайте выбор: ',reply_markup=keyboard)
        bot.send_message(user_id1,'Сделайте выбор: ',reply_markup=keyboard)
        call_result = 'Да'
    elif call.data == 'Нет' and call_result == '':
        bot.send_message(user_id1,'Данный пользователь отказался от игры')
        call_result = 'Нет'
    if call.from_user.id == user_id1 and call.data in button_name and choise1 == '':
        with open('choise1.txt','r+',encoding='utf-8') as f:
            f.write(call.data)
            choise1 = f.read()
    if call.from_user.id == user_id2 and call.data in button_name and choise2 == '':
        with open('choise2.txt','r+',encoding='utf-8') as f:
            f.write(call.data)
            choise2 = f.read()
    if choise1 != '' and choise2 != '':
        result(choise1,choise2)
@bot.message_handler(commands=['result'])
def resultat(message):
    result(choise1,choise2)
bot.polling(non_stop=True,interval=0)
