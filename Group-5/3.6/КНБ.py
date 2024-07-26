import telebot

with open('token_5gr.txt') as f:
    TOKEN = f.read() # В файле записан только токен бота
choice1, choice2 = '', ''
bot = telebot.TeleBot(TOKEN)
user_id1,user_id2 = 0, 0
keyboard_game = telebot.types.ReplyKeyboardMarkup(resize_keyboard=True)
keyboard_game.add('Камень', "Ножницы", "Бумага")
keyboard_ans = telebot.types.ReplyKeyboardMarkup(resize_keyboard=True)
keyboard_ans.add('Да',"Нет")
@bot.message_handler(commands=['game','id'])
def start(message):
    if message.text == '/game':
        global user_id1
        bot.send_message(message.chat.id,'С кем хотите сыграть? Введие id пользователя')
        user_id1 = message.from_user.id
        bot.register_next_step_handler(message,get_ans)
    elif message.text == '/id':
        bot.send_message(message.chat.id,f'Ваш id: {message.from_user.id}')
def get_ans(message):
    global user_id2
    user_id2 = int(message.text)
    send = bot.send_message(user_id2,f"С вами хочет сыграть пользователь @{message.from_user.username}.Хотите с ним сыграть?")
    bot.register_next_step_handler(send,go_play)
def go_play(message):
    global user_id1,user_id2
    if message.from_user.id == user_id2:
        if message.text == 'Да':
            bot.send_message(user_id1,'Пользователь согласился сыграть')
            bot.send_message(user_id1,'Сделайте свой выбор', reply_markup=keyboard_game)
            bot.send_message(user_id2,'Сделайте свой выбор', reply_markup=keyboard_game)
            bot.register_next_step_handler(message,result)
        else:
            bot.send_message(user_id1,'Пользователь не хочет играть с вами')
    else:
        bot.send_message(message.chat.id,f'Не спамьте пожалуйста. Мы ждём ответ от {user_id2}')
        bot.register_next_step_handler(message,go_play)
def result(message):
    if message.from_user.id == user_id1 and choice1 == '':
        choice1 == message.text
        bot.send_message(message.chat.id,'Результат записан.')
    if message.from_user.id == user_id2 and choice2 == '':
        choice2 == message.text
        bot.send_message(message.chat.id,'Результат записан.')
    if choice1 == '' or choice2 == '':
        bot.send_message(message.chat.id,'Подождите другого пользователя')
        bot.register_next_step_handler(message,result)
    else:
        if choice2 == choice1:
            bot.send_message(user_id1,'Ничья')
            bot.send_message(user_id2,'Ничья')
        elif (choice1=='Ножницы' and choice2=='Бумага') or (choice1=='Камень' and choice2=='Ножницы') or (choice1=='Бумага' and choice2=='Камень'):
            bot.send_message(user_id1,f'Победа!, соперник выбрал {choice2}')
            bot.send_message(user_id2,f'Поражение!, соперник выбрал {choice1}')
        else:
            bot.send_message(user_id2,f'Победа!, соперник выбрал {choice1}')
            bot.send_message(user_id1,f'Поражение!, соперник выбрал {choice2}')
bot.polling(non_stop=True, interval=0)