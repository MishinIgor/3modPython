import telebot,requests
from pogoda import *
with open('token_15gr.txt') as f:
    TOKEN = f.read()
my_chatid = -4137666167
bot = telebot.TeleBot(TOKEN)
comands = ['id','погода','info','coffee']
text_comands = (',').join(comands)

@bot.message_handler(commands=comands)
def universal(message):
    if message.text == '/info':
        bot.send_message(message.chat.id,f'Я умею выполнять команды: {text_comands}')
    elif message.text == '/id':
        bot.send_message(message.chat.id,f'Ваш айди: {message.from_user.id}')
        bot.send_message(message.chat.id,f'Айди чата: {message.chat.id}')
    elif message.text == '/coffee':
        r = requests.get('https://coffee.alexflipnote.dev/random.json').json()
        url_rand_coffee = r['file']
        bot.send_photo(message.chat.id,url_rand_coffee)
    elif message.text == '/погода':
        keyboard = telebot.types.ReplyKeyboardMarkup(row_width=1,resize_keyboard=True)
        button_geo = telebot.types.KeyboardButton(text = 'Поделиться местоположением', request_location=True)
        keyboard.add(button_geo)
        bot.send_message(message.chat.id,'Поделись местоположением',reply_markup=keyboard)
@bot.message_handler(content_types=['location'])
def pogoda(message):
    a = telebot.types.ReplyKeyboardRemove()
    bot.send_message(message.chat.id,weather_info(message.location.latitude,message.location.longitude),reply_markup=a)
bot.polling(non_stop=True,interval=0)