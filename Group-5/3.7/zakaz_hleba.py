import telebot,random,json
from telebot import types
with open('token_5gr.txt') as f:
    TOKEN = f.read()
bot = telebot.TeleBot(TOKEN)
buy = {
        "Хлеб белый": 25,
        "Хлеб чёрный": 27,
        "Булочка с изюмом": 20
        }
clients = {}
key = ''
zakaz = []
try:
    with open('clients_gr5.json',encoding='utf-8') as f:
        clients = json.load(f)
except Exception:
        pass
comands = {'help': 'Выводит все команды',
           'create_buy': 'Создаёт заказ',
           'create_card': 'Создаёт вашу карточку постоянного клиента',
           'info': "Выводит информацию о пользователях создавших карты"
           }
@bot.message_handler(commands=list(comands.keys()))
def universal(message):
    if message.text == '/help':
        for i,j in comands.items():
            bot.send_message(message.chat.id,f'Команда /{i} - {j}')
    elif message.text == '/create_card':
        bot.send_message(message.chat.id,'Введите логин для карты')
        bot.register_next_step_handler(message,create_card)
    elif message.text == '/info':
        for i,j in clients.items():
            bot.send_message(message.chat.id,f'{i} - {j}')
    elif message.text == '/create_buy':
        bot.send_message(message.chat.id,'Введите логин для заказа')
        bot.register_next_step_handler(message,create_buy)
def create_buy(message):
    global key
    key = message.text
    if key in clients.keys():
        keyboard = telebot.types.InlineKeyboardMarkup()
        for i,j in buy.items():
            keyboard.add(telebot.types.InlineKeyboardButton(text=f'{i}-{j}',callback_data=i))
        bot.send_message(message.chat.id,'Выберите продукцию для заказа',reply_markup=keyboard)
    else:
        bot.send_message(message.chat.id,'Такого пользователя не существует')
def create_card(message):
    global clients
    key = message.text
    clients[key] = {'TG_id': message.from_user.id,'TG_name':'@'+message.from_user.username}
    with open('clients_gr5.json','w',encoding='utf-8') as f:
        json.dump(clients,f)
    bot.send_message(message.chat.id,f'Пользователь {message.text} добавлен')
@bot.callback_query_handler(func= lambda call: True)
def callback_query(call):
    global clients, key
    # clients[key]['Заказ']
    zakaz.append(call.data)
    pass
bot.polling(non_stop=True,interval=0)