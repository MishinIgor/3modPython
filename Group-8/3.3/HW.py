# Постановка задачи: 
# Создать бота, который из сообщения пользователя будет создавать опрос. 
# Первая строка сообщения пользователя - вопрос,
# 2 - 11 строки - варианты ответов. Если сообщение пользователя менее 3 строк или более 11,
# то выводить соответствующее сообщение. 
import telebot,random

with open('token_8gr.txt') as f:
    TOKEN = f.read() # Тут мы помещаем токен в константу
my_bot = telebot.TeleBot(TOKEN)

#Получение любого другого сообщения
@my_bot.message_handler(content_types=['text', 'photo', 'sticker'])
def handle_message(message):
    #Обработка ошибки
    try:
        #Ответ на текстовое сообщение
        if message.text:
            #Проверяем ошибку передачи геолокации
            if message.text == "Отправить 🗺️":
                my_bot.reply_to(message, "Ваш браузер не поддерживает передачу геолокации", reply_markup=telebot.types.ReplyKeyboardRemove())
            #Проверяем присутствуют ли переносы в сообщении. Если нет просто повторяем сообщение
            elif message.text.count("\n") > 0:
                #Проверяем количество строк. Предварительно убираем пустые элементы.
                if len(list(filter(None, message.text.split('\n')))) in range(3,12):
                    #Разбиваем сообщение на строки и создаем список. Удаляем пустые элементы, если они были.
                    msg_line = list(filter(None, message.text.split('\n')))
                    que = msg_line[0]
                    ans = msg_line[1:]
                    #Отправляем сообщение с опросом. Первая строка - вопрос, остальные строки - варианты ответов.
                    my_bot.send_poll(message.chat.id, que, ans)
                else:
                    my_bot.reply_to(message, "Для создания опроса в Вашем сообщении должно быть от 3 до 11 строк.\nПервая строка - вопрос, остальные строки - варианты ответов.", reply_markup=telebot.types.ReplyKeyboardRemove())
            else:
                my_bot.reply_to(message, message.text, reply_markup=telebot.types.ReplyKeyboardRemove())
    
        #Ответ на изображение
        if message.photo:
            my_bot.send_message(message.chat.id, "Вы прислали изображение", reply_markup=telebot.types.ReplyKeyboardRemove())
    
        #Ответ на стикер
        if message.sticker:
            my_bot.send_message(message.chat.id, message.sticker, reply_markup=telebot.types.ReplyKeyboardRemove())

    except Exception:
        my_bot.send_message(message.chat.id, "Ошибка ввода данных", reply_markup=telebot.types.ReplyKeyboardRemove())
my_bot.polling(non_stop=True, interval=0)