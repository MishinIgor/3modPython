import telebot,random

with open('token_8gr.txt') as f:
    TOKEN = f.read() # Тут мы помещаем токен в константу
bot = telebot.TeleBot(TOKEN)

# 'text' - текстовые
# 'audio' - аудио
# 'document' - файл
# 'photo' - фото
# 'sticker' - стикеры
# "video" - видео
# "video_note" - кружочек
# "voice" - аудиосообщение
# "location" - местоположение
# "contact" - контакты
# "new_chat_members" - присоединение к чату нового пользователя
# "left_chat_member" - отсоединение пользователя от чата
# "new_chat_title" - новое название чата
# "delete_chat_photo" - удаление фото чата
# "group_chat_created" - создание чата
# "channel_chat_created" - создание канала
# "pinned_message" - закрепление сообщения
@bot.message_handler(func=lambda x: x.text.lower() in ['привет', "здравствуй", "добрый день"])
def say_hello(message):
    bot.send_message(message.chat.id, random.choice(['Привет :)', "Здравствуй О_О", "Добрый день ^_^"]))
@bot.message_handler(commands=['get_info'])
def func_bot(message):
    send = bot.send_message(message.chat.id,'Что именно вы хотите узнать? \n first_name - Ваше имя, \n username - Ваш ник \n last_name - Ваша фамилия')
    bot.register_next_step_handler(send,info)
@bot.message_handler(commands=['start','help'])
def start(message):
    if message.text == '/start':
        bot.send_message(message.chat.id,f'Добрый день, {message.from_user.username}. И чего это вы мне тут спамите?')
    else:
        bot.send_message(message.chat.id,'Вы вводите устаревшие данные. Для начала работы введите /start')
@bot.message_handler(content_types=['sticker'])
def get_sticker(message):
    bot.send_message(message.chat.id,message.sticker.width)
@bot.message_handler(content_types=['pinned_message'])
def pin(message):
    bot.send_message(message.chat.id,f'{message.from_user.id} - что-то закрепили')
@bot.message_handler(content_types=['text'])
def info(message):
    if message.text == 'first_name':
        bot.send_message(message.chat.id,f'first_name: {message.from_user.first_name}')
    elif message.text == 'username':
        bot.send_message(message.chat.id,f'username: {message.from_user.username}') 
    elif message.text == 'last_name':
        bot.send_message(message.chat.id,f'last_name: {message.chat.id,message.from_user.last_name}')
    else:
        bot.send_message(message.chat.id,f'Моя твоя не понимать, лучше введи: first_name, last_name, username')
@bot.message_handler(content_types=['photo','document'])
def get_file(message):
    bot.send_message(message.chat.id,f'Получены сверх секретнные данные')


bot.polling(non_stop=True, interval=0)

