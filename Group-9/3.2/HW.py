# Напишите код для бота, который при получение текстового сообщения, 
# в котором встречается слово ‘рандом’ (в любом месте) отправляет случайное число от 0 до 100, 
# в любом другом случае дублирует текст пользователя. Обязательно должно быть два разных хэндлера.
import telebot,random #Импортиуем библиотеку для работы с ботами
with open('token_9gr.txt') as f:
    TOKEN = f.read() #Вводим токен в константу
bot = telebot.TeleBot(TOKEN) #Создаём переменную которая будет являться классом бота с токеном из константы
@bot.message_handler(func = lambda x: 'рандом' in x.text.lower())
def add_random(message):
    bot.send_message(message.chat.id,f'Рандомное значение(0-100): {random.randint(0,100)}')
@bot.message_handler(content_types=['text'])
def eho(message):
    bot.send_message(message.chat.id,message.text)
bot.polling(non_stop=True, interval=0)