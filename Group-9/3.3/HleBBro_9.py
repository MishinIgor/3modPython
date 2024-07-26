import telebot,random #Импортиуем библиотеку для работы с ботами
with open('token_9gr.txt') as f:
    TOKEN = f.read() #Вводим токен в константу
bot = telebot.TeleBot(TOKEN) #Создаём переменную которая будет являться классом бота с токеном из константы
mychat_id = -4230070784
@bot.message_handler(commands=['отправка'])
def otprafka(message):
    if message.from_user.id == 1680980801:
        with open('test.txt','r',encoding='utf-8') as file:
            bot.send_message(mychat_id,file.read())
            
@bot.message_handler(content_types=['text'])
def user_add(message):
    with open('test.txt','a',encoding='utf-8') as file:
        text = f'Пользователь @{message.from_user.username} с id {message.from_user.id} создал сообщение: {message.text} \n'
        file.write(text)
bot.polling(non_stop=True, interval=0)