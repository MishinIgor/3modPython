#ДЗ: Необходимо написать бота, который по команде /coffee будет отправлять случайное фото кофе.

from transliterate import translit
import telebot,requests
with open('token_5gr.txt') as f:
    TOKEN = f.read()
bot = telebot.TeleBot(TOKEN)
comands = ['info','rand_cat','cat_text','rand_fox','rand_duck','rand_dog','погода','rand_coffee']
text_comands = '/'+(',/').join(comands)
@bot.message_handler(commands=comands)
def universal(message):
    if message.text == '/info':
        bot.send_message(message.chat.id,f'Я умею выполнять команды: {text_comands}')
    elif message.text == '/rand_cat':
        r = requests.get(f'https://cataas.com/cat?json=true')
        img = 'https://cataas.com/cat/' + r.json()['_id']
        bot.send_photo(message.chat.id,img)
    elif message.text == '/cat_text':
        bot.send_message(message.chat.id,'Введите текст для картинки')
        bot.register_next_step_handler(message,generate_cat)
    elif message.text == '/rand_fox':
        r = requests.get('https://randomfox.ca/floof/')
        img = r.json()['image']
        bot.send_photo(message.chat.id,img)
    elif message.text == '/rand_duck':
        r = requests.get('https://random-d.uk/api/random')
        img = r.json()['url']
        bot.send_photo(message.chat.id,img)
    elif message.text == '/rand_dog':
        r = requests.get('https://random.dog/woof.json')
        img = r.json()['url']
        bot.send_photo(message.chat.id,img)
    elif message.text == '/погода':
        bot.send_message(message.chat.id,'Введите город в котором хотите узнать погоду с большой буквы.')
        bot.register_next_step_handler(message,pogoda)
    elif message.text == '/rand_coffee':
        r = requests.get('https://coffee.alexflipnote.dev/random.json').json()
        url_rand_coffee = r['file']
        bot.send_photo(message.chat.id,url_rand_coffee)
def pogoda(message):
    city = message.text
    cityen = translit(city,language_code='ru',reversed=True)
    rezult = ''
    try:
        r = requests.get(f'https://goweather.herokuapp.com/weather/{cityen}')
        rezult = r.json()
        temp = rezult['temperature']
        wind = rezult['wind']
        wind = int(wind.split()[0])
        wind = str(round(wind*1000/3600,2)) +' м/c'
        rezult = f'Погода в городе {city}: Температура - {temp}, Скорость ветра - {wind}'
    except Exception:
        rezult = 'Ввели некорректные данные'

def generate_cat(message):
    try:
        r = requests.get(f'https://cataas.com/cat/says/{message.text}?json=true')
        img = 'https://cataas.com/cat/' + r.json()['_id'] + f'/says/{message.text}'
        bot.send_photo(message.chat.id,img)
    except Exception:
        bot.send_message(message.chat.id,'Не вводите знаки ?,!,/')
        bot.send_message(message.chat.id,'Введите повторно текст')
        bot.register_next_step_handler(message,generate_cat)
bot.polling(non_stop=True,interval=0)