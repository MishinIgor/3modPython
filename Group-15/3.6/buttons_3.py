import telebot,random
from telebot import types
with open('token_15gr.txt') as f:
    TOKEN = f.read()
my_chatid = -4137666167
bot = telebot.TeleBot(TOKEN)

jokes = [
'У меня была одна проблема, поэтому я решил написать программу, которая её решит. Теперь у меня есть 1 проблема, 9 ошибок и 12 предупреждений.',
'Если бы программисты были врачами, им бы говорили «У меня болит нога», а они отвечали «Ну не знаю, у меня такая же нога, а ничего не болит»',
'Хороший программист - проливает кофе на себя. И ноут цел, и бодрит в два раза лучше.'
]
@bot.message_handler(commands=['start'])
def start(message):
    keyboard = telebot.types.ReplyKeyboardMarkup(resize_keyboard=True)
    key_quote = telebot.types.KeyboardButton('Расскажи анекдот')
    keyboard.add(key_quote)
    bot.send_message(message.chat.id,'Потри кнопку и увидишь анекдот',reply_markup=keyboard)
def send_joke(message):
    quote = random.choice(jokes)
    bot.send_message(message.chat.id,quote)
@bot.message_handler(func=lambda message: message.text == 'Расскажи анекдот')
def quote_message(message):
    send_joke(message)
bot.polling(non_stop=True,interval=0)