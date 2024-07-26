# Необходимо написать бота, который по команде /coffee будет отправлять случайное фото кофе.
import telebot,requests
with open('token_15gr.txt') as f:
    TOKEN = f.read()

my_chatid = -4137666167
bot = telebot.TeleBot(TOKEN)

@bot.message_handler(commands=['coffee'])
def coffee(message):
    r = requests.get('https://coffee.alexflipnote.dev/random.json').json()
    url_rand_coffee = r['file']
    bot.send_photo(my_chatid,url_rand_coffee)
bot.polling(non_stop=True,interval=0)