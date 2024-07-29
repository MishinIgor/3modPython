import telebot, random, copy, json
with open('token_9gr.txt') as f:
    TOKEN = f.read()
bot = telebot.TeleBot(TOKEN)

users_info = {}
locations = {
    '1' : {'text' : 'Вы играете за героя, который попал в опасный лес, вам нужно найти выход в город и остаться живым', 'items' : [], 'next_move' : {'Пойти вперед' : '2'}, 'exchange' : {}},
    '2' : {'text' : 'Вы попали в лес и ощутили приятный аромат сосновых деревьев, который наполнил легкие. Похоже, что вы оказались в глубине дикой природы, где еще не ощущается шум городской суеты.', 'items' : [], 'next_move' : {'Пойти налево' : '3',
                                                                                                                                                                                                                                      'Пойти прямо' : '4',
                                                                                                                                                                                                                                      'Пойти направо' : '5'}, 'exchange' : {}},
    '3' : {'text' : 'На покрытой землей каменной плите сидят темные фигуры, их глаза горят в темноте, а в руках у них ножи. Они улыбаются вам и произносят "Добро пожаловать, Наш новый друг!". Вам настолько не хватает еды и воды для того, чтобы идти дальше, что вы становитесь их жертвой и все заканчивается очень плохо.', 'items' : [], 'next_move' : {'Вы погибли. Начать сначала': '1'}, 'exchange' : {}},
    '4' : {'text' : 'Вы вышли в поле. Перед вам торговец.', 'items' : [], 'next_move' : {'Вернуть назад' : '2'}, 'exchange' : {'шкатулка' : 'золото: 3'}},
    '5' : {'text' : 'Вы оказались около подземелья, которое смотрелось довольно страшно. ', 'items' : [], 'next_move' : {'Вернуться назад' : '2',
                                                                                'Войти внутрь' : '7',
                                                                                'Осмотреться вокруг' : '6'}, 'exchange' : {}},
    '6' : {'text' : 'Осматриваясь вокруг, вы замечаете, что на стене рядом с входом кто-то нанес странные символы, которые вы не можете разгадать. Далее ты немного еще побродил с надеждой что-то найти...', 'items' : ['шкатулка'], 'next_move' : {'Вернуться к подземелью' : '5'}, 'exchange' : {}},
    '7' : {'text' : 'Стены здесь полностью закрыты грубым камнем, а в воздухе царит прохлада и сырость. Похоже, что вы находитесь на начальном уровне подземелья.', 'items' : ['золото: 2'], 'next_move' : {'Пойти вперед' : '8',
                                                                                                                                                                                                            'Выйти на улицу' : '5'}, 'exchange' : {}},
    '8' : {'text' : 'Ты проходишь дальше, тут очень темно и сыро. Но вдруг в далеке ты замечаешь свет', 'items' : [], 'next_move' : {'Пойти дальше' : '9',
                                                                                                                                     'Вернуться' : '7'}, 'exchange' : {}},
    '9' : {'text' : 'Концовка не за горами, но прохождение не обойдется без дополнительных расходов. На выходе стоит разбойник с табличкой "выход 5 золотых"', 'items' : [], 'next_move' : {'Вернуться назад' : '8'}, 'exchange' : {'золото: 5' : 'выход'}}
}

comands = {'help': 'Ввыводит все допустимые команды',
           'game': 'начинает новую игру',
           'save': 'сохраняет текущий результат',
           'load': 'продолжает игру с предыдущего сохранения'}
@bot.message_handler(commands=list(comands.keys()))
def start_game(message):
    global users_info
    if message.text == '/game':
        #добавляем пользователя в словарь с значениями по умолчанию
        users_info[message.from_user.username] = {'cur_pos': '1','coins': 0, 'items': [], 'loc': copy.deepcopy(locations)}
        txt, keyboard = generate_story(message.from_user.username,users_info[message.from_user.username]['cur_pos'])
        bot.send_message(message.chat.id,txt,reply_markup=keyboard)
    elif message.text == '/help':
        info = ''
        for key,value in comands.items():
            info += f'/{key} - {value} \n'
        bot.send_message(message.chat.id,info)
    elif message.text == '/save':
        with open(f'{message.from_user.id}.json','w',encoding='utf-8') as f:
            json.dump(users_info,f,indent=2,ensure_ascii=False)
    elif message.text == '/load':
        try:
            with open(f'{message.from_user.id}_gr9.json','r',encoding='utf-8') as f:
                users_info = json.load(f)
            txt, keyboard = generate_story(message.from_user.username,users_info[message.from_user.username]['cur_pos'])
            bot.send_message(message.chat.id,txt,reply_markup=keyboard)
        except Exception as exc:
            bot.send_message(message.chat.id,f'Сохранений не найдено(или возникла ошибка {exc}), введите /game, чтобы начать новую игру.')
def generate_story(user,position):
    #берем текстовое описание локации
    txt = locations[position]['text']
    # создаём клавиатуру
    keyboard = telebot.types.InlineKeyboardMarkup()
    #создаём кнопки
    for i in users_info[user]['loc'][position]['next_move']:
        # берем текст направления
        key_txt = i
        # берём название локации
        key_data = locations[position]['next_move'][i]
        keyboard.add(telebot.types.InlineKeyboardButton(text=key_txt,callback_data=key_data))
    return (txt,keyboard)
@bot.callback_query_handler(func=lambda call: call.data in locations)
def callback_query(call):
    #меняем текущую позицию пользователя
    users_info[call.from_user.username]['cur_pos'] = call.data
    #генерируем новый текст и кнопки
    txt, keyboard = generate_story(call.from_user.username,users_info[call.from_user.username]['cur_pos'])
    bot.send_message(call.message.chat.id,txt,reply_markup=keyboard)
if __name__ == '__main__':
    bot.infinity_polling()
