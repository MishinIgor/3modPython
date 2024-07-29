import telebot,random,json,copy
with open('token_5gr.txt') as f:
    TOKEN = f.read()
bot = telebot.TeleBot(TOKEN)

users_info = {}
# '': {'text': '', 'items': [], 'next_move': {}, 'exchange': {}}
locations = {
    '1': {'text': 'Вы играете за героя, который попал в опасный лес, вам нужно найти выход в город и остаться живым', 'items': [], 'next_move': {'Пойти вперед': "2"}, 'exchange': {}},
    '2': {'text': 'Вы попали в лес и ощутили приятный аромат сосновых деревьев, который наполнил легкие. Похоже, что вы оказались в глубине дикой природы, где ещё не ощущается шум городской суеты.', 'items': [], 'next_move': {"Пройти налево": "3", "Пройти прямо": "4", "Пройти направо": "5"}, 'exchange': {}},
    '3': {'text': 'на покрытой земле каменной плите сидят темные фигуры, их глаза горят в темноте, а в руках у них ножи. Они улыбаются вам и произносят "Добро пожаловать, наш новый друг!". Вам настолько не хватает еды и воды для того, чтобы идти дальше, что вы становитесь их жертвой и все заканчивается очень плохо.', 'items': [], 'next_move': {"Вы погибли. Начать сначала?": "1"}, 'exchange': {}},
    '4': {'text': 'Вы вышли в поле. Перед вами торговец', 'items': [], 'next_move': {"Вернуться": "2"}, 'exchange': {'шкатулка': {'золото': 3}}},
    '5': {'text': 'Вы оказались около подземелья, которое смотрелось довольно страшно', 'items': [], 'next_move': {"Вернуться": "2", "Войти в подземелье": "7", "Осмотреться": "6"}, 'exchange': {}},
    '6': {'text': 'Осматриваясь вокруг, вы замечаете, что на стене рядом с входом кто-то нанес странные символы, которые вы не можете разгадать. Далее ты немного ещё побродил с надеждой что-то найти...', 'items': ["шкатулка"], 'next_move': {"Вернуться": "5"}, 'exchange': {}},
    '7': {'text': 'Стены здесь полностью закрыты грубым камнем, а в воздухе царит прохлада и сырость. Похоже, что вы находитесь на начальном уровне подземелья.', 'items': [{"золото": 2}], 'next_move': {"Вернуться": "5", "Пойти дальше": "8"}, 'exchange': {}},
    '8': {'text': 'Ты проходишь далльше, тут очень темно и сыро. Но вдруг в далеке ты замечаешь свет.', 'items': [], 'next_move': {"Вернуться": "7", "Пройти дальше": "9"}, 'exchange': {}},
    '9': {'text': 'Концовка не за горами, но прохождение не обойдется без дополнительных расходов. У выхода стоит разбойник с табличкой "выход за 5 золотых".', 'items': [], 'next_move': {}, 'exchange': {"золото: 5": "выход"}},
}

comands = {'help': 'Выводит все команды',
           'game': 'Начинает НОВУЮ игру',
           'save': 'Сохраняет игру',
           'load': 'Продолжает игру с последнего сохранения'}
@bot.message_handler(commands=list(comands.keys()))
def my_game(message):
    global users_info
    if message.text == '/help':
        info = ''
        for key,value in comands.items():
            info += f'/{key} - {value} \n'
        bot.send_message(message.chat.id,info)
    elif message.text == '/game':
        users_info[message.from_user.username] = {'cur_pos': '1', 'золото': 0, 'items': [], 'loc': copy.deepcopy(locations)}
        txt, keyboard = generate_story(message.from_user.username,users_info[message.from_user.username]['cur_pos'])
        bot.send_message(message.chat.id,txt,reply_markup=keyboard)
    elif message.text == '/save':
        with open(f'{message.from_user.id}.json','w',encoding='utf-8') as f:
            json.dump(users_info,f,indent=2,ensure_ascii=False)
    elif message.text == '/load':
        with open(f'{message.from_user.id}.json','r',encoding='utf-8') as f:
            users_info = json.load(f)
        txt, keyboard = generate_story(message.from_user.username,users_info[message.from_user.username]['cur_pos'])
        bot.send_message(message.chat.id,txt,reply_markup=keyboard)
        
def generate_story(user,position):
    #берем текстовое описание локации
    txt = locations[position]['text']
    #создаём клавиатуру
    keyboard = telebot.types.InlineKeyboardMarkup()
    #создаём кнопки с ответами по следующим ходам
    for i in users_info[user]['loc'][position]['next_move']:
        # берем текст направления
        key_txt = i
        # берем название локации
        key_data = locations[position]['next_move'][i]
        keyboard.add(telebot.types.InlineKeyboardButton(text=key_txt,callback_data=key_data))
    return (txt,keyboard)
@bot.callback_query_handler(func=lambda call: call.data in locations)
def callback_query(call):
    users_info[call.from_user.username]['cur_pos'] = call.data
    txt, keyboard = generate_story(call.from_user.username,users_info[call.from_user.username]['cur_pos'])
    bot.send_message(call.message.chat.id,txt,reply_markup=keyboard)
# @bot.message_handler(content_types=['text'])
# def loc(message):
#     if message.text in '123456789':
#         users_info[message.from_user.username]['cur_pos'] = message.text
#         txt, keyboard = generate_story(message.from_user.username,users_info[message.from_user.username]['cur_pos'])
#         bot.send_message(message.chat.id,txt,reply_markup=keyboard)

if __name__ == '__main__':
    bot.infinity_polling()