#ДЗ: Внимательно изучите API https://coffee.alexflipnote.dev/ 
#Необходимо написать бота, который по команде /coffee будет отправлять случайное фото кофе.

with open('token_9gr.txt') as f:
    TOKEN = f.read()
from weather import *
import telebot, requests
bot = telebot.TeleBot(TOKEN)
comands = ['help','pogoda_loc','my_loc']
text_comands = '/'+(', /').join(comands)
@bot.message_handler(commands=comands)
def universal(message):
    if message.text == '/help':
        bot.send_message(message.chat.id,f'Я умею выполнять команды {text_comands}')
    elif message.text == '/pogoda_loc':
        bot.send_message(message.chat.id,'Введите через запятую долготу и широту. Например: 123.51, -12.12')
        bot.register_next_step_handler(message,pogoda)
    elif message.text == '/my_loc':
        keyboard = telebot.types.ReplyKeyboardMarkup(row_width=1,resize_keyboard=True)
        button_geo = telebot.types.KeyboardButton(text='Поделиться местополжоением',request_location=True)
        keyboard.add(button_geo)
        bot.send_message(message.chat.id,'Поделиться местоположением',reply_markup=keyboard)
def pogoda(message):
    lat = ((message.text).split(',')[0]).replace(' ', '')
    lon = ((message.text).split(',')[1]).replace(' ', '')
    bot.send_message(message.chat.id,info_weather(lat,lon))
    bot.send_location(message.chat.id,lat,lon)
    if drop_info(lat,lon)['Температура'] > 35:
        bot.send_photo(message.chat.id,'https://avatars.mds.yandex.net/get-entity_search/2331707/844211852/orig')
        bot.send_message(message.chat.id,'Если не хотите умереть в этом месте, запасайтесь водой срочно!')
    if drop_info(lat,lon)['Скорость ветра'] > 10:
        bot.send_photo(message.chat.id,'https://www.funnyart.club/uploads/posts/2022-12/thumbs/1672159029_www-funnyart-club-p-silnii-veter-prikol-yumor-59.jpg')
        bot.send_message(message.chat.id,'Надеюсь твой попросёнок построил дом из керпича, иначе его сдует...')   
@bot.message_handler(content_types=['location'])
def weather_loc(message):
    a = telebot.types.ReplyKeyboardRemove()
    bot.send_message(message.chat.id,info_weather(message.location.latitude,message.location.longitude),reply_markup=a)
bot.polling(non_stop=True,interval=0)