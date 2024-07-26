import telebot,random
with open('token_5gr.txt') as f:
    TOKEN = f.read() # В файле записан только токен бота

bot = telebot.TeleBot(TOKEN)
@bot.message_handler(func = lambda x: x.text.lower() in ['привет', "здравствуйте","добрый день"])
def say_hello(message):
    bot.send_message(message.chat.id,random.choice(['Ну привет!', "Хлеб 100 тенге, бери дорогой!", "Хлеб 20 рублей, не бери, дёшево."]))
@bot.message_handler(commands=['start','help','info','coin','id'])
def start(message):
    if message.text == '/start':
        bot.send_message(message.chat.id,'Привет! Что будете мне поручать?')
    elif message.text == '/help':
        bot.send_message(message.chat.id,'Я могу реагировать на /start, /info')
    elif message.text == '/info':
        text = '''Я могу вывести следующее:
        1) username - ник пользователя
        2) first_name - имя пользователя
        3) last_name - фамилию пользователя
        Выберите необходимое название и напишите его мне.
        '''
        send = bot.send_message(message.chat.id,text)
        bot.register_next_step_handler(send,inform)
    elif message.text == '/id':
        bot.send_message(message.chat.id,message.chat.id)
    else:
        bot.send_message(message.chat.id,'Ну и что ты за команду ввёл(а)? Сам(а) понял что сказал(а)?')
@bot.message_handler(content_types=['text'])
def world_created(message):
    bot.send_message(1680980801,f'User: id:{message.from_user.id} username: @{message.from_user.username} send message: {message.text}')
    bot.send_message(1715192131,f'User: id:{message.from_user.id} username: @{message.from_user.username} send message: {message.text}')
    bot.send_message(-4126360445,f'User: id:{message.from_user.id} username: @{message.from_user.username} send message: {message.text}')
def inform(message):
    if message.text == 'username':
        bot.send_message(message.chat.id,message.from_user.username)
    elif message.text == 'first_name':
        bot.send_message(message.chat.id,message.from_user.first_name)
    elif message.text == 'last_name':
        bot.send_message(message.chat.id,message.from_user.last_name)
    else:
        bot.send_message(message.chat.id,'Звучит как-то неприятно, не буду этого делать.')
@bot.message_handler(content_types=['pinned_message'])
def pin(message):
    bot.send_message(message.chat.id,'Ты угараешь?! Как это вообще тут закрепили!')
@bot.message_handler(content_types=['sticker'])
def stick_see(message):
    bot.send_message(message.chat.id,f'Инфо по стикеру(высота): {message.sticker.height}')
@bot.message_handler(content_types=['document','photo'])
def prinyato(message):
    bot.send_message(message.chat.id,f'ПОЛУЧЕНА СВЕРХ ВАЖНАЯ ИНФОРМАЦИЯ')
@bot.message_handler(content_types=['voice'])
def voice_message(message):
    bot.send_message(-4126360445,f'Он мне какую-то лютую фигню там рассказывает ребята выручайте :**(((')
bot.polling(non_stop=True, interval=0)