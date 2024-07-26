# Пропишите функцию, которая при получении сообщения 
# пользователя дублирует текст сообщения пользователя 10 раз и отправляет обратным сообщением
import telebot,random #Импортиуем библиотеку для работы с ботами
with open('token_9gr.txt') as f:
    TOKEN = f.read() #Вводим токен в константу
bot = telebot.TeleBot(TOKEN) #Создаём переменную которая будет являться классом бота с токеном из константы

@bot.message_handler(content_types=['text'])
def eho(message):
    bot.send_message(message.chat.id,message.text*10)
bot.polling(non_stop=True, interval=0)