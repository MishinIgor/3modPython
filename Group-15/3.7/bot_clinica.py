# При вводе команды /start необходимо создать inline клавиатуру с 5 кнопками 
# (визуально одинаковыми, но в callback_data должны быть разные значения от 0 до 4, в зависимости от кнопки). 
# При нажатии на любую из кнопок будет вызываться обработчик, в котором с помощью модуля random будем определять 
# победное значение (от 0 до 4). Далее с помощью условия сравнивается ответ пользователя и победное значение и 
# выводится результат. 

import telebot,random,json
from telebot import types
with open('token_15gr.txt') as f:
    TOKEN = f.read()
key = ''
bot = telebot.TeleBot(TOKEN)
comands = ['help','create_card','info']
text_comands = (',').join(comands)
try:
    with open('cards_clients.json', encoding='utf-8') as f:
        data_clients = json.load(f)
except Exception:
    with open('cards_clients.json','+x', encoding='utf-8') as f:
        data_clients = json.load(f)
@bot.message_handler(commands=comands)
def universal(message):
    if message.text == '/help':
        bot.send_message(message.chat.id,f'Я умею выполнять команды {text_comands}')
    elif message.text == '/create_card':
        bot.send_message(message.chat.id,f'Введите Ваш логин для карточки')
        bot.register_next_step_handler(message,client)
    elif message.text == '/info':
        bot.send_message(message.chat.id,f'Зарегистрированны в карточке: {data_clients}')
def client(message):
    global key
    key = message.text
    data_clients[key] = {'TG_id': message.from_user.id, 'TG_username': message.from_user.username}
    with open('cards_clients.json','+a',encoding='utf-8') as card:
        json.dump(data_clients, card)
bot.polling(non_stop=True,interval=0)