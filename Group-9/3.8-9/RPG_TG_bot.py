import telebot, random, copy, json
with open('token_9gr.txt') as f:
    TOKEN = f.read()
bot = telebot.TeleBot(TOKEN)

users_info = {}
locations = {
    '1' : {'text' : 'Вы играете за героя, который попал в опасный лес, вам нужно найти выход в город и остаться живым', 'items' : [], 'next_move' : {'Пойти вперед' : '2'}, 'exchange' : {}},
    '2' : {'text' : 'Вы попали в лес и ощутили приятный аромат сосновых деревьев, который наполнил легкие. Похоже, что вы оказались в глубине дикой природы, где еще не ощущается шум городской суеты.', 'items' : ['фляга'], 'next_move' : {'Пойти налево' : '3',
                                                                                                                                                                                                                                      'Пойти прямо' : '4',
                                                                                                                                                                                                                                      'Пойти направо' : '5'}, 'exchange' : {}},
    '3' : {'text' : 'На покрытой землей каменной плите сидят темные фигуры, их глаза горят в темноте, а в руках у них ножи. Они улыбаются вам и произносят "Добро пожаловать, Наш новый друг!". Вам настолько не хватает еды и воды для того, чтобы идти дальше, что вы становитесь их жертвой и все заканчивается очень плохо.', 'items' : [], 'next_move' : {'Вы погибли. Начать сначала': 'new_game'}, 'exchange' : {}},
    '4' : {'text' : 'Вы вышли в поле. Перед вам торговец.', 'items' : [], 'next_move' : {'Вернуть назад' : '2'}, 'exchange' : {'шкатулка' : 'золото: 3'}},
    '5' : {'text' : 'Вы оказались около подземелья, которое смотрелось довольно страшно. ', 'items' : ['тапки'], 'next_move' : {'Вернуться назад' : '2',
                                                                                'Войти внутрь' : '7',
                                                                                'Осмотреться вокруг' : '6'}, 'exchange' : {}},
    '6' : {'text' : 'Осматриваясь вокруг, вы замечаете, что на стене рядом с входом кто-то нанес странные символы, которые вы не можете разгадать. Далее ты немного еще побродил с надеждой что-то найти...', 'items' : ['шкатулка'], 'next_move' : {'Вернуться к подземелью' : '5'}, 'exchange' : {}},
    '7' : {'text' : 'Стены здесь полностью закрыты грубым камнем, а в воздухе царит прохлада и сырость. Похоже, что вы находитесь на начальном уровне подземелья.', 'items' : ['золото: 2',"бутерброд"], 'next_move' : {'Пойти вперед' : '8',
                                                                                                                                                                                                            'Выйти на улицу' : '5'}, 'exchange' : {}},
    '8' : {'text' : 'Ты проходишь дальше, тут очень темно и сыро. Но вдруг в далеке ты замечаешь свет', 'items' : ['тетрадь по алгебре','перстень'], 'next_move' : {'Пойти дальше' : '9',
                                                                                                                                     'Вернуться' : '7'}, 'exchange' : {}},
    '9' : {'text' : 'Концовка не за горами, но прохождение не обойдется без дополнительных расходов. На выходе стоит разбойник с табличкой "выход 5 золотых"', 'items' : [], 'next_move' : {'Вернуться назад' : '8'}, 'exchange' : {'золото: 5' : 'выход'}},
    "10": {'text': 'В глубине леса есть таинственная тропа, которая ведёт к дому. Она петляет между деревьями и кустами, огибая овраги и холмы. По пути можно встретить лесных обитателей, которые не боятся человека. Кажется, что эта тропа бесконечна, но она всегда приводит к опушке леса, откуда уже рукой подать до дома.','items' : [], 'next_move' : {'Вернуться домой' : 'Победа'}, 'exchange' : {}}
}

comands = {'help': 'Ввыводит все допустимые команды',
           'game': 'начинает новую игру',
           'save': 'сохраняет текущий результат',
           'load': 'продолжает игру с предыдущего сохранения',
           'items': 'Выводит все предметы и золото'}
