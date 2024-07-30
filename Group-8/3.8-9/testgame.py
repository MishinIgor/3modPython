import telebot
from copy import deepcopy
with open('token_8gr.txt') as f:
    TOKEN = f.read()


bot = telebot.TeleBot(TOKEN)

users_info = {}

locations = {
    '1' : {'text' : 'Вы играете за героя, который попал в опасный лес, вам нужно найти выход в город и остаться живым', 'items' : [], 'next_move' : {'Пойти вперед' : '2'}, 'exchange' : {}},
    '2' : {'text' : 'Вы попали в лес и ощутили приятный аромат сосновых деревьев, который наполнил легкие. Похоже, что вы оказались в глубине дикой природы, где еще не ощущается шум городской суеты.', 'items' : [], 'next_move' : {'Пойти налево' : '3',
                                                                                                                                                                                                                                      'Пойти прямо' : '4',
                                                                                                                                                                                                                                      'Пойти направо' : '5'}, 'exchange' : {}},
    '3' : {'text' : 'На покрытой землей каменной плите сидят темные фигуры, их глаза горят в темноте, а в руках у них ножи. Они улыбаются вам и произносят "Добро пожаловать, Наш новый друг!". Вам настолько не хватает еды и воды для того, чтобы идти дальше, что вы становитесь их жертвой и все заканчивается очень плохо.', 'items' : [], 'next_move' : {}, 'exchange' : {}},
    '4' : {'text' : 'Вы вышли в поле. Перед вам торговец.', 'items' : [], 'next_move' : {'Вернуть назад' : '2'}, 'exchange' : {'шкатулка' : 'золото: 3'}},
    '5' : {'text' : 'Вы оказались около подземелья, которое смотрелось довольно страшно. ', 'items' : [], 'next_move' : {'Вернуться назад' : '2',
                                                                                'Войти внутрь' : '7',
                                                                                'Осмотреться вокруг' : '6'}, 'exchange' : {}},
    '6' : {'text' : 'Осматриваясь вокруг, вы замечаете, что на стене рядом с входом кто-то нанес странные символы, которые вы не можете разгадать. Далее ты немного еще побродил с надеждой что-то найти...', 'items' : ['шкатулка'], 'next_move' : {'Вернуться к подземелью' : '5'}, 'exchange' : {}},
    '7' : {'text' : 'Стены здесь полностью закрыты грубым камнем, а в воздухе царит прохлада и сырость. Похоже, что вы находитесь на начальном уровне подземелья.', 'items' : ['золото: 2'], 'next_move' : {'Пойти вперед' : '8',
                                                                                                                                                                                                            'Выйти на улицу' : '5'}, 'exchange' : {}},
    '8' : {'text' : 'Ты проходишь дальше, тут очень темно и сыро. Но вдруг в далеке ты замечаешь свет', 'items' : [], 'next_move' : {'Пойти дальше' : '9',
                                                                                                                                     'Вернуться' : '7'}, 'exchange' : {}},
    '9' : {'text' : 'Концовка не за горами, но прохождение не обойдется без дополнительных расходов.', 'items' : [], 'next_move' : {'Вернуться назад' : '8'}, 'exchange' : {'золото: 5' : 'выход'}}
}

def generate_story(user, position):
    # берем текстовое описание локации
    txt = locations[position]['text']
    # создаем клавиатуру
    keyboard = telebot.types.InlineKeyboardMarkup()
    # создаем кнопки с ответами по следующим ходам
    for i in users_info[user]['loc'][position]['next_move']:
        # берем текст направления
        key_txt = i
        # берем название локации
        key_data = locations[position]['next_move'][i]
        keyboard.add(telebot.types.InlineKeyboardButton(text=key_txt, callback_data=key_data))
    
    # создаем кнопки для предметов, которые можно взять
    for i in users_info[user]['loc'][position]['items']:
        # берем название предмета
        key_txt = 'Взять предмет - ' + i
        # в callback_data добавим в начало 'item ', чтобы в будущем было проще разделить обработку на несколько функций
        key_data = 'item ' + i
        keyboard.add(telebot.types.InlineKeyboardButton(text=key_txt, callback_data=key_data))
    
    # создаем кнопки для предметов которыми можем обменяться
    for i in users_info[user]['loc'][position]['exchange']:
        # проверяем, что у нас есть нужный предмет для обмена или неообходимое кол-во монет
        if i in users_info[user]['items'] or (i.startswith('золото: ') and users_info[user]['coins'] >= int(i.replace('золото: ', ''))):
            # генерируем текст обмена
            key_txt = 'Обменять предмет ' + i + ' на ' + users_info[user]['loc'][position]['exchange'][i]
            # в callback_data добавим в начало 'exchange ', чтобы в будущем было проще разделить обработку на несколько функций
            key_data = 'exchange ' + i
            keyboard.add(telebot.types.InlineKeyboardButton(text=key_txt, callback_data=key_data))

    return (txt, keyboard)


@bot.message_handler(commands=['game'])
def start_game(message):
    # добавляем пользователя в словарь с значениями по умолчанию
    users_info[message.from_user.username] = {'cur_pos' : '1', 'coins' : 0, 'items' : [], 'loc' : deepcopy(locations)}
    txt, keyboard = generate_story(message.from_user.username, users_info[message.from_user.username]['cur_pos'])
    bot.send_message(message.chat.id, txt, reply_markup=keyboard)

# если call.data в ключах словаря locations
@bot.callback_query_handler(func=lambda call: call.data in locations)
def callback_query(call):
    # меняем текущую позицию пользователя
    users_info[call.from_user.username]['cur_pos'] = call.data
    # генерируем новый текст и кнопки
    txt, keyboard = generate_story(call.from_user.username, users_info[call.from_user.username]['cur_pos'])
    # отправляем сообщение
    bot.send_message(call.message.chat.id, txt, reply_markup=keyboard)

# если call.data начинается с 'item '
@bot.callback_query_handler(func=lambda call: call.data.startswith('item '))
def callback_query(call):
    # берем название предмета (в строке заменяем подстроку 'item ' на '')
    item = call.data.replace('item ', '')
    # если предмет начинается на 'золото: '
    if item.startswith('золото: '):
        # то добавляем пользователю на баланс это кол-во монет
        users_info[call.from_user.username]['coins'] += int(item.replace('золото: ', ''))
    else:
        # иначе просто добавляем в список предметов
        users_info[call.from_user.username]['items'].append(item)
    # удалаляем с карты локаций этот предмет (чтобы повторно не взять)
    users_info[call.from_user.username]['loc'][users_info[call.from_user.username]['cur_pos']]['items'].remove(item)
    # сообщение о удачном действии
    bot.send_message(call.message.chat.id, 'Готово✔')
    # генерируем текст и кнопки и отправляем
    txt, keyboard = generate_story(call.from_user.username, users_info[call.from_user.username]['cur_pos'])
    bot.send_message(call.message.chat.id, txt, reply_markup=keyboard)


# если call.data начинается с 'exchange '
@bot.callback_query_handler(func=lambda call: call.data.startswith('exchange '))
def callback_query(call):
    # берем название предмета (в строке заменяем подстроку 'exchange ' на '')
    item1 = call.data.replace('exchange ', '')
    # берем название предмета (из словаря) , который получим
    item2 = users_info[call.from_user.username]['loc'][users_info[call.from_user.username]['cur_pos']]['exchange'][item1]
    # Если item1 начинается с 'золото: '
   
    if item1.startswith('золото: '):
        # уменьшаем кол-во монет
        # На то, что у нас достаточно монет проверять не нужно,
        # мы это уже сделали при генереции кнопок
        users_info[call.from_user.username]['coins'] -= int(item1.replace('золото: ', ''))
    else:
        # иначе удаляем предмет
        users_info[call.from_user.username]['items'].remove(item1)
   
    # если мы меняем на золото
    if item2.startswith('золото: '):
        # увеличиваем баланс
        users_info[call.from_user.username]['coins'] += int(item2.replace('золото: ', ''))
    else:
        # иначе добавляем нам предмет
        users_info[call.from_user.username]['items'].append(item2)
    # удаляем с локации этот обмен
    users_info[call.from_user.username]['loc'][users_info[call.from_user.username]['cur_pos']]['exchange'].pop(item1)
       
    # если мы обменялись на выход, то выводим сообщение о победе
    if item2 == 'выход':
        bot.send_message(call.message.chat.id, 'Тебе удалось пройти квест')
    else:
        # сообщение об удачном действии
        bot.send_message(call.message.chat.id, 'Готово✔')
        # генерируем слудующий ход
        txt, keyboard = generate_story(call.from_user.username, users_info[call.from_user.username]['cur_pos'])
        bot.send_message(call.message.chat.id, txt, reply_markup=keyboard)

if __name__ == '__main__':
    bot.infinity_polling()