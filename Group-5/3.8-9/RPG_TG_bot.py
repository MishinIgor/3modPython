import telebot,random,json,copy,time
with open('token_5gr.txt') as f:
    TOKEN = f.read()
bot = telebot.TeleBot(TOKEN)

users_info = {}
# '': {'text': '', 'items': [], 'next_move': {}, 'exchange': {}}

locations = {
    '1': {'text': 'Вы играете за героя, который попал в опасный лес, вам нужно найти выход в город и остаться живым', 'items': ['перстень'], 'next_move': {'Пойти вперед': "2"}, 'exchange': {}},
    '2': {'text': 'Вы попали в лес и ощутили приятный аромат сосновых деревьев, который наполнил легкие. Похоже, что вы оказались в глубине дикой природы, где ещё не ощущается шум городской суеты.', 'items': ['фляга'], 'next_move': {"Пройти налево": "3", "Пройти прямо": "4", "Пройти направо": "5"}, 'exchange': {}},
    '3': {'text': 'на покрытой земле каменной плите сидят темные фигуры, их глаза горят в темноте, а в руках у них ножи. Они улыбаются вам и произносят "Добро пожаловать, наш новый друг!". Вам настолько не хватает еды и воды для того, чтобы идти дальше, что вы становитесь их жертвой и все заканчивается очень плохо.', 'items': [], 'next_move': {"Вы погибли. Начать сначала?": "new_game"}, 'exchange': {}},
    '4': {'text': 'Вы вышли в поле. Перед вами торговец', 'items': ['сапог'], 'next_move': {"Вернуться": "2"}, 'exchange': {'шкатулка': "золото: 3"}},
    '5': {'text': 'Вы оказались около подземелья, которое смотрелось довольно страшно', 'items': ['кирка'], 'next_move': {"Вернуться": "2", "Войти в подземелье": "7", "Осмотреться": "6"}, 'exchange': {}},
    '6': {'text': 'Осматриваясь вокруг, вы замечаете, что на стене рядом с входом кто-то нанес странные символы, которые вы не можете разгадать. Далее ты немного ещё побродил с надеждой что-то найти...', 'items': ["шкатулка"], 'next_move': {"Вернуться": "5"}, 'exchange': {}},
    '7': {'text': 'Стены здесь полностью закрыты грубым камнем, а в воздухе царит прохлада и сырость. Похоже, что вы находитесь на начальном уровне подземелья.', 'items': ["золото: 2"], 'next_move': {"Вернуться": "5", "Пойти дальше": "8"}, 'exchange': {}},
    '8': {'text': 'Ты проходишь далльше, тут очень темно и сыро. Но вдруг в далеке ты замечаешь свет.', 'items': ['тетрадь по алгебре'], 'next_move': {"Вернуться": "7", "Пройти дальше": "9"}, 'exchange': {}},
    '9': {'text': 'Концовка не за горами, но прохождение не обойдется без дополнительных расходов. У выхода стоит разбойник с табличкой "выход за 5 золотых".', 'items': [], 'next_move': {}, 'exchange': {"золото: 5": "выход"}},
}

comands = {'help': 'Выводит все команды',
           'game': 'Начинает НОВУЮ игру',
           'save': 'Сохраняет игру',
           'load': 'Продолжает игру с последнего сохранения',
           'items': 'Показывает собранные предметы и золото'}
key_death = telebot.types.InlineKeyboardMarkup()
key_death.add(telebot.types.InlineKeyboardButton(text='Начать сначала', callback_data='new_game'))
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
    # создаём кнопки для предметов, которые можно взять
    for i in users_info[user]['loc'][position]['items']:
        # берем название предмета
        key_txt = f'Взять предмет {i} 🔍'
        key_data = 'item '  + i
        keyboard.add(telebot.types.InlineKeyboardButton(text=key_txt,callback_data=key_data))
    # создаём кнопки для обмена предметами
    for i in users_info[user]['loc'][position]['exchange']:
        # проверяем, что у нас есть нужный предмет для обмена или необходимо кол-во монет
        if i in users_info[user]['items'] or (i.startswith('золото: ') and users_info[user]['золото'] >= int(i.replace('золото: ', ''))):
            # генерируем текст обмена
            key_txt = f'👉Обменять предмет {i} на {users_info[user]['loc'][position]['exchange'][i]} 🤝'
            key_data = 'exchange ' + i
            keyboard.add(telebot.types.InlineKeyboardButton(text=key_txt,callback_data=key_data))
    return (txt,keyboard)
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
        with open(f'{message.from_user.id}_gr5.json','w',encoding='utf-8') as f:
            json.dump(users_info[message.from_user.username],f,indent=2,ensure_ascii=False)
    elif message.text == '/load':
        try:
            with open(f'{message.from_user.id}_gr5.json','r',encoding='utf-8') as f:
                users_info[message.from_user.username] = json.load(f)
            txt, keyboard = generate_story(message.from_user.username,users_info[message.from_user.username]['cur_pos'])
            bot.send_message(message.chat.id,txt,reply_markup=keyboard)
        except Exception as exc:
            bot.send_message(message.chat.id,f'(ошибка {exc}). Попробуй начать новую игру введя команду /game.')
    elif message.text == '/items':
        all_items = (',').join(users_info[message.from_user.username]['items'])
        txt, keyboard = generate_story(message.from_user.username,users_info[message.from_user.username]['cur_pos'])
        bot.send_message(message.chat.id,f'Ваше золото: {users_info[message.from_user.username]['золото']}')
        bot.send_message(message.chat.id,f'Ваши предметы: {all_items}',reply_markup=keyboard)
