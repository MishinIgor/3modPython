# Создать бота, который из сообщения пользователя будет создавать опрос. 
# Первая строка сообщения пользователя - вопрос, 2 - 11 строки - варианты ответов. 
# Если сообщение пользователя менее 3 строк или более 11, то выводить соответствующее сообщение.
import telebot,random

with open('token_15gr.txt') as f:
    TOKEN = f.read() # Тут будем хранить наш токен

bot = telebot.TeleBot(TOKEN)

@bot.message_handler(content_types=['text'])
def opros(message):
    soobshenie = (message.text).split()
    que = soobshenie[0]
    ans = soobshenie[1:]
    if 2<len(soobshenie)<12:
        bot.send_poll(message.chat.id,que,ans)
    else:
        bot.send_message(message.chat.id,'Вы создаёте опрос. Введите от 3 до 11 строк. 1 строка вопрос, остальные ответ')
bot.polling(non_stop=True, interval=0)