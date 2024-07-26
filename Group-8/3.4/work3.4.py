import requests,telebot,random
with open('token_8gr.txt') as f:
    TOKEN = f.read()
bot = telebot.TeleBot(TOKEN)

# r = requests.get('https://goweather.herokuapp.com/weather/Samara')
@bot.message_handler(commands=['погода'])
def city(message):
    bot.send_message(message.chat.id,'Скажите в каком городе хотите узнать погоду? Введите город транслитом с большой буквы')
    bot.register_next_step_handler(message,pogoda)
def pogoda(message):
    try:
        p = requests.get(f'https://goweather.herokuapp.com/weather/{message.text}')
        bot.send_message(message.chat.id,p.json()['temperature'])
    except Exception:
        bot.send_message(message.chat.id,'Вы ввели некорректные данные')
        
bot.polling(non_stop=True, interval=0)