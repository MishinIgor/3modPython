# Постановка задачи: 
# Напишите код для бота, который при получение текстового сообщения, 
# в котором встречается слово ‘рандом’ (в любом месте) отправляет случайное число от 0 до 100, 
# в любом другом случае дублирует текст пользователя. Обязательно должно быть два разных хэндлера.

import telebot,random
with open('token_5gr.txt') as f:
    TOKEN = f.read() # В файле записан только токен бота 

bot = telebot.TeleBot(TOKEN)

@bot.message_handler(func = lambda x: 'рандом' in x.text.lower())
def say_random(message):
    bot.send_message(message.chat.id,f'Рандомное значение: {random.randint(0,100)}')
@bot.message_handler(content_types=['text'])
def messx10(message):
    bot.send_message(message.chat.id,message.text)

bot.polling(non_stop=True, interval=0)