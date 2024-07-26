import telebot
with open('token_8gr.txt') as f:
    TOKEN = f.read()
bot = telebot.TeleBot(TOKEN)
id_user1, id_user2 = 0, 0
choice1, choice2 = '',''
# создание списка кнопок
keyboard_game = telebot.types.ReplyKeyboardMarkup(resize_keyboard=True)
keyboard_game.add('Камень', 'Ножницы', 'Бумага')
keyboard_ans = telebot.types.ReplyKeyboardMarkup(resize_keyboard=True)
keyboard_ans.add('Да', 'Нет')
#Обработчик команды /game
@bot.message_handler(commands=['game'])
def start_game(message):
    bot.send_message(message.chat.id,'Привет, это игра в "Камень, ножницы, бумага". Напишите имя пользователя, с кем хотите сыграть')
    bot.register_next_step_handler(message,get_ans)
def get_ans(message):
    global id_user2, id_user1
    id_user1 = message.from_user.id 
    id_user2 = message.text
    bot.register_next_step_handler(id_user2,go_play)
def go_play(message):
    bot.send_message(int(id_user2),f'С вами хочет сыграть пользователь @{message.from_user.username} в "камень ножницы будмага". Хотите сыграть?',reply_markup=keyboard_ans)
    bot.register_next_step_handler(message,ans)
def ans(message):
    if message.text == "Да":
        bot.send_message(id_user1,'Пользователь согласился сыграть с вами. Сделайте свой выбор',reply_markup=keyboard_game)
        bot.send_message(id_user2,'Сделайте свой выбор',reply_markup=keyboard_game)
        bot.register_next_step_handler(message,choice)
def choice(message):
    global choice1, choice2
    if message.from_user.id == id_user1:
        choice1 = message.text
    if message.from_user.id == id_user2:
        choice2 = message.text
    if choice2 != '' and choice1 != '':
        bot.register_next_step_handler(message,rezult)
def rezult(message):
    if choice1 == choice2:
        bot.send_message(id_user1,'Ничья')
        bot.send_message(id_user2,'Ничья')
    elif (choice1 == 'Ножницы' and choice2=='Бумага') or (choice1 == 'Камень' and choice2=='Ножницы') or (choice1 == 'Бумага' and choice2=='Камень'):
        bot.send_message(id_user1,f'Вы победили,{choice1} побеждает {choice2}')
        bot.send_message(id_user2,f'Вы проиграли,{choice1} побеждает {choice2}')
    elif (choice2 == 'Ножницы' and choice1=='Бумага') or (choice2 == 'Камень' and choice1=='Ножницы') or (choice2 == 'Бумага' and choice1=='Камень'):
        bot.send_message(id_user2,f'Вы победили,{choice2} побеждает {choice1}')
        bot.send_message(id_user1,f'Вы проиграли,{choice2} побеждает {choice1}')
@bot.message_handler(commands=['my_id'])
def my_id(message):
    bot.send_message(message.chat.id,f'Ваш id:{message.from_user.id}')
bot.polling(non_stop=True, interval=0)