@bot.callback_query_handler(func=lambda call: call.data in locations)
def callback_query(call):
    users_info[call.from_user.username]['cur_pos'] = call.data
    txt, keyboard = generate_story(call.from_user.username,users_info[call.from_user.username]['cur_pos'])
    bot.send_message(call.message.chat.id,txt,reply_markup=keyboard)
@bot.callback_query_handler(func=lambda call: call.data == 'new_game')
def callback_query(call):
    users_info[call.from_user.username] = {'cur_pos': '1', 'золото': 0, 'items': [], 'loc': copy.deepcopy(locations)}
    txt, keyboard = generate_story(call.from_user.username,users_info[call.from_user.username]['cur_pos'])
    bot.send_message(call.message.chat.id,txt,reply_markup=keyboard)
@bot.callback_query_handler(func = lambda call: call.data.startswith('item '))
def callback_query(call):
    # берем название предмета (в строке заменяем подстроку 'item', на '')
    item = call.data.replace('item ','')
    if item.startswith('золото: '):
        # то добавляем пользователю на баланс это кол-во монет
        emoji = '💵'
        users_info[call.from_user.username]['золото'] += int(item.replace('золото: ', ''))
    else:
        emoji = '📦'
        # иначе просто добавляем в список предметов
        users_info[call.from_user.username]['items'].append(item)
    # удаляем с карты локации этот предмет
    users_info[call.from_user.username]['loc'][users_info[call.from_user.username]['cur_pos']]['items'].remove(item)
    if item == 'тетрадь по алгебре':
        bot.answer_callback_query(call.id,'Вы погибли')
        bot.send_message(call.message.chat.id,'Позарились списать ДЗ? Не тут то было...В тетради пригрелась змея, которая напугалась и ужалила вас. Теперь вы мертвы',reply_markup=key_death)
    # сообщение о удачном действии
    elif item == 'фляга':
        bot.answer_callback_query(call.id,'Вы погибли')
        bot.send_message(call.message.chat.id,'Во фляге оставалось ещё виски. Вродебы, мало, но на пустой желудок ужасная смесь. Вы пьяный упали в лужу, и погибли захлебнувшись. А ведь минздрав предупреждал...',reply_markup=key_death)
    else:
        if item == 'кирка':
            bot.answer_callback_query(call.id,f'Я каменщик работаю 3 дня без зарплаты')
        elif item == 'сапог':
            bot.answer_callback_query(call.id,f'Ну и вонь из этих тапок...')
        txt, keyboard = generate_story(call.from_user.username,users_info[call.from_user.username]['cur_pos'])
        bot.send_message(call.message.chat.id,f'Готово! {emoji}')
        bot.send_message(call.message.chat.id,txt,reply_markup=keyboard)
@bot.callback_query_handler(func = lambda call: call.data.startswith('exchange '))
def callback_query(call):
    item1 = call.data.replace('exchange ', '')# что хотят за обмен
    item2 = users_info[call.from_user.username]['loc'][users_info[call.from_user.username]['cur_pos']]['exchange'][item1] #что дадут при обмене
    # Если item1 начинается с золото:
    if item1.startswith('золото: '):
        #Уменьшем кол-во монет. Проверку достаточности не проводим, она вшита при генерировании кнопки
        users_info[call.from_user.username]['золото'] -= int(item1.replace('золото: ', ''))
    else:
        users_info[call.from_user.username]['items'].remove(item1)
    # Если мы меняем на золто
    if item2.startswith('золото: '):
        #увеличиваем баланс
        users_info[call.from_user.username]['золото'] += int(item2.replace('золото: ', ''))
    else:
        # иначе добавляем нам предмет
        users_info[call.from_user.username]['items'].append(item2)
    users_info[call.from_user.username]['loc'][users_info[call.from_user.username]['cur_pos']]['exchange'].pop(item1)
    # если мы обменялись на выход, то выходим и сообщаем о победе
    if item2 == 'выход':
        bot.answer_callback_query(call.id,'ПОБЕДА!!!')
        bot.send_message(call.message.chat.id,f'🍞🍕🥪🥙🌮🍔 @{call.from_user.username}! Тебе удалось пройти квест!🍞🍕🥪🥙🌮🍔')
    else:
        # сообщение об удачном действии
        bot.answer_callback_query(call.id,'Обмен завершён')
        bot.send_message(call.message.chat.id,f'Получено {item2}')
        txt, keyboard = generate_story(call.from_user.username,users_info[call.from_user.username]['cur_pos'])
        bot.send_message(call.message.chat.id,txt,reply_markup=keyboard)
if __name__ == '__main__':
    bot.infinity_polling()