keyboard_death = telebot.types.InlineKeyboardMarkup()
keyboard_death.add(telebot.types.InlineKeyboardButton(text='Начать заного',callback_data='new_game'))
def generate_story(user,position):
    #берем текстовое описание локации
    txt = users_info[user]['loc'][position]['text']
    # создаём клавиатуру
    keyboard = telebot.types.InlineKeyboardMarkup()
    #создаём кнопки
    for i in users_info[user]['loc'][position]['next_move']:
        # берем текст направления
        key_txt = i
        # берём название локации
        key_data = users_info[user]['loc'][position]['next_move'][i]
        keyboard.add(telebot.types.InlineKeyboardButton(text=key_txt,callback_data=key_data))
    # создаём кнопки для items
    for i in users_info[user]['loc'][position]['items']:
        #берем название предмета
        if i.startswith('золото: '):
            key_txt = f'💰 {i} 🔍'
        else:
            key_txt = f'🎁 {i} 🔍'
        key_data = 'item ' + i
        keyboard.add(telebot.types.InlineKeyboardButton(text=key_txt,callback_data=key_data))
    # создаём кнопки для обмена
    for i in users_info[user]['loc'][position]['exchange']:
        #Проверяем, что у нас есть нужный предмет для обмена или необходимое кол-во монет.
        if i in users_info[user]['items'] or (i.startswith('золото: ') and users_info[user]['coins'] >= int(i.replace('золото: '))):
            # генерируем текст обмена
            key_txt = f'👉Обменять предмет {i} на {users_info[user]['loc'][position]['exchange'][i]}👈'
            key_data = 'exchange ' + i
            keyboard.add(telebot.types.InlineKeyboardButton(text=key_txt,callback_data=key_data))
    return (txt,keyboard)

@bot.message_handler(commands=list(comands.keys()))
def start_game(message):
    global users_info
    if message.text == '/game':
        #добавляем пользователя в словарь с значениями по умолчанию
        users_info[message.from_user.username] = {'cur_pos': '1','coins': 0, 'items': [], 'loc': copy.deepcopy(locations)}
        txt, keyboard = generate_story(message.from_user.username,users_info[message.from_user.username]['cur_pos'])
        bot.send_message(message.chat.id,txt,reply_markup=keyboard)
    elif message.text == '/items':
        all_item = (',').join(users_info[message.from_user.username]['items'])
        txt, keyboard = generate_story(message.from_user.username,users_info[message.from_user.username]['cur_pos'])
        bot.send_message(message.chat.id,f'Ваши предметы: {all_item}')
        bot.send_message(message.chat.id,f'Ваше золото: {users_info[message.from_user.username]['coins']}',reply_markup=keyboard)
    elif message.text == '/help':
        info = ''
        for key,value in comands.items():
            info += f'/{key} - {value} \n'
        bot.send_message(message.chat.id,info)
    elif message.text == '/save':
        with open(f'{message.from_user.id}_gr9.json','w',encoding='utf-8') as f:
            json.dump(users_info[message.from_user.username],f,indent=2,ensure_ascii=False)
    elif message.text == '/load':
        try:
            with open(f'{message.from_user.id}_gr9.json','r',encoding='utf-8') as f:
                users_info[message.from_user.username] = json.load(f)
            txt, keyboard = generate_story(message.from_user.username,users_info[message.from_user.username]['cur_pos'])
            bot.send_message(message.chat.id,txt,reply_markup=keyboard)
        except Exception as exc:
            bot.send_message(message.chat.id,f'Сохранений не найдено(или возникла ошибка {exc}), введите /game, чтобы начать новую игру.')
@bot.callback_query_handler(func=lambda call: call.data in locations)
def callback_query(call):
    #меняем текущую позицию пользователя
    users_info[call.from_user.username]['cur_pos'] = call.data
    #генерируем новый текст и кнопки
    txt, keyboard = generate_story(call.from_user.username,users_info[call.from_user.username]['cur_pos'])
    bot.send_message(call.message.chat.id,txt,reply_markup=keyboard)
@bot.callback_query_handler(func=lambda call: call.data == 'new_game')
def new_game(call):
    users_info[call.from_user.username] = {'cur_pos': '1','coins': 0, 'items': [], 'loc': copy.deepcopy(locations)}
    txt, keyboard = generate_story(call.from_user.username,users_info[call.from_user.username]['cur_pos'])
    bot.send_message(call.message.chat.id,txt,reply_markup=keyboard)
