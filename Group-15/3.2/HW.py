# Напишите код для бота, который при получение текстового сообщения, в котором встречается слово 
# ‘рандом’ (в любом месте) отправляет случайное число от 0 до 100, 
# в любом другом случае дублирует текст пользователя. Обязательно должно быть два разных хэндлера.
import telebot,random

with open('token_15gr.txt') as f:
    TOKEN = f.read() # Тут будем хранить наш токен

bot = telebot.TeleBot(TOKEN)

@bot.message_handler(func = lambda x: "рандом" in x.text.lower())
def randomize(message):
    bot.send_message(message.chat.id,f'рандомное значение: {random.randint(0,100)}')
@bot.message_handler(content_types=['text'])
def echo(message):
    bot.send_message(message.chat.id,message.text)
bot.polling(non_stop=True, interval=0)