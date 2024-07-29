# Доделать: Забирать из локации итемы и помещать в инвентарь, появление кнопки при возможности обмена, сохранение
import telebot,random,json
from copy import deepcopy
with open('token_8gr.txt') as f:
    TOKEN = f.read()
bot = telebot.TeleBot(TOKEN)
users_info = {}
locations = { '1': {'text': 'Вы играете за героя, который попал в опасный лес. Вам нужно найти выход в город и остаться живым.', 
                    'items': [], 'next_move': {'Пойти вперёд': '2'}, 'exchange': {} },
             '2': {'text': 'Вы попали в лес и ощутили приятный аромат сосновых деревьев, который наполнил легкие. Похоже, что вы оказались в глубине дикой природы, где ещё не ощущается шум городской суеты.', 'items': [], 
                   'next_move': {"Пойти налево": "3",
                                 "Пойти прямо": "4",
                                 "Пойти направо": "5"}, 'exchange': {}},
            '3': {'text': 'На покрытой землёй каменной плите сидят темные фигуры, их глаза горяд в темноте, а в руках у них ножи. Они улыбаются вам и произносят "Добро пожаловать, Наш новый друг!". Вам настолько не хватает еды и воды для того, чтобы идти дальше, что вы становитесь их жертвой и все заканчивается очень плохо.', 'items': [], 'next_move': {}, 'exchange': {}},
            '4': {'text': 'Вы вышли в поле. Перед вами торговец.', 'items': [], 'next_move': {"Вернуться назад": "2"}, 'exchange': {"Шкатулка": {"золото": 3}} },
            "5": {'text': 'Вы оказались около подземелья, которое смотрелось довольно страшно.', 'items': [], 'next_move': {'Вернуться назад': '2', "Войти внутрь": "7", "Осмотреться вокруг": "6"}, 'exchange': {} },
            "6": {'text': "Осматриваясь вокруг, вы замеаете, что на стене рядом с входом кто-то нанес странные символы, которые вы не можете разгадать. Далее Вы немного ещё побродил с надеждой что-то найти...", 'items': [], 'next_move': {'Вернуться к подземелью': '5'}, 'exchange': {} },
            "7": {'text': 'Стены здесь полностью закрыты грубым камнем, а в воздухе царит прохлада и сырость. Похоже, что вы находитесь на начальном уровне подземелья', 'items': [{"золото": 2}], 'next_move': {"Пройти вперёд": "8", "Выйти на улицу": "5"}, 'exchange': {}},
            "8": {'text': 'Ты проходишь дальше, тут очень темно и сыро. Но вдруг в далеке ты замечаешь свет', 'items': [], 'next_move': {"Пойти дальше": "9", "Вернуться": "7"}, 'exchange': {} },
            "9": {'text': 'Концовка не за горами, но похождение не обойдется без дополнительных расходов.', 'items': [], 'next_move': {"Вернуться назад": "8"}, 'exchange': {"выход": {"золото": 5}} }
             }
@bot.message_handler(commands=['start'])
def start_game(message):
    # добавляем пользователя в словарь с значениями по умолчанию
    users_info[message.from_user.username] = {'cur_pos': '1', 'золото': 0, 'items': [], 'loc': deepcopy(locations)}
    txt, keyboard = generate_story(message.from_user.username,users_info[message.from_user.username]['cur_pos'])
    bot.send_message(message.chat.id, txt, reply_markup=keyboard)
def generate_story(user,position):
    #берем текстовое описание локации
    txt = locations[position]['text']
    # создаём клавиатуру
    keyboard = telebot.types.InlineKeyboardMarkup()
    #Создаём кнопки с ответами по следующим ходам
    for i in users_info[user]['loc'][position]['next_move']:
        key_txt = i
        key_data = locations[position]['next_move'][i]
        keyboard.add(telebot.types.InlineKeyboardButton(text = key_txt, callback_data=key_data))
    return (txt,keyboard)
@bot.callback_query_handler(func= lambda call: call.data in locations)
def callback_query(call):
    # меняем текущую позицию пользователя
    users_info[call.from_user.username]['cur_pos'] = call.data
    # генерируем новый текст и кнопки
    txt, keyboard = generate_story(call.from_user.username, users_info[call.from_user.username]['cur_pos'])
    # отправляем сообщение
    bot.send_message(call.message.chat.id,txt,reply_markup=keyboard)
@bot.message_handler(commands=['save','load'])
def save_load(message):
    global users_info
    if message.text == '/save':
        with open(f'{message.from_user.id}.json','w',encoding='utf-8') as f:
            json.dump(users_info,f,ensure_ascii=False)
    elif message.text == '/load':
        with open(f'{message.from_user.id}.json','w',encoding='utf-8') as f:
            users_info = json.load(f)
        bot.send_message(message.chat.id,'Введите /start для продолжения')

bot.polling(non_stop=True, interval=0)