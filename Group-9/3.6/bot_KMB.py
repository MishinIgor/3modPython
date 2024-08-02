import telebot
with open('token_5gr.txt') as f:
    TOKEN = f.read() # В файле записан только токен бота
choice1, choice2 = '', ''
chat_id = 0

# Создание экземпляра бота с использованием токена
bot = telebot.TeleBot(TOKEN)
user_id1,user_id2 = 0, 0

# Создание клавиатуры для выбора в игре
keyboard_game = telebot.types.ReplyKeyboardMarkup(resize_keyboard=True)
keyboard_game.add('Камень', "Ножницы", "Бумага")


# Клавиатура для ответа на предложение сыграть
keyboard_ans = telebot.types.ReplyKeyboardMarkup(resize_keyboard=True)
keyboard_ans.add('Да',"Нет")

# Словарь для хранения состояния игр
# Ключом является идентификатор чата, значением - состояние игры
games = {}

@bot.message_handler(commands=['game', 'id'])
def start(message):
    """
    Обрабатывает команды /game и /id.
    При команде /game запрашивает ID оппонента для начала игры.
    При команде /id отправляет пользователю его ID.
    """
    global chat_id
    chat_id = message.chat.id  # Идентификатор чата, где была отправлена команда
    if message.text == '/game':
        global user_id1
        bot.send_message(message.chat.id,'С кем хотите сыграть? Введие id пользователя')
        user_id1 = message.from_user.id
        bot.register_next_step_handler(message,get_ans)
        bot.send_message(chat_id, 'С кем хотите сыграть? Введите ID пользователя:')
        bot.register_next_step_handler(message, get_opponent_id)
    elif message.text == '/id':
        bot.send_message(message.chat.id,f'Ваш id: {message.from_user.id}')
def get_ans(message):
    global user_id2
    user_id2 = int(message.text)
    send = bot.send_message(user_id2,f"С вами хочет сыграть пользователь @{message.from_user.username}.Хотите с ним сыграть?")
    bot.register_next_step_handler(send,go_play)
def go_play(message):
    global user_id1,user_id2,chat_id
    bot.send_message(chat_id, f'Ваш ID: {message.from_user.id}')

def get_opponent_id(message):
    """
    Получает ID оппонента от пользователя.
    Проверяет, что ID корректен и не равен собственному ID.
    Инициализирует состояние игры и отправляет запрос оппоненту.
    """
    chat_id = message.chat.id  # Идентификатор чата
    user_id1 = message.from_user.id  # ID отправителя сообщения
    try:
        user_id2 = int(message.text)  # Преобразование введенного ID в целое число
        if user_id2 == user_id1:
            bot.send_message(chat_id, 'Вы не можете играть сами с собой!')
            return
        # Инициализация состояния игры в словаре games
        games[chat_id] = {
            'user_id1': user_id1,
            'user_id2': user_id2,
            'choice1': '',  # Выбор первого игрока
            'choice2': '',  # Выбор второго игрока
            'status': 'waiting_for_response'  # Статус игры: ожидание ответа оппонента
        }
        # Отправка запроса на игру второму игроку
        send_message = bot.send_message(user_id2, f"С вами хочет сыграть пользователь @{message.from_user.username}. Хотите с ним сыграть?")
        print(f"Отправлено сообщение пользователю {user_id2}: {send_message.text}")  # Отладочное сообщение
        # Регистрация следующего шага для ответа от оппонента
        bot.register_next_step_handler_by_chat_id(user_id2, lambda msg: go_play(msg, chat_id))
    except ValueError:
        bot.send_message(chat_id, 'Пожалуйста, введите корректный ID пользователя.')

