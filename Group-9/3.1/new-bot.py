import telebot #Импортиуем библиотеку для работы с ботами

with open('token_9gr.txt') as f:
    TOKEN = f.read() #Вводим токен в константу
from_value = ''
out_value = ''
how_value = 0
rezult = 0
bot = telebot.TeleBot(TOKEN) #Создаём переменную которая будет являться классом бота с токеном из константы
VALUTA = { #Стоимость реализуется переводом из ХлебКойна в необходимую валюту. 
    "ХлебКойн": 1,
    "Рубль": 88,
    "Доллар": 192,
    "Евро": 395,
    "Тенге": 100
} #Нужно обменять 500 рублей в Тенге. Какой результат? 1250, т. к. 500*ТЕНГЕ(VALUE)/РУБЛЬ(VALUE)
name_valuts = (', ').join(list(VALUTA.keys()))
valuts = ''
for i,j in VALUTA.items():
    valuts += i+' - '+str(j)+'\n'
@bot.message_handler(content_types=['text']) #создаём реакцию на ввод текстового сообщения
def start(message): #Пишем функцию, аргументом которого будет являться сообщение от пользователя
    if message.text == '/обмен':
        bot.send_message(message.from_user.id,f'Введите точное название валюты которую хотите обменять: {name_valuts}') #Бот печатает сообщение юзеру который ему пишет
        bot.register_next_step_handler(message,in_value)
    elif message.text == '/инфо':
        bot.send_message(message.from_user.id,f'{valuts}')
    else:
        bot.send_message(message.from_user.id,'Для информации по курсу валют, введите /инфо, для обмена введите /обмен')
def in_value(message):
    global from_value
    from_value = message.text
    bot.send_message(message.from_user.id,f'Введите точное название валюты которую хотите получить: {name_valuts}')
    bot.register_next_step_handler(message,how_many)
def how_many(message):
    global out_value
    out_value = message.text
    bot.send_message(message.from_user.id,f'Вы хотите обменять {from_value} на {out_value}. Если данные не верны, в колличестве обмена введите 0.')
    bot.send_message(message.from_user.id,'Какое кол. валюты вы хотите обменять?')
    bot.register_next_step_handler(message,raschet)
def raschet(message):
    global how_value
    how_value = 0
    try:
        how_value = int(message.text)
        rezult = how_value*VALUTA[out_value]/VALUTA[from_value]
        bot.send_message(message.from_user.id,f'С {how_value} {from_value} вы получили {rezult} {out_value}')
    except Exception:
        bot.send_message(message.from_user.id,f'Введите пожалуйста целочисленный тип данных')
        bot.register_next_step_handler(message,raschet)
    
bot.polling(non_stop=True, interval=0)