import telebot,random,json,copy,time
with open('token_5gr.txt') as f:
    TOKEN = f.read()
bot = telebot.TeleBot(TOKEN)

users_info = {}
# '': {'text': '', 'items': [], 'next_move': {}, 'exchange': {}}
answers = ['дыхание','эхо','вчера, сегодня, завтра', 'неправильно','февраль','в каждом']
check_ans = 0
zagadki = {
    'Легче пера, но дольше двух минут его не удержишь. Что это такое?': 'дыхание',
    "Ты меня слышишь, но не видишь. Я не говорю, пока ты не скажешь. Что я?": "эхо",
    "Назови три последовательных дня, которые не являются днями недели.": "вчера, сегодня, завтра",
    "Какое слово всегда пишется неправильно?": "неправильно",
    "В каком месяце люди меньше всего спят?": "февраль",
    "В каком месяце 28 дней?": "в каждом"
}
locations = {
    '1': {'text': 'Вы играете за героя, который попал в опасный лес, вам нужно найти выход в город и остаться живым', 'items': [], 'next_move': {'Пойти вперед': "2"}, 'exchange': {}},
    '2': {'text': 'Вы попали в лес и ощутили приятный аромат сосновых деревьев, который наполнил легкие. Похоже, что вы оказались в глубине дикой природы, где ещё не ощущается шум городской суеты.', 'items': ['фляга'], 'next_move': {"Пройти налево": "3", "Пройти прямо": "4", "Пройти направо": "5"}, 'exchange': {}},
    '3': {'text': 'на покрытой земле каменной плите сидят темные фигуры, их глаза горят в темноте, а в руках у них ножи. Они улыбаются вам и произносят "Добро пожаловать, наш новый друг!". Вам настолько не хватает еды и воды для того, чтобы идти дальше, что вы становитесь их жертвой и все заканчивается очень плохо.', 'items': [], 'next_move': {"Вы погибли. Начать сначала?": "new_game"}, 'exchange': {}},
    '4': {'text': 'Вы вышли в поле. Перед вами торговец', 'items': ['сапог'], 'next_move': {"Вернуться на перекрёсток": "2"}, 'exchange': {'шкатулка': "золото: 3"}},
    '5': {'text': 'Вы оказались около подземелья, которое смотрелось довольно страшно', 'items': ['кирка'], 'next_move': {"Вернуться": "2", "Войти в подземелье": "7", "Осмотреться": "6"}, 'exchange': {}},
    '6': {'text': 'Осматриваясь вокруг, вы замечаете, что на стене рядом с входом кто-то нанес странные символы, которые вы не можете разгадать. Далее ты немного ещё побродил с надеждой что-то найти...', 'items': ["шкатулка"], 'next_move': {"Вернуться": "5"}, 'exchange': {}},
    '7': {'text': 'Стены здесь полностью закрыты грубым камнем, а в воздухе царит прохлада и сырость. Похоже, что вы находитесь на начальном уровне подземелья.', 'items': ["золото: 2"], 'next_move': {"Вернуться": "5", "Пойти дальше": "8"}, 'exchange': {}},
    '8': {'text': 'Ты проходишь далльше, тут очень темно и сыро. Но вдруг в далеке ты замечаешь свет.', 'items': ['тетрадь по алгебре','перстень'], 'next_move': {"Вернуться": "7", "Пройти дальше": "9"}, 'exchange': {}},
    '9': {'text': 'Концовка не за горами, но прохождение не обойдется без дополнительных расходов. У выхода стоит разбойник с табличкой "выход за 5 золотых".', 'items': [], 'next_move': {}, 'exchange': {"золото: 5": "вход"}},
    '10': {'text': 'Хижина разбойников представляла собой простое строение из больших камней с хлипкой соломенной крышей. На крыше был знак с чёрными перекрещёнными костями в красном кругу. На столе в хижине разбойников стояла еда. Там были фрукты, овощи, мясо и хлеб. Также на столе можно было увидеть кувшины с водой и кружки.', 'items': ['нож','флаг воров','хлеб'], 'next_move': {'Выйти из хижина в лес': '11'}, 'exchange': {}},
    '11': {'text': 'Вы снова оказались в лесу, но уже полны сил. Вы видите знак "Налево: дикая тропа", "Прямо: Избушка", "Направо: Разбойничий пир"', 'items': [], 'next_move': {'Пойти налево': "12", "Пойти прямо": "13", "Пойти направо": "14"}, 'exchange': {}},
    '12': {'text': 'Дикая тропа в лесу представляет собой узкую, извилистую дорожку, покрытую мхом и заросшую травой. Она проходит через густые заросли деревьев, создавая ощущение таинственности и уединения. ', 'items': ['ягоды'], 'next_move': {'Выход на поле': '4','Вернуться к указателю': '11'}, 'exchange': {}},
    '13': {'text': 'В глубине густого леса, где деревья стоят так плотно, что их кроны образуют зелёный купол над головой, стоит избушка. Её стены сделаны из толстых брёвен, а крыша покрыта мхом и лишайником. Маленькие окна с деревянными ставнями пропускают немного света внутрь.', 'items': ['листок с подсказками'], 'next_move': {'Войти в избушку': '15'}, 'exchange': {}},
    '15': {'text': 'Изба внутри представляет собой тёмное и мрачное помещение. В центре комнаты расположена большая печь, служащая источником тепла и света. У стен находятся деревянные лавки и полки, на которых хранятся разные предметы, такие как метла, ступа, сушёные травы и коренья. В углу стоит старый сундук, полный тайн и загадок. Внутри вас встретила Баба-Яга. Вы должны отгадать её загадки, иначе живым не выбраться. Но если отгадаете, путь домой найти поможет.', 'items': [], 'next_move': {'Сыграть с бабой ягой': 'загадки '}, 'exchange': {}}
}

