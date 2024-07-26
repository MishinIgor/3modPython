import telebot,requests
from transliterate import translit 
with open('token_15gr.txt') as f:
    TOKEN = f.read()
my_chatid = -4137666167
bot = telebot.TeleBot(TOKEN)
comands = ['id','погода','info','coffee']
text_comands = (',').join(comands)
@bot.message_handler(commands=comands)
def universal(message):
    if message.text == '/info':
        bot.send_message(my_chatid,f'Я умею выполнять команды: {text_comands}')
    elif message.text == '/id':
        bot.send_message(message.chat.id,f'Ваш айди: {message.from_user.id}')
        bot.send_message(message.chat.id,f'Айди чата: {message.chat.id}')
    elif message.text == '/погода':
        bot.send_message(my_chatid,'В каком городе хотите узнать погоду? Введите город с большой буквы')
        bot.register_next_step_handler(message,pogoda)
def pogoda(message):
    city = message.text
    cityen = translit(city, language_code='ru', reversed=True)
    #bot.send_message(my_chatid,f'Вы хотите узнать погоду в {cityen}. Пожалуйста подождите.')
    pogod = requests.get(f'https://goweather.herokuapp.com/weather/{cityen}')
    temperatura = pogod.json()['temperature']
    wind = pogod.json()['wind']
    bot.send_message(my_chatid,f'Погода в {city}, Температура: {temperatura}, Ветер: {wind}')
bot.polling(non_stop=True,interval=0)