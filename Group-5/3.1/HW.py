import telebot
with open('token_5gr.txt') as f:
    TOKEN = f.read() # В файле записан только токен бота

bot = telebot.TeleBot(TOKEN)

@bot.message_handler(content_types=['text'])
def messx10(message):
    bot.send_message(message.chat.id,(message.text)*10)

bot.polling(non_stop=True, interval=0)