import telebot,random

with open('token_15gr.txt') as f:
    TOKEN = f.read() # Тут будем хранить наш токен

bot = telebot.TeleBot(TOKEN)

@bot.message_handler(commands=['photo','loc_photo','doc','venue'])
def universal(message):
    if message.text == '/photo':
        bot.send_photo(message.chat.id,
                   random.choice(['https://u2.9111s.ru/uploads/202304/14/709e295519328b25eae5b223206c5831.jpg',
                        'https://apelsin-centr.ru/upload/iblock/66d/ghx0otisvyti5vvqeec4awl4h0wkkt2p.jpg',
                        'https://www.sevenstarwebsolutions.com/wp-content/uploads/2019/07/Python-Web-Development.png']))
        bot.send_photo(1251102161,random.choice(['https://u2.9111s.ru/uploads/202304/14/709e295519328b25eae5b223206c5831.jpg',
                        'https://apelsin-centr.ru/upload/iblock/66d/ghx0otisvyti5vvqeec4awl4h0wkkt2p.jpg',
                        'https://www.sevenstarwebsolutions.com/wp-content/uploads/2019/07/Python-Web-Development.png']))
    elif message.text == '/loc_photo':
        bot.send_photo(message.chat.id,open(random.choice(['image.png']),'rb'))
    elif message.text == '/doc':
        bot.send_document(1251102161,open('image.png','rb'))
        bot.send_document(message.chat.id,open('image.png','rb'))
    elif message.text == '/venue':
        bot.send_venue(message.chat.id,43.205120, 76.905024,'Тут ныкается препод',"Казахстан, Алматы")
        bot.send_venue(message.chat.id,55.012508, 73.332408,'Алексей Кузнецов',"Что-то, где-то") 
        bot.send_venue(5205857297,43.205120, 76.905024,'Тут ныкается препод',"Казахстан, Алматы")
        bot.send_venue(5205857297,55.012508, 73.332408,'Алексей Кузнецов',"Что-то, где-то") #5205857297
bot.polling(non_stop=True, interval=0)