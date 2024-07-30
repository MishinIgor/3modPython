import telebot, json, copy
with open('token_15gr.txt') as f:
    TOKEN = f.read()
bot = telebot.TeleBot(TOKEN)
# {‘локация’ : {
# ‘text’ : ‘текстовое описание’, 
# ‘items’ : [‘предметы, которые можно собрать’] , 
# ‘next_move’ : {‘направление’ : ‘локация’}, 
# ‘exchange’ : {‘что меняем’ : ‘на что меняем’}
# }
# }

users_info = {}
location = {'1': {'text': 'Вы играете за героя, который попал в опасный лес, вам нужно найти выход в город и остаться живым', 'items': [], 'next_move': {'Пойти вперед': "2"}, 'exchange':{}},
            '2': {'text': 'Вы попали в лес и ощутили приятный аромат сосновых деревьев, который наполнил легкие. Похоже, что вы оказались в глубине дикой природы, где еще не ощущается шум городской суеты.', 'items': ['фляга'], 'next_move': {"Пройти налево": "3", "Пройти прямо": "4", "Пройти направо": "5"}, 'exchange':{}},
            '3': {'text': 'На покрытой земле каменной плите сидят темные фигуры, их глаза горят в темноте, а в руках у них ножи. Они улыбаются вам и произносят "Добро пожаловать, Наш новый друг!". Вам настолько не хватает еды и воды для того, чтобы идти дальше, что вы становитесь их жертвой и всё заканчивается очень плохо', 'items': [], 'next_move': {'Начать сначала': "new_game"}, 'exchange':{}},
            '4': {'text': 'Вы вышли в поле. Перед вами торговец.', 'items': [], 'next_move': {"Вернуться назад": "2"}, 'exchange':{"шкатулка": "золото: 3"}},
            '5': {'text': 'Вы оказались около подземелья, которое смотрелось довольно страшно.', 'items': ["кирка"], 'next_move': {"Войти внутрь": "7", "Осмотреться": "6", "Вернуться назад": "2"}, 'exchange':{}},
            '6': {'text': 'Осматриваясь вокруг, вы замечаете что на стене рядом с входом кто-то нанес странные символы, которые вы не можете разгадать. Далее Вы немного ещё побродили с надеждой что-то найти...', 'items': ["шкатулка"], 'next_move': {"Вернуться к подземелью": "5"}, 'exchange':{}},
            '7': {'text': 'Стены здесь полностью закрыты грубым камнем, а в воздухе царит прохлада и сырость. Похоже, что вы находитесь на начальном уровне подземелья.', 'items': ["золото: 2"], 'next_move': {"Пойти вперед": "8", "Выйти на улицу": "5"}, 'exchange':{}},
            '8': {'text': 'Вы проходите дюальше, тут очень темно и сыро. Но вдруг в далеке Вы замечаете свет.', 'items': [], 'next_move': {"Пойти дальше": "9", "Вернуться": "7"}, 'exchange':{}},
            '9': {'text': 'Концовка не за горами, но прохождение не обойдётся без дополнительных расходов. На входе стоит разбойник с табличкой "выход за 5 золотых"', 'items': [], 'next_move': {}, 'exchange': {"золото: 5": "выход"}}} # '': {'text': '', 'items': [], 'next_move': {}, 'exchange':{}}
comands = {'help': 'Выводит все команды которые может выполнить.',
           'game': "Начинает НОВУЮ игру",
           'save': 'Сохраняет игру',
           'load': 'продолжает игру загрузив последнее сохранение',
           'items': 'Показывает собранные предметы'}
def generate_story(user,position):
        global users_info
        # берем текстовое описание локации
        txt = location[position]['text']
        #создаём клавиатуру
        keyboard = telebot.types.InlineKeyboardMarkup()
        #Создаём кнопки с ответами по следующим ходам
        for i in users_info[user]['loc'][position]['next_move']:
            # берем текст направления
            key_txt = i
            key_data = location[position]['next_move'][i]
            keyboard.add(telebot.types.InlineKeyboardButton(text=key_txt,callback_data=key_data))
        # создаем кнопки для предметов, которые можно взять
        for i in users_info[user]['loc'][position]['items']:
            #берем название предмета
            key_txt = f'Взять предмет - {i}'
            #в callback_data добавим в начало "item", чтобы в будущем было проще разделить обработку на несколько функций
            key_data = 'item ' + i
            keyboard.add(telebot.types.InlineKeyboardButton(text=f'{key_txt}🔍',callback_data=key_data))
        for i in users_info[user]['loc'][position]['exchange']:
            # проверяем, что у нас есть нужный предмет для обмена или неообходимое кол-во монет.
            if i in users_info[user]['items'] or (i.startswith('золото: ') and users_info[user]['золото'] >= int(i.replace('золото: ', ''))):
                # генерируем текст обмена
                key_txt = f'Обменять предмет {i} на {users_info[user]['loc'][position]['exchange'][i]} 🤝'
                # в callback_data добавим в начало 'exchange ', чтобы в будущем было проще разделить обработку на несколько функций
                key_data = 'exchange '+i
                keyboard.add(telebot.types.InlineKeyboardButton(text=key_txt,callback_data=key_data))
        return (txt, keyboard)
