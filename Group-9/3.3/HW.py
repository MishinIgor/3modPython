# Создать бота, который из сообщения пользователя будет создавать опрос. 
# Первая строка сообщения пользователя - вопрос, 2 - 11 строки - варианты ответов. 
# Если сообщение пользователя менее 3 строк или более 11, то выводить соответствующее сообщение. 
import telebot,random #Импортиуем библиотеку для работы с ботами

with open('token_9gr.txt') as f:
    TOKEN = f.read()

bot = telebot.TeleBot(TOKEN) #Создаём переменную которая будет являться классом бота с токеном из константы
mychat_id = -4230070784
@bot.message_handler(content_types=['text'])
def oprosnik(message):
    opros = (message.text).split('\n')
    if 2<len(opros)<12:
        bot.send_poll(mychat_id,opros[0],opros[1:])
    else:
        bot.send_message(message.chat.id,'Не могу создать опрос по вашему сообщению')
bot.polling(non_stop=True, interval=0)