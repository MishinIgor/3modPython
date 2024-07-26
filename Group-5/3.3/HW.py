# Создать бота, который из сообщения пользователя будет создавать опрос. 
# Первая строка сообщения пользователя - вопрос, 2 - 11 строки - варианты ответов. 
# Если сообщение пользователя менее 3 строк или более 11, то выводить соответствующее сообщение. 

import telebot,random
with open('token_5gr.txt') as f:
    TOKEN = f.read()
bot = telebot.TeleBot(TOKEN)
mychat_id = -4126360445
@bot.message_handler(content_types=['text'])
def oprosik(message):
    text = message.text
    text = text.split('\n')
    if 2<len(text)<=11:
        bot.send_poll(mychat_id,text[0],text[1:])
        bot.send_poll(message.chat.id,text[0],text[1:])
    else:
        bot.send_message(message.chat.id,'Введите сообщение в котором от 3 до 11 строк')
bot.polling(non_stop=True, interval=0)