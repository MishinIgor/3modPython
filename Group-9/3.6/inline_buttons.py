import telebot, random
with open('token_9gr.txt') as f:
    TOKEN = f.read()
button_name = ['Камень',"Ножницы","Бумага"]
bot = telebot.TeleBot(TOKEN)

markup = telebot.types.InlineKeyboardMarkup()
button1 = telebot.types.InlineKeyboardButton(text='Нажми меня!',callback_data='Руки вернул!',url='https://pytba.readthedocs.io/ru/latest/types.html#telebot.types.InlineKeyboardButton')
button2 = telebot.types.InlineKeyboardButton(text='Нажми меня!',callback_data='Руки прочь!',url='https://docs.yandex.ru/docs/view?tm=1722006326&tld=ru&lang=ru&text=телебот%20PDF&url=https%3A%2F%2Fpytba.readthedocs.io%2F_%2Fdownloads%2Fru%2Flatest%2Fpdf%2F&lr=54&mime=pdf&l10n=ru&sign=f5f8b277e67993cf7d55010aecdc1c83&keyno=0&nosw=1&serpParams=tm%3D1722006326%26tld%3Dru%26lang%3Dru%26text%3D%25D1%2582%25D0%25B5%25D0%25BB%25D0%25B5%25D0%25B1%25D0%25BE%25D1%2582%2BPDF%26url%3Dhttps%253A%2F%2Fpytba.readthedocs.io%2F_%2Fdownloads%2Fru%2Flatest%2Fpdf%2F%26lr%3D54%26mime%3Dpdf%26l10n%3Dru%26sign%3Df5f8b277e67993cf7d55010aecdc1c83%26keyno%3D0%26nosw%3D1')
markup.add(button1,button2)

keyboard = telebot.types.InlineKeyboardMarkup()
lst = []
for i in button_name:
    lst.append(telebot.types.InlineKeyboardButton(text=str(i),callback_data=str(i)))
keyboard.add(*lst)
@bot.message_handler(commands=['start'])
def start(message):
    bot.send_message(message.chat.id,'Показываю все кнопки:',reply_markup=markup)
@bot.message_handler(commands=['game'])
def game(message):
    bot.send_message(message.chat.id,'Показываю все кнопки:',reply_markup=keyboard)
@bot.callback_query_handler(func=lambda call: True)
def call_back(call):
    bot.answer_callback_query(call.id,call.data)
    bot.send_message(call.message.chat.id,f'Пользователь нажимает {call.data}')
bot.polling(non_stop=True,interval=0)
