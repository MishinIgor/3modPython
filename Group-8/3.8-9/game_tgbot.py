import telebot,random,json
from copy import deepcopy
with open('token_8gr.txt') as f:
    TOKEN = f.read()
bot = telebot.TeleBot(TOKEN)
users_info = {}
locations = { '1': {'text': 'Вы играете за героя, который попал в опасный лес. Вам нужно найти выход в город и остаться живым.', 
                    'items': [], 'next_move': {'Пойти вперёд': '2'}, 'exchange': {} },
             '2': {'text': 'Вы попали в лес и ощутили приятный аромат сосновых деревьев, который наполнил легкие. Похоже, что вы оказались в глубине дикой природы, где ещё не ощущается шум городской суеты.', 'items': ['фляга'], 
                   'next_move': {"Пойти налево": "3",
                                 "Пойти прямо": "4",
                                 "Пойти направо": "5"}, 'exchange': {}},
            '3': {'text': 'На покрытой землёй каменной плите сидят темные фигуры, их глаза горяд в темноте, а в руках у них ножи. Они улыбаются вам и произносят "Добро пожаловать, Наш новый друг!". Вам настолько не хватает еды и воды для того, чтобы идти дальше, что вы становитесь их жертвой и все заканчивается очень плохо.', 'items': [], 'next_move': {"Вы погибли💀. Начать заного": "new_game"}, 'exchange': {}},
            '4': {'text': 'Вы вышли в поле. Перед вами торговец.', 'items': [], 'next_move': {"Вернуться назад": "2"}, 'exchange': {"шкатулка": "золото: 3"} },
            "5": {'text': 'Вы оказались около подземелья, которое смотрелось довольно страшно.', 'items': ['дубинка'], 'next_move': {'Вернуться назад': '2', "Войти внутрь": "7", "Осмотреться вокруг": "6"}, 'exchange': {} },
            "6": {'text': "Осматриваясь вокруг, вы замеаете, что на стене рядом с входом кто-то нанес странные символы, которые вы не можете разгадать. Далее Вы немного ещё побродил с надеждой что-то найти...", 'items': ["шкатулка"], 'next_move': {'Вернуться к подземелью': '5'}, 'exchange': {} },
            "7": {'text': 'Стены здесь полностью закрыты грубым камнем, а в воздухе царит прохлада и сырость. Похоже, что вы находитесь на начальном уровне подземелья', 'items': ["золото: 2"], 'next_move': {"Пройти вперёд": "8", "Выйти на улицу": "5"}, 'exchange': {}},
            "8": {'text': 'Ты проходишь дальше, тут очень темно и сыро. Но вдруг в далеке ты замечаешь свет', 'items': ['револьвер'], 'next_move': {"Пойти дальше": "9", "Вернуться": "7"}, 'exchange': {} },
            "9": {'text': 'Концовка не за горами, но похождение не обойдется без дополнительных расходов.', 'items': ['перстень'], 'next_move': {"Вернуться назад": "8"}, 'exchange': {"золото: 5": "new_location"} },
            "10": {'text': 'Тропа из леса при закате выглядит особенно живописно. Тёплые лучи солнца окрашивают деревья в золотисто-красные оттенки, создавая атмосферу волшебства и умиротворения. Теперь возвращение домой уже не выглядит как сказка.', 'items': ['фляга'], 'next_move': {"Тропа домой": "выход"}, 'exchange': {} }
             }
locations2 = {}
comands = {'help': 'Выводит список допустимы команд',
           'start': 'Начинает НОВУЮ игру',
           'save': 'Сохраняет текущий прогресс',
           'load': 'Начинает игру с последнего сохранения',
           'items': 'Выводит инвентарь'}