comands = {'help': 'Выводит все команды',
           'game': 'Начинает НОВУЮ игру',
           'save': 'Сохраняет игру',
           'load': 'Продолжает игру с последнего сохранения',
           'items': 'Показывает собранные предметы и золото'}
key_death = telebot.types.InlineKeyboardMarkup()
key_death.add(telebot.types.InlineKeyboardButton(text='Начать сначала', callback_data='new_game'))
key_zagadka = telebot.types.InlineKeyboardMarkup()
for i in answers:
    key_zagadka.add(telebot.types.InlineKeyboardButton(text=i,callback_data='загадки '+i))
def generate_story(user,position):
    #берем текстовое описание локации
    txt = users_info[user]['loc'][position]['text']
    #создаём клавиатуру
    keyboard = telebot.types.InlineKeyboardMarkup()
    #создаём кнопки с ответами по следующим ходам
    for i in users_info[user]['loc'][position]['next_move']:
        # берем текст направления
        key_txt = i+'🚪'
        # берем название локации
        key_data = users_info[user]['loc'][position]['next_move'][i]
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
        bot.send_message(call.message.chat.id,'Во фляге оставалось ещё "огненная вода". Вродебы, мало, но на пустой желудок ужасная смесь. Вы упали в лужу, и погибли захлебнувшись. А ведь минздрав предупреждал...',reply_markup=key_death)
    else:
        if item == 'кирка':
            bot.answer_callback_query(call.id,f'Я каменщик работаю 3 дня без зарплаты')
        elif item == 'сапог':
            bot.answer_callback_query(call.id,f'Ну и вонь из этих тапок...')
        elif item == 'перстень':
            bot.answer_callback_query(call.id,'Гравировка на перстне: "Король"')
            loc_text = '''В тёмном лесу, где деревья стояли плотной стеной, а земля была покрыта мхом, на путника напал отряд разбойников. Они были вооружены мечами и луками, их лица были скрыты капюшонами.
Путник, заметив разбойников, попытался убежать, но они быстро настигли его. Один из разбойников схватил путника за руку и сорвал с пальца перстень.
Однако, когда разбойник взглянул на перстень, его глаза расширились от удивления. На перстне была гравировка «Король». Разбойники, увидев эту надпись, испугались и отступили.
Путник, воспользовавшись моментом, вырвался из их рук и побежал дальше в лес. Разбойники остались стоять на месте, не решаясь преследовать его.'''
            users_info[call.from_user.username]['loc']['3'] = {
            'text': loc_text, 'items': [], 'next_move': {}, 'exchange': {'перстень': "выход"}
            }
            bot.send_photo(call.message.chat.id,'https://avatars.dzeninfra.ru/get-zen_doc/271828/pub_663a9dea9f669c30c357f34f_663a9e7d8f0f1a1233727a79/scale_1200')
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
        bot.send_photo(call.message.chat.id,'https://cdn.shopify.com/s/files/1/0884/4668/files/Dollarphotoclub_90793952.jpg?3721008843865200259')
    elif item2 == 'вход':
        bot.answer_callback_query(call.id,'Добро пожаловать в хижину разбойников')
        users_info[call.from_user.username]['loc']['9']['next_move'] = {'Вернуться': "8", "Войти внутрь": "10"}
        users_info[call.from_user.username]['loc']['4']['next_move']['Вернуться на дикую тропу'] = "12"
        txt, keyboard = generate_story(call.from_user.username,users_info[call.from_user.username]['cur_pos'])
        bot.send_photo(call.message.chat.id,'https://pro-dachnikov.com/uploads/posts/2023-01/1673091824_pro-dachnikov-com-p-foto-tainoi-dveri-28.jpg',reply_markup=keyboard)
    elif item2 == 'загадки':
        bot.register_next_step_handler(call,zagadki)
    else:
        # сообщение об удачном действии
        bot.answer_callback_query(call.id,'Обмен завершён')
        bot.send_message(call.message.chat.id,f'Получено {item2}')
        txt, keyboard = generate_story(call.from_user.username,users_info[call.from_user.username]['cur_pos'])
        bot.send_message(call.message.chat.id,txt,reply_markup=keyboard)
@bot.callback_query_handler(func = lambda call: call.data.startswith('загадки '))
def game_babayaga(call):
    zagadka = random.choice(list(zagadki.keys()))
    if 'листок с подсказками' in users_info[call.from_user.username]['items']:
        bot.send_message(call.message.chat.id,zagadka)
if __name__ == '__main__':
    bot.infinity_polling()