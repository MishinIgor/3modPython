import telebot,random #Импортиуем библиотеку для работы с ботами
with open('token_9gr.txt') as f:
    TOKEN = f.read() #Вводим токен в константу
bot = telebot.TeleBot(TOKEN) #Создаём переменную которая будет являться классом бота с токеном из константы
mychat_id = -4230070784
comands = ['photo','help','loc_photo','doc','отправка','venue']
photos = [
    'https://tardokanatomy.ru/sites/default/files/izo/programmirovanie-3-1.png',
    'https://etu.ru/assets/cache/images/ru/povyshenie-kvalifikacii/minors/1280x800-programmirovanie-na-python.4d8.jpg',
    'https://1.bp.blogspot.com/-VMixkQ96920/YFNrowGuuuI/AAAAAAAABp8/OIXGED4_dSkDQBQ27Q_ZbxppScYOkdDagCLcBGAsYHQ/s1440/87-879618_big-python-logo-wallpaper-python-digital-marketing.jpg',
    'https://balakovo24.ru/b24/uploads/2022/06/python.jpg'
]
@bot.message_handler(commands=comands)
def universal(message):
    if message.text == '/help':
        bot.send_message(message.chat.id,f'Я умею выполнять команды: {comands[:]}')
    elif message.text == '/photo':
        bot.send_message(message.chat.id,'Хотите получить в личном или публичном чате(введите лично/публично)?') # Только в лс боту писать
        bot.register_next_step_handler(message,yes_or_no)
    elif message.text == '/loc_photo':
        bot.send_photo(message.chat.id,open('image.png','rb'))
    elif message.text == '/doc':
        bot.send_document(message.chat.id,open('test.txt','rb'))
    elif message.text == '/отправка':
        if message.from_user.id == 1680980801:
            with open('test.txt','r',encoding='utf-8') as file:
                bot.send_message(mychat_id,file.read())
    elif message.text == '/venue':
        bot.send_message(message.chat.id,'Напишите через пробел вашу широту,долготу,описание места, описание локации')
        bot.register_next_step_handler(message,location)
def location(message):
    ven = (message.text).split()
    bot.send_venue(mychat_id,ven[0],ven[1],ven[2],ven[3])
def yes_or_no(message):
    if message.text == 'лично':
        bot.send_photo(message.from_user.id,random.choice(photos))
    elif message.text == 'публично':
        bot.send_photo(mychat_id,random.choice(photos))
    else:
        bot.send_message(message.chat.id,'Ничего не понятно :(')
            
@bot.message_handler(content_types=['text'])
def user_add(message):
    with open('test.txt','a',encoding='utf-8') as file:
        text = f'Пользователь @{message.from_user.username} с id {message.from_user.id} создал сообщение: {message.text} \n'
        file.write(text)
bot.polling(non_stop=True, interval=0)