@bot.message_handler(commands=list(comands.keys()))
def start_game(message):
    global users_info
    if message.text == '/game':
        #Добавляем пользователя в словарь с значениями по умолчанию.
        users_info[message.from_user.username] = {'cur_pos': '1', 'золото': 0, 'items': [], 'loc': copy.deepcopy(location)}
        txt, keyboard = generate_story(message.from_user.username,users_info[message.from_user.username]['cur_pos'])
        bot.send_message(message.chat.id,txt,reply_markup=keyboard)
    elif message.text == '/help':
        info = ''
        for i,j in comands.items():
            info += f'/{i} - {j}'+'\n'
        bot.send_message(message.chat.id,info)
    elif message.text == '/save':
        with open(f'{message.from_user.id}_gr15.json','w',encoding='utf-8') as f:
            json.dump(users_info[message.from_user.username],f,indent=2,ensure_ascii=False)
    elif message.text == '/load':
        try:
            with open(f'{message.from_user.id}_gr15.json','r',encoding='utf-8') as f:
                users_info[message.from_user.username] = json.load(f)
            txt, keyboard = generate_story(message.from_user.username,users_info[message.from_user.username]['cur_pos'])
            bot.send_message(message.chat.id,txt,reply_markup=keyboard)
        except Exception as exc:
            bot.send_message(message.chat.id,f'Ваших сохранений не найдено(или ошибка {exc})')
    elif message.text == '/items':
        my_items = (',').join(users_info[message.from_user.username]['items'])
        bot.send_message(message.chat.id,f'Ваш предметы: {my_items}')
        bot.send_message(message.chat.id,f'Ваше золото: {users_info[message.from_user.username]['золото']}')
@bot.callback_query_handler(func = lambda call: call.data in location)
def callback_query(call):
    # меняем текущую позицию пользователя
    users_info[call.from_user.username]['cur_pos'] = call.data
    #генерируем новый текст и кнопки
    txt, keyboard = generate_story(call.from_user.username,users_info[call.from_user.username]['cur_pos'])
    bot.send_message(call.message.chat.id, txt, reply_markup=keyboard)
    
@bot.callback_query_handler(func = lambda call: call.data.startswith('item '))
def callback_query(call):
    # берем название предмета (в строке заменяем подстроку 'item' на '')
    item = call.data.replace('item ', '')
    # если предмет начинается на "золото: "
    if item.startswith('золото: '):
        # то добавляем пользователю на балнс это кол-во монет
        users_info[call.from_user.username]['золото'] += int(item.replace('золото: ', ''))
    else:
        # иначе просто добавляем в список предметов
        users_info[call.from_user.username]['items'].append(item)
    # удаляем с карты локации этот предмет (чтобы повторно не взять)
    users_info[call.from_user.username]['loc'][users_info[call.from_user.username]['cur_pos']]['items'].remove(item)
    # сообщение о удачном действии
    bot.send_message(call.message.chat.id, f'➕Получен {item}➕')
    txt, keyboard = generate_story(call.from_user.username,users_info[call.from_user.username]['cur_pos'])
    bot.send_message(call.message.chat.id,txt,reply_markup=keyboard)
@bot.callback_query_handler(func = lambda call: call.data.startswith('exchange '))
def callback_query(call):
    # берем название предмета (в строке заменяем подстроку 'exchange ' на '')
    item1 = call.data.replace('exchange ', '')
    # берем название предмета (из словаря), который получим
    item2 = users_info[call.from_user.username]['loc'][users_info[call.from_user.username]['cur_pos']]['exchange'][item1]
    # Если item1 начинается с 'золото: '
    if item1.startswith('золото: '):
        #уменьшаем кол-во монет. На достаточность проверять не нужно, мы это сделали при создании кнопок обмена
        users_info[call.from_user.username]['золото'] -= int(item1.replace('золото: ', ''))
    else:
        # иначе удаляем предмет
        users_info[call.from_user.username]['items'].remove(item1)
    #если мы меняем на золото
    if item2.startswith('золото: '):
        #увеличиваем баланс
        users_info[call.from_user.username]['золото'] += int(item2.replace('золото: ', ''))
    else:
        # иначе добавляем нам предмет
        users_info[call.from_user.username]['items'].append(item2)
        #удаляем с локации этот обмен
    users_info[call.from_user.username]['loc'][users_info[call.from_user.username]['cur_pos']]['exchange'].pop(item1)
    if item2 == 'выход':
        bot.send_message(call.message.chat.id,'Тебе удалось пройти квест')
    else:
        # сообщение об удачном действии
        bot.send_message(call.message.chat.id,f'Обмен завершён. Получено {item2}')
        txt, keyboard = generate_story(call.from_user.username,users_info[call.from_user.username]['cur_pos'])
        bot.send_message(call.message.chat.id,txt,reply_markup=keyboard)
@bot.callback_query_handler(func = lambda call: call.data.startswith('new_game'))
def new_game(call):
    bot.answer_callback_query(call.id,'Все ваши предметы удалены')
    users_info[call.from_user.username] = {'cur_pos': '1', 'золото': 0, 'items': [], 'loc': copy.deepcopy(location)}
    txt, keyboard = generate_story(call.from_user.username,users_info[call.from_user.username]['cur_pos'])
    bot.send_message(call.message.chat.id,txt,reply_markup=keyboard)
if __name__ == '__main__':
    bot.infinity_polling()