def go_play(message, chat_id):
    """
    Обрабатывает ответ оппонента на запрос игры.
    Если оппонент согласен, начинает игру и запрашивает выбор.
    Если отказался, удаляет данные игры.
    """
    if chat_id not in games:
        bot.send_message(message.chat.id, 'Игра не найдена.')
        return

    user_id1 = games[chat_id]['user_id1']  # ID первого игрока
    user_id2 = games[chat_id]['user_id2']  # ID второго игрока

    if message.from_user.id == user_id2:
        if message.text == 'Да':
            bot.send_message(user_id1,'Пользователь согласился сыграть')
            bot.send_message(user_id1,'Сделайте свой выбор', reply_markup=keyboard_game)
            bot.send_message(user_id2,'Сделайте свой выбор', reply_markup=keyboard_game)
            bot.register_next_step_handler(message,result)
            games[chat_id]['status'] = 'in_progress'  # Изменение статуса на "в процессе"
            bot.send_message(user_id1, 'Пользователь согласился сыграть.')
            bot.send_message(user_id1, 'Сделайте свой выбор:', reply_markup=keyboard_game)
            bot.send_message(user_id2, 'Сделайте свой выбор:', reply_markup=keyboard_game)
            # Регистрация следующего шага для обоих игроков
            bot.register_next_step_handler_by_chat_id(user_id1, lambda msg: result(msg, chat_id))
            bot.register_next_step_handler_by_chat_id(user_id2, lambda msg: result(msg, chat_id))
        elif message.text == 'Нет':
            bot.send_message(user_id1, 'Пользователь не хочет играть с вами.')
            del games[chat_id]  # Удаление данных игры, так как игрок отказался
        else:
            bot.send_message(user_id1,'Пользователь не хочет играть с вами')
            bot.send_message(message.chat.id, 'Пожалуйста, ответьте "Да" или "Нет".')
            bot.register_next_step_handler(message, lambda msg: go_play(msg, chat_id))
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
        bot.send_message(message.chat.id, f'Не спамьте, пожалуйста. Мы ждём ответ от пользователя с ID {user_id2}.')
        bot.register_next_step_handler(message, lambda msg: go_play(msg, chat_id))

def result(message, chat_id):
    """
    Обрабатывает выбор игроков и определяет результат игры.
    Отправляет результаты обеим сторонам и удаляет данные игры после завершения.
    """
    if chat_id not in games:
        bot.send_message(message.chat.id, 'Игра не найдена.')
        return

    user_id1 = games[chat_id]['user_id1']  # ID первого игрока
    user_id2 = games[chat_id]['user_id2']  # ID второго игрока
    choice1 = games[chat_id]['choice1']  # Выбор первого игрока
    choice2 = games[chat_id]['choice2']  # Выбор второго игрока

    # Проверка, что игра находится в статусе "в процессе"
    if games[chat_id]['status'] != 'in_progress':
        bot.send_message(message.chat.id, 'Игра не активна. Пожалуйста, начните новую игру.')
        return

    # Обработка выбора первого игрока
    if message.from_user.id == user_id1:
        if not choice1:
            games[chat_id]['choice1'] = message.text
            bot.send_message(message.chat.id, 'Ваш выбор записан.')
            print(f"Выбор игрока {user_id1}: {message.text}")  # Отладочное сообщение
    # Обработка выбора второго игрока
    elif message.from_user.id == user_id2:
        if not choice2:
            games[chat_id]['choice2'] = message.text
            bot.send_message(message.chat.id, 'Ваш выбор записан.')
            print(f"Выбор игрока {user_id2}: {message.text}")  # Отладочное сообщение

    # Обновление состояния игры с выбором обоих игроков
    choice1 = games[chat_id]['choice1']
    choice2 = games[chat_id]['choice2']

    if not choice1 or not choice2:
        bot.send_message(message.chat.id, 'Ожидание выбора другого пользователя...')
        bot.register_next_step_handler(message, lambda msg: result(msg, chat_id))
    else:
        if choice2 == choice1:
            bot.send_message(user_id1,'Ничья')
            bot.send_message(user_id2,'Ничья')
        elif (choice1=='Ножницы' and choice2=='Бумага') or (choice1=='Камень' and choice2=='Ножницы') or (choice1=='Бумага' and choice2=='Камень'):
            bot.send_message(user_id1,f'Победа!, соперник выбрал {choice2}')
            bot.send_message(user_id2,f'Поражение!, соперник выбрал {choice1}')
        # Определение результата игры
        if choice1 == choice2:
            bot.send_message(user_id1, 'Ничья!')
            bot.send_message(user_id2, 'Ничья!')
        elif (choice1 == 'Ножницы' and choice2 == 'Бумага') or \
             (choice1 == 'Камень' and choice2 == 'Ножницы') or \
             (choice1 == 'Бумага' and choice2 == 'Камень'):
            bot.send_message(user_id1, f'Победа! Соперник выбрал {choice2}')
            bot.send_message(user_id2, f'Поражение! Соперник выбрал {choice1}')
        else:
            bot.send_message(user_id2,f'Победа!, соперник выбрал {choice1}')
            bot.send_message(user_id1,f'Поражение!, соперник выбрал {choice2}')
            bot.send_message(user_id2, f'Победа! Соперник выбрал {choice1}')
            bot.send_message(user_id1, f'Поражение! Соперник выбрал {choice2}')

        # Удаление данных игры после завершения
        del games[chat_id]

# Запуск бота. Он будет работать в бесконечном цикле и обрабатывать сообщения.
bot.polling(non_stop=True, interval=0)