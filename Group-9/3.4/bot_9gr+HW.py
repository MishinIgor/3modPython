from transliterate import translit
import telebot, requests
with open('token_9gr.txt') as f:
    TOKEN = f.read()
bot = telebot.TeleBot(TOKEN)
comands = ['rand_fox','help','rand_duck','rand_dog','pogoda','rand_coffee']
text_comands = '/'+(', /').join(comands)
@bot.message_handler(commands=comands)
def universal(message):
    if message.text == '/help':
        bot.send_message(message.chat.id,f'Я умею выполнять команды {text_comands}')
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
    elif message.text == '/pogoda':
        bot.send_message(message.chat.id,'Введите город в котором хотите узнать погоду с большой буквы')
        bot.register_next_step_handler(message,pogoda)
    elif message.text == '/rand_coffee':
        r = requests.get('https://coffee.alexflipnote.dev/random.json').json()
        img = r['file']
        bot.send_photo(message.chat.id,img)
def pogoda(message):
    city = message.text
    cityen = translit(city,language_code='ru',reversed=True)
    rezult = ''
    try:
        r = requests.get(f'https://goweather.herokuapp.com/weather/{cityen}')
        rezult = r.json()
        temp = rezult['temperature']
        reztemp = int(temp.split()[0])
        if reztemp <0:
            reztemp = 'Оденьте шапку'
            img = 'https://elcontacto.ru/files/journal/original/1648586034_AdobeStock_173659966.jpeg'
        elif 0<reztemp<10:
            reztemp = 'Прохладно, наденьте плащ или куртку'
            img = 'https://sun9-29.userapi.com/impg/HACt-RgCznrQ6yxr6_yJpe_YvQHFRySCKB1bTQ/B14Ajs8peC8.jpg?size=1096x683&quality=95&sign=66d1a3ec0ffb5a27909f859be4fabd5e&c_uniq_tag=BgsnqQHMZMmn39FCJTJZhQRghCzqN38c3XzoWpRmuuY&type=album'
        elif 10<reztemp<20:
            reztemp = 'Холодный ветер, оденьте кофту или ветровку с флисом'
            img = 'https://www.lrt.lt/img/2020/05/19/655863-866729-1287x836.jpg'
        elif 20<reztemp<30:
            img = 'https://www.summeridgeanimalclinic.com/blog/wp-content/uploads/2014/07/Summer-Cat.jpg'
            reztemp = 'В такую погоду можно гулять в футболке'
        wind = rezult['wind'] # изначально в км/ч
        wind = int(wind.split()[0])
        wind = str(round(wind*1000/3600,2)) +' м/c'
        bot.send_photo(message.chat.id,img)
        rezult = f'Погода в городе {city}: Температура - {temp}, Скорость ветра - {wind}. {reztemp}'
    except Exception as exc:
        rezult = f'Ввели некорректные данные, попробуйте ввести ещё раз. Ошибка {exc}, {r.status_code}'
        bot.register_next_step_handler(message,pogoda)
    bot.send_message(message.chat.id,rezult)
bot.polling(non_stop=True,interval=0)