@bot.callback_query_handler(func=lambda call: call.data.startswith('item '))
def callback_query(call):
    #берем название предмета (в строке заменяем подстроку 'item', на '')
    item = call.data.replace('item ','')
    # если предмет начинается на "золото: "
    if item.startswith('золото: '):
        #то добавляем пользователю на балнс это кол-во монет
        users_info[call.from_user.username]['coins'] += int(item.replace('золото: ',''))
    else:
        users_info[call.from_user.username]['items'].append(item)
        #удаляем с карты локации этот предмет
    if item == 'тетрадь по алгебре':
        bot.answer_callback_query(call.id,'Вы погибли')
        bot.send_message(call.message.chat.id,'Хотели списать дз? Не тут то было! В тетради спала змея, и напугавшись укусила вас в глаз. Вы не смогли из за этого высосать яд и погибли.',reply_markup=keyboard_death)
    elif item == 'фляга':
        bot.answer_callback_query(call.id,'Вы погибли')
        bot.send_message(call.message.chat.id,'Обнаружив немного виски и выпих для храбрости на голодный желудок, вы ощутили лёгкость падения и мягкость ближайшей лужи. Захлебнувшись, вы так и не вспомнили, что минздрав предупреждал ведь...',reply_markup=keyboard_death)
    else:
        if item == 'бутерброд':
            bot.answer_callback_query(call.id,'Никогда ещё плесень не была такой вкусной')
        elif item == 'перстень' or 'перстень' in users_info[call.from_user.username]['items']:
            bot.answer_callback_query(call.id,'Теперь ты король воров. И никто тебя в лесу не тронет')
            users_info[call.from_user.username]['loc']['3']['next_move'].pop('Вы погибли. Начать сначала')
            users_info[call.from_user.username]['loc']['3']['next_move']['Тропа домой'] = '10' 
            users_info[call.from_user.username]['loc']['3']['text'] = 'Разбойники напали на Вас, но, увидев ваш перстень, осознали свою ошибку. Они извинились перед Вами и признались, что приняли Вас за другого человека. Вы поняли, что разбойники приняли вас за свеого.'
        users_info[call.from_user.username]['loc'][users_info[call.from_user.username]['cur_pos']]['items'].remove(item)
        # сообщение о удачном действии
        txt, keyboard = generate_story(call.from_user.username,users_info[call.from_user.username]['cur_pos'])
        bot.send_message(call.message.chat.id,txt,reply_markup=keyboard)
        bot.send_message(call.message.chat.id,f'Получен {item}',reply_markup=keyboard)
@bot.callback_query_handler(func=lambda call: call.data.startswith('Победа'))
def callback_query(call):
    bot.answer_callback_query(call.id,'ПОБЕДА!!!')
    bot.send_message(call.message.chat.id,'И вот она, долгожданная дорога домой! Вы никогда не забудете такое путешествие. Жаль, что это лишь сон и вы в своей кровати...')
@bot.callback_query_handler(func=lambda call: call.data.startswith('exchange '))
def callback_query(call):
    item1 = call.data.replace('exchange ', '') #предмет для обмена
    item2 = users_info[call.from_user.username]['loc'][users_info[call.from_user.username]['cur_pos']]['exchange'][item1] #предмет для получения
    # если item1 золото:
    if item1.startswith('золото: '):
        #Уменьшаем кол. нашего золота
        users_info[call.from_user.username]['coins'] -= int(item1.replace('золото: ',''))
    else:
        users_info[call.from_user.username]['items'].remove(item1)
    # если мы меняем на золото
    if item2.startswith('золото: '):
        users_info[call.from_user.username]['coins'] += int(item2.replace('золото: ',''))
    else:
        # иначе добавляем предмет
        users_info[call.from_user.username]['items'].append(item2)
    users_info[call.from_user.username]['loc'][users_info[call.from_user.username]['cur_pos']]['exchange'].pop(item1)
    # Если мы обменяли на выход, то выводим сообщение о переходе
    if item2 == 'выход':
        bot.send_message(call.message.chat.id,'Когда вы вошли, разбойник захлопнул двери. Вы увидели в просторном холле, где стены украшены изображениями древних битв и охотничьих сцен, стоит большой каменный стол с резными ножками в виде драконов. По огромным фигурам и объектам вы понимаете, что вы попали в дом великанов, и теперь вам нужно найти выход пока они не нашли вас.')
    else:
        txt, keyboard = generate_story(call.from_user.username,users_info[call.from_user.username]['cur_pos'])
        bot.send_message(call.message.chat.id,txt,reply_markup=keyboard)
        bot.send_message(call.message.chat.id,f'Отличный обмен! Получен {item2}',reply_markup=keyboard)
if __name__ == '__main__':
    bot.infinity_polling()
