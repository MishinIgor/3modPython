import telebot,random

with open('token_8gr.txt') as f:
    TOKEN = f.read() # Тут мы помещаем токен в константу
bot = telebot.TeleBot(TOKEN)

# 'text' - текстовые
# 'audio' - аудио
# 'document' - файл
# 'photo' - фото
# 'sticker' - стикеры
# "video" - видео
# "video_note" - кружочек
# "voice" - аудиосообщение
# "location" - местоположение
# "contact" - контакты
# "new_chat_members" - присоединение к чату нового пользователя
# "left_chat_member" - отсоединение пользователя от чата
# "new_chat_title" - новое название чата
# "delete_chat_photo" - удаление фото чата
# "group_chat_created" - создание чата
# "channel_chat_created" - создание канала
# "pinned_message" - закрепление сообщения
@bot.message_handler(commands=['photo','loc_photo','doc','venue','opros','voice','id'])
def send_photo(message):
    if message.text == '/photo':
        bot.send_photo(message.chat.id,'https://tardokanatomy.ru/sites/default/files/izo/programmirovanie-3-1.png')
    elif message.text == '/loc_photo':
        bot.send_photo(message.chat.id,open('image.png','rb'))
    elif message.text == '/doc':
        bot.send_document(message.chat.id,open('text.txt','rb'))
    elif message.text == '/venue':
        bot.send_venue(message.chat.id,43.205001, 76.904879,'Препод ныкается тут','Казахстан, г. Алматы')
    elif message.text == '/opros':
        que = 'Нравится ли вам заниматься программированием?'
        ans = ['Норм',
               "Очень нравится",
               "Как-то не очень",
               "Хотелось бы другого препода",
               "Отличный томада и конкурсы интересные",
               "Препод норм но программа слабенькая"]
        bot.send_poll(message.chat.id,que,ans)
    elif message.text == '/id':
        bot.send_message(message.chat.id,message.chat.id)
bot.polling(non_stop=True, interval=0)

