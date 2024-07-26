import telebot,random #Импортиуем библиотеку для работы с ботами
with open('token_9gr.txt') as f:
    TOKEN = f.read() #Вводим токен в константу
bot = telebot.TeleBot(TOKEN) #Создаём переменную которая будет являться классом бота с токеном из константы
mychat_id = -4230070784
# "text" - текст
# "audio" - аудио
# "document" - файл
# "photo" - фото
# "sticker" - стикеры
# "video" - видео
# "video_note" - кружки
# "voice" - голосовое сообщение
# "location" - местоположение
# "contact" - контакт
# "new_chat_members" - присоединение нового пользователя к чату
# "left_chat_members" - отсоединение нового пользователя от чата
# "new_cht_title" - новое название чата
# "new_chat_photo" - новое фото чата
# "delete_chat_photo" - удаление фото чата
# "group_chat_created" - создание нового чата
# "channel_chat_created" - создание нового канала
# "pinned_message" - заклеплённое сообщение
@bot.message_handler(func = lambda x: x.text.lower() in ['привет',"здравствуй", "добрый день"])
def say_hello(message):
    bot.send_message(message.chat.id,random.choice(['Привет! Хлеб 20 рублей, бери!', "Хлеб уже 25 рублей, будешь брать?", "Я уже продал весь хлеб, умирай голодным"]))
@bot.message_handler(commands=['start','help','info','id'])
def start(message):
    if 'start' in message.text:
        bot.send_message(message.chat.id,'Привет! Ты запустил своего первого бота')
    elif 'help' in message.text:
        bot.send_message(message.chat.id,'Я поддерживаю команды /start, /help, /info')
    elif message.text == '/id':
        bot.send_message(message.chat.id,f'Ваш id: {message.from_user.id}')
        bot.send_message(message.chat.id,f'Айди чата в котором вы пишите: {message.chat.id}')
    elif 'info' in message.text:
        text = '''Я могу вывести следующу информацию:
        is_bot - является ли пользователь ботом
        first_name - имя пользователя
        last_name - фамилия пользователя
        username - ник пользователя
        '''
        bot.send_message(message.chat.id,text)
        bot.register_next_step_handler(message,inform)
    else:
        bot.send_message(message.chat.id,'Это сообщение никогда не выводится')
def inform(message):
    if message.text == 'is_bot':
        bot.send_message(message.chat.id,f'Проверка пользователя на бота: {message.from_user.is_bot}')
    elif message.text == 'first_name':
        bot.send_message(message.chat.id,f'Имя пользователя: {message.from_user.first_name}')
    elif message.text == 'last_name':
        bot.send_message(message.chat.id,f'Фамилия пользователя: {message.from_user.last_name}')
    elif message.text == 'username':
        bot.send_message(message.chat.id,f'Никнейм пользователя: {message.from_user.username}')
    else:
        bot.send_message(message.chat.id,'Звучит как-то не приятно, я этого делать не буду')
@bot.message_handler(content_types=['document'])
def my_doc(message):
    bot.send_message(message.chat.id,'ОГО! Сверх секретные данные!')
@bot.message_handler(content_types=['photo'])
def my_photo(message):
    bot.send_message(message.chat.id,'Вау! Крутая фотка!'*2)
    bot.send_message(message.chat.id,'А это вы где так?')
    bot.send_message(message.chat.id,'А это вы где так?')
@bot.message_handler(content_types=['location','voice','contact'])
def ogogoshka(message):
    bot.send_message(message.chat.id,'Мне не хватит на билеты')
    bot.send_message(message.chat.id,'Говорите громче, вас не слышно')
    bot.send_message(message.chat.id,'У меня 0 на балансе, сам набери.')
@bot.message_handler(content_types=['text','sticker'])
def helper(message):
    #bot.send_message(1668071582,f'Привет Артём! Тут мне пишут для тебя эти пользователи: username: @{message.from_user.username} id: {message.from_user.id} first_name: {message.from_user.first_name}')
    bot.send_message(mychat_id,f'Привет Чатик! Тут мне пишут для вас эти пользователи: username: @{message.from_user.username} id: {message.from_user.id} first_name: {message.from_user.first_name}')
@bot.message_handler(content_types=['voice'])
def reaction(message):
    bot.send_message(mychat_id,'Ребятаааа, он такое мне тут сказал не поверите!')
bot.polling(non_stop=True, interval=0)