keyboard_dead = telebot.types.InlineKeyboardMarkup()
keyboard_dead.add(telebot.types.InlineKeyboardButton(text='Вы погибли, начать сначала 💀',callback_data='new_game'))
def generate_story(user,position):
    #берем текстовое описание локации
    txt = users_info[user]['loc'][position]['text']
    # создаём клавиатуру
    keyboard = telebot.types.InlineKeyboardMarkup()
    #Создаём кнопки с ответами по следующим ходам
    for i in users_info[user]['loc'][position]['next_move']:
        key_txt = i+' 🚪'
        key_data = users_info[user]['loc'][position]['next_move'][i]
        keyboard.add(telebot.types.InlineKeyboardButton(text = key_txt, callback_data=key_data))
    #Создаём кнопки для подбора предметов
    for i in users_info[user]['loc'][position]['items']:
        #берем название предметов
        key_txt = f'Взять предмет - {i}🔍'
        # в callback_data добавим в начало 'item', чтобы в будущем было проще разделить обработку на несколько функций
        key_data = 'item ' + i
        keyboard.add(telebot.types.InlineKeyboardButton(text=key_txt, callback_data= key_data))
    #Создаём кнопки для обмена
    for i in users_info[user]['loc'][position]['exchange']:
        # проверяем, что у нас есть нужный предмет для обмена или неообходимое кол-во монет
        if i in users_info[user]['items'] or (i.startswith('золото: ') and users_info[user]['золото'] >= int(i.replace('золото: ',''))):
            # генерируем текст обмена
            key_txt = f'👉обменять предмет {i} на {users_info[user]['loc'][position]['exchange'][i]}🤝'
            # в callback_data добавим в начало 'exchange ', чтобы в будущем было проще разделить обработку на несколько функций
            key_data = 'exchange ' + i
            keyboard.add(telebot.types.InlineKeyboardButton(text=key_txt, callback_data=key_data))
    return (txt,keyboard)
@bot.message_handler(commands=list(comands.keys()))
def start_game(message):
    global users_info
    if message.text == '/help':
        info = ''
        for key,value in comands.items():
            info += f'/{key} - {value} \n'
        bot.send_message(message.chat.id,info)
    elif message.text == '/start':
        # добавляем пользователя в словарь с значениями по умолчанию
        users_info[message.from_user.username] = {'cur_pos': '1', 'золото': 0, 'items': [], 'loc': deepcopy(locations)}
        txt, keyboard = generate_story(message.from_user.username,users_info[message.from_user.username]['cur_pos'])
        bot.send_message(message.chat.id, txt, reply_markup=keyboard)
    elif message.text == '/save':
        with open(f'{message.from_user.id}_gr8.json','w',encoding='utf-8') as f:
            json.dump(users_info[message.from_user.username],f,indent=2,ensure_ascii=False)
    elif message.text == '/load':
        try:
            with open(f'{message.from_user.id}_gr8.json','r',encoding='utf-8') as f:
                users_info[message.from_user.username] = json.load(f)
            txt, keyboard = generate_story(message.from_user.username,users_info[message.from_user.username]['cur_pos'])
            bot.send_message(message.chat.id, txt, reply_markup=keyboard)
        except Exception as exc:
            bot.send_message(message.chat.id, f'Сохранений не найдено(ошибка: {exc}). Начните новую игру введя /start')
    elif message.text == '/items':
        txt, keyboard = generate_story(message.from_user.username,users_info[message.from_user.username]['cur_pos'])
        all_items = (',').join(users_info[message.from_user.username]["items"])
        bot.send_message(message.chat.id,f'Золото: {users_info[message.from_user.username]["золото"]}')
        bot.send_message(message.chat.id,f'Предметы: {all_items}',reply_markup=keyboard)
@bot.callback_query_handler(func= lambda call: call.data in locations)
def callback_query(call):
    # меняем текущую позицию пользователя
    users_info[call.from_user.username]['cur_pos'] = call.data
    # генерируем новый текст и кнопки
    txt, keyboard = generate_story(call.from_user.username, users_info[call.from_user.username]['cur_pos'])
    # отправляем сообщение
    bot.send_message(call.message.chat.id,txt,reply_markup=keyboard)
