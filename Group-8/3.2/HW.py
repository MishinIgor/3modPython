# Напишите код для бота, который при получение текстового сообщения, 
# в котором встречается слово ‘рандом’ (в любом месте) отправляет случайное число от 0 до 100, 
# в любом другом случае дублирует текст пользователя. Обязательно должно быть два разных хэндлера.

import telebot,random

with open('token_8gr.txt') as f:
    TOKEN = f.read() # Тут мы помещаем токен в константу
bot = telebot.TeleBot(TOKEN)

@bot.message_handler(func=lambda msg: "рандом" in msg.text.lower()) 
def random_handler(msg):
    bot.send_message(msg.chat.id,f'Рандомное значение 0-100: {random.randrange(101)}')

@bot.message_handler(content_types = 'text')
def main(message):
    bot.send_message(message.chat.id, message.text)

bot.polling(non_stop=True, interval=0)