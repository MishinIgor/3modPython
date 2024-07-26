import telebot,random
with open('token_5gr.txt') as f:
    TOKEN = f.read()# В файле записан только токен бота

bot = telebot.TeleBot(TOKEN)
mychat_id = -4126360445
comands = ['photo','info_my_id','help','loc_photo','loc_doc','venue','opros']
@bot.message_handler(commands=comands)
def universal(message):
    if message.text == '/photo':
        bot.send_photo(-4126360445,random.choice(['https://yt3.googleusercontent.com/ytc/AOPolaSVgk1szd5nxHt4Wp-cL3C0TXc50JbwWz9KD-OZjA=s900-c-k-c0x00ffffff-no-rj',
                                                  'https://flomaster.top/uploads/posts/2023-01/1674094500_flomaster-club-p-piton-risunok-instagram-36.png',
                                                  'https://2nskgym.ru/wp-content/uploads/2024/04/shutterstock_684957946-scaled-1.jpg']))
        bot.send_message(mychat_id,'Питон отличный язык, подойдёт для начального изучения. Очень многое поддерживается на этом языке.')
    elif message.text == '/info_my_id':
        bot.send_message(mychat_id,f'Ваш id: {message.from_user.id}')
    elif message.text == '/help':
        bot.send_message(mychat_id,f'На данный момент я поддерживаю следующие команды: {comands}')
    elif message.text == '/loc_photo':
        bot.send_photo(mychat_id,open('image.png','rb'))
    elif message.text == '/loc_doc':
        bot.send_document(mychat_id,open('image.png','rb'))
        bot.send_document(mychat_id,open('test.txt','rb'))
    elif message.text == '/venue':
        bot.send_venue(mychat_id,43.205120, 76.905024,'Тут ныкается препод', "Казахстан, Алматы")
    elif message.text == '/opros':
        que = 'Хотите разбор ДЗ?'
        ans = ('Да',"Нет", "Я вообще безпонятия что происходит", "Другое")
        bot.send_poll(mychat_id,que,ans)
@bot.message_handler(content_types=['photo'])
def myphoto_id(message):
    bot.send_message(message.chat.id,message.photo)
    
bot.polling(non_stop=True, interval=0)