@bot.callback_query_handler(func = lambda call: call.data.startswith('item '))
def callback_query(call):
    # берем название предмета (в строке заменяем подстроку 'item' На '')
    item = call.data.replace('item ', '')
    users_info[call.from_user.username]['loc'][users_info[call.from_user.username]['cur_pos']]['items'].remove(item)
    txt, keyboard = generate_story(call.from_user.username,users_info[call.from_user.username]['cur_pos'])
    if item.startswith('золото: '):
        #то добавляем пользователю на баланс это кол-во монет
        users_info[call.from_user.username]['золото'] += int(item.replace('золото: ',""))
        bot.send_message(call.message.chat.id, f'Получено {item}',reply_markup=keyboard)
    elif item == 'фляга':
        bot.answer_callback_query(call.id,'Вы погибли')
        bot.send_message(call.message.chat.id, 'На дне фляги ещё оставалась "огненная вода". Вы решили попробовать его для храбрости, но на пустой желудок вы лишь упали лицом в лужу и захлебнулись. А ведь минздрав предупреждал...',reply_markup=keyboard_dead)
    elif item == 'револьвер':
        bot.answer_callback_query(call.id,'Вы погибли')
        bot.send_message(call.message.chat.id, 'Вы нашли отличное, но старое оружие. Когда вы попытались положить револьвер себе под пояс, случайно нажали на курок. Пуля рекошетила по всему подземелью и попала вам в голову.',reply_markup=keyboard_dead)
    elif item == 'перстень':
        bot.answer_callback_query(call.id,'Перстень словно сковал палец. Но теперь вы чувствуете, что вас никто не тронет.')
        users_info[call.from_user.username]['loc']['3']['text'] = 'На путника напали разбойники, но, увидев перстень главы разбойников на его руке, они отступили. Путник был одет в простую одежду, но его перстень был украшен драгоценными камнями и излучал яркое сияние. Разбойники узнали перстень своего главаря и поняли, что перед ними человек, обладающий властью и влиянием. Испугавшись наказания за нападение на такого человека, разбойники отступили.'
        users_info[call.from_user.username]['loc']['3']['next_move'] = {'Тропа из леса': '10'}
        bot.send_photo(call.message.chat.id,'https://fine-jewellery.ru/wp-content/files_mf/1397408142печаткасгербомиззолота.jpg',reply_markup=keyboard)
    else:
        #Иначе просто добавляем в список предметов
        users_info[call.from_user.username]['items'].append(item)
        #сообщение о удачном действии
        bot.send_message(call.message.chat.id, f'Получено {item}')
        #Генерируем текст и кнопки и отправляем
        bot.send_message(call.message.chat.id,txt,reply_markup=keyboard)
@bot.callback_query_handler(func = lambda call: call.data == 'выход')
def the_end(call):
    bot.send_message(call.message.chat.id, 'Молодец! Вот на тебе 🧠, больше не теряйся и не теряй.')
    bot.send_photo(call.message.chat.id, 'https://wallpapers.com/images/file/inspirational-kneeling-man-hoct4hym94sin20x.jpg')
@bot.callback_query_handler(func = lambda call: call.data.startswith('exchange '))
def callback_query(call):
    #Берем название предмета(в строке заменяем подстроку 'exchange ' на '')
    item1 = call.data.replace('exchange ','')
    # берем название предмета (из словаря), который получим
    item2 = users_info[call.from_user.username]['loc'][users_info[call.from_user.username]['cur_pos']]['exchange'][item1]
    # Если item1 начинается с 'золото: '
    if item1.startswith('золото: '):
        #уменьшаем кол-во монет
        #на то, что у нас достаточно монет проверять не нужно,мы это уже сделали при генерации кнопок
        users_info[call.from_user.username]['золото'] -= int(item1.replace('золото: ', ''))
    else:
        #иначе удаляем предмет
        users_info[call.from_user.username]['items'].remove(item1)
    # если мы меняем на золото
    if item2.startswith('золото: '):
        #увеличиваем баланс
        users_info[call.from_user.username]['золото'] += int(item2.replace('золото: ', ''))
    else:
        # иначе добавляем нам предмет
        users_info[call.from_user.username]['items'].append(item2)
    # удаляем с локации этот обмен
    users_info[call.from_user.username]['loc'][users_info[call.from_user.username]['cur_pos']]['exchange'].pop(item1)
       
    # если мы обменялись на выход, то выводим сообщение о победе
    # сообщение об удачном действии
    bot.send_message(call.message.chat.id, f'Получено {item2}. Отличный обмен!')
    # генерируем слудующий ход
    txt, keyboard = generate_story(call.from_user.username, users_info[call.from_user.username]['cur_pos'])
    bot.send_message(call.message.chat.id, txt, reply_markup=keyboard)
@bot.callback_query_handler(func = lambda call: call.data == 'new_game')
def new_game(call):
    users_info[call.from_user.username] = {'cur_pos': '1', 'золото': 0, 'items': [], 'loc': deepcopy(locations)}
    txt, keyboard = generate_story(call.from_user.username,users_info[call.from_user.username]['cur_pos'])
    bot.send_message(call.message.chat.id, txt, reply_markup=keyboard)
@bot.callback_query_handler(func = lambda call: call.data == 'new_location')
def new_loc(call):
    users_info[call.from_user.username] = {'cur_pos': '1', 'золото': 0, 'items': users_info['items'], 'loc': deepcopy(locations2)}
    txt, keyboard = generate_story(call.from_user.username,users_info[call.from_user.username]['cur_pos'])
    bot.send_message(call.message.chat.id, txt, reply_markup=keyboard)
bot.polling(non_stop=True, interval=0)