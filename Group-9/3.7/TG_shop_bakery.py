import telebot, random, json
with open('token_9gr.txt') as f:
    TOKEN = f.read()
bot = telebot.TeleBot(TOKEN)
#Считываем из файла данные  если он сущесвтует. Если нет создаём пустой словарь
try:
    with open('shop_bakery_gr9.json',encoding='utf-8') as f:
        shop = json.load(f)
except Exception:
    shop = {}
products = {
    'Хлеб белый': 25,
    "Хлеб чёрный": 27,
    "Булочка с изюмом": 20
}
user_plata_id = 0
keyboard_products = telebot.types.InlineKeyboardMarkup()
for i,j in products.items():
    keyboard_products.add(telebot.types.InlineKeyboardButton(text=f'{i}-{j}',callback_data=i))
keyboard_products.add(telebot.types.InlineKeyboardButton(text='Завершить',callback_data='Завершить'))
keyboard_score = telebot.types.InlineKeyboardMarkup()
button_yes = telebot.types.InlineKeyboardButton(text='Да',callback_data='Да')
button_no = telebot.types.InlineKeyboardButton(text='Нет',callback_data='Нет')
keyboard_score.row(button_yes,button_no)
comands = {'help': 'Выводит все команды которые может выполнить бот',
           'info': 'Выводит зарегистрированных пользователей',
           'create_client': "Регистрация клиента",
           "create_buy": "Создание покупки",
           "оплачено": "Команда вводится после оплаты счёта для подтверждения оплаты",
           }
@bot.message_handler(commands=list(comands.keys()))
def universal(message):
    if message.text == '/help':
        for i,j in comands.items():
            bot.send_message(message.chat.id,f'/{i} - {j}')
    elif message.text == '/create_client':
        if str(message.from_user.id) in list(shop.keys()):
            bot.send_message(message.chat.id,'Вы уже есть в списке клиентов')
        else:
            shop[message.from_user.id] = {'TG_fist_name': message.from_user.first_name, 'TG_name': '@'+message.from_user.username, 'покупка': [], 'счёт': 0}
            with open('shop_bakery_gr9.json', 'w',encoding='utf-8') as f:
                json.dump(shop,f,indent=2,ensure_ascii=False)
            bot.send_message(message.chat.id,'Вы внесены в список клиентов')
    elif message.text == '/info':
        for i,j in shop.items():
            bot.send_message(message.chat.id,f'{j}')
    elif message.text == '/create_buy':
        if str(message.from_user.id) in list(shop.keys()):
            bot.send_message(message.chat.id,'Выберите товар',reply_markup=keyboard_products)
        else:
            bot.send_message(message.chat.id,'Вас нет в списке клиентов, введите команду /create_client и повторите запрос.')
    elif message.text == '/оплачено':
        global user_plata_id
        user_plata_id = str(message.from_user.id)
        bot.send_message(1680980801,f'Подтвердите оплату счёта от {shop[user_plata_id]}',reply_markup=keyboard_score)
@bot.callback_query_handler(func = lambda call: True)
def callback_query(call):
    global shop
    a = []
    if call.data in list(products.keys()):
        bot.answer_callback_query(call.id,f'В корзину добавлен {call.data}')
        a += call.data
    elif call.data == 'Завершить':
        bot.send_message(call.message.chat.id,f'Товары в корзине: {a}, К оплате: {shop[call.from_user.id]["счёт"]}')
        bot.send_message(call.message.chat.id,f'Оплатить можно по номеру 8-999-495-34-80, после оплаты введите /оплачено')
        with open('shop_bakery_gr9.json', 'w',encoding='utf-8') as f:
                json.dump(shop,f,indent=2,ensure_ascii=False)
    elif call.data == 'Да':
        shop[user_plata_id]['покупка'] = []
        shop[user_plata_id]['счёт'] = 0
        with open('shop_bakery_gr9.json', 'w',encoding='utf-8') as f:
                json.dump(shop,f,indent=2,ensure_ascii=False)
        bot.send_message(user_plata_id,'Ваша оплата подтверждена. Ожидайте заказ')
    elif call.data == 'Нет':
        bot.send_message(call.message.chat.id,f'Оплата не подтверждена, повторите отправку чека пожалуйста.')


if __name__ == '__main__':
    bot.infinity_polling()
