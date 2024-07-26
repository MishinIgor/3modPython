import telebot,random

with open('token_15gr.txt') as f:
    TOKEN = f.read() # Тут будем хранить наш токен

bot = telebot.TeleBot(TOKEN)

# "text" - текст
# "audio" - аудио
# "document" - файл
# "photo" - фото
# "sticker" - стикер
# "video" - видео
# "video_note" - кружок
# "voice" - аудиосообщение
# "location" - местоположение
# "contact" - контакт
# "new_chat_members" - присоединение к чату нового пользователя
# "left_chat_member" - отсоединение от чата пользователя
# "new_chat_title" - новое название чата
# "new_chat_photo" - новое фото чата
# "delete_chat_photo" - удаление фото чата
# "group_chat_created" - создание чата
# "chanal_chat_created" - создание канала
# "pinned_message" - закрепление сообщения
@bot.message_handler(func = lambda x: x.text.lower() in ["привет", "здравствуй", "добрый день"])
def say_hello(message):
    bot.send_message(message.chat.id,random.choice(['Привет :)', "ЗдравствуйтЭ ^_^", "Хлеб брать будешь?"]))
@bot.message_handler(commands=['help'])
def help(message):
    text = '''
    Я поддерживаю следующие команды:
    /start - Вывод приветствия
    /get_info - информация о пользователе
    /help - Помощь(то, что вы видите сейчас. Не много, но как есть.)
    '''
    bot.send_message(message.chat.id,text)
@bot.message_handler(commands=['get_info']) # chat.id, username, second_name,first_name
def get_info(message):
    text = '''Я могу дать информацию по:
    1) chat.id - айди чата;
    2) username - никнейм пользователя;
    3) first_name - имя пользователя;
    4) last_name - фамилия пользователя.
    Выберите необходимый вариант, и напишите в сообщение название варианта
    '''
    send = bot.send_message(message.chat.id,text)
    bot.register_next_step_handler(send,info)
def info(message):
    if message.text == 'chat.id':
        bot.send_message(message.chat.id,message.chat.id)
    elif message.text == 'username':
        bot.send_message(message.chat.id,message.from_user.username)
    elif message.text == 'last_name':
        bot.send_message(message.chat.id,message.from_user.last_name)
    elif message.text == 'first_name':
        bot.send_message(message.chat.id,message.from_user.first_name)
    else:
        bot.send_message(message.chat.id,'На данный момент я могу дать информацию по chat.id,username,last_name,first_name')
@bot.message_handler(commands=['start'])
def start(message):
    bot.send_message(message.chat.id,f'Добрый день, {message.from_user.username}')
@bot.message_handler(content_types=['sticker'])
def get_sticker(message):
    bot.send_message(message.chat.id,f'Инфо по стикеру(emoji): {message.sticker.emoji}')
@bot.message_handler(content_types=['pinned_message'])
def pin(message):
    bot.send_message(message.chat.id,f'СРОЧНО ТРЕБУЕТСЯ ВНИМАНИЕ! ПОЯВИЛСЯ ЗАКРЕП! ОТ {message.from_user.first_name}')
@bot.message_handler(content_types=['document','photo'])
def poluchalka(message):
    bot.send_message(message.chat.id,'ПОЛУЧЕНА СВЕРХ СЕКРЕТНАЯ И ВАЖНАЯ ИНФОРМЕЙШН')
@bot.message_handler(content_types=['text'])
def all_in(message):
    bot.send_message(message.chat.id,'Ну вот и всё, планета захвачена')
bot.polling(non_stop=True, interval=0)