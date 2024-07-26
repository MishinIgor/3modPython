import telebot
TOKEN = '7206858358:AAHk4AEodxlR0CEt9GNf1250jO7JZgDYBSk' # В файле записан только токен бота
in_valuta = ''
out_valuta = ''
all_many = ''
out_many = 0
bot = telebot.TeleBot(TOKEN)
VALUTA = { # Переведите 135 рублей в Тенге. 
    'ХлебКойн': 1,
    "Рубли": 88,
    "Доллар": 3,
    "Евро": 4,
    "Тенге": 478
}
inform_str = ''
for i,j in VALUTA.items():
    inform_str += ' ' +str(i) + ' - ' + str(j)+';' 
name_valuta = (',').join(list(VALUTA.keys()))
@bot.message_handler(commands=['обмен','валюта'])
def start(message):
    if message.text == '/валюта':
        bot.send_message(message.from_user.id,f'{inform_str} - вся валюта представлена в видете стоимости за ХлебКойн')
    elif message.text == '/обмен':
        bot.send_message(message.from_user.id,f'Какая у Вас валюта из перечисленной: {name_valuta}')
        bot.register_next_step_handler(message,out_value)
def out_value(message):
    global in_valuta
    in_valuta = message.text
    bot.send_message(message.from_user.id,f'В какую валюту из перечисленного будем переводить: {name_valuta}')
    bot.register_next_step_handler(message,add_many)
def add_many(message):
    global out_valuta
    out_valuta = message.text
    bot.send_message(message.from_user.id,f'Вы хотите перевести {in_valuta} в {out_valuta}')
    bot.send_message(message.from_user.id,f'Введите количество валюты которое хотите перевести')
    bot.register_next_step_handler(message,raschet)
def raschet(message):
    global all_many
    all_many = 0
    try:
        all_many = int(message.text)
        out_many = (all_many/VALUTA[in_valuta])*VALUTA[out_valuta]
        bot.send_message(message.from_user.id,f'За {all_many} {in_valuta}, вы получите {out_many} {out_valuta}')
    except Exception:
        bot.send_message(message.chat.id,'Введите кооректный тип данных')
        bot.register_next_step_handler(message,raschet)
@bot.message_handler(content_types=['text','sticker','voice'])
def start(message):
    bot.send_message(message.from_user.id,'Если хотите узнать курс валют введите /валюта, если хотите обменять введите /обмен')
bot.polling(non_stop=True, interval=0)