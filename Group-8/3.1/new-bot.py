import telebot

with open('token_8gr.txt') as f:
    TOKEN = f.read() # Тут мы помещаем токен в константу
bot = telebot.TeleBot(TOKEN)
PROBLEMS = {
    "Интернет": {
        "Не работает подключение": "Попробуйте перезапустить роутер или ударить себя током",
        "Слишком быстрый интернет, я боюсь течения": "Не беспокойтесь, вы слишком хороши для нашего течения",
        "Я выбрал не ту категорию": "Хорошо, выберите снова."
    },
    "ТВ": {
        "Я выбрал не ту категорию": "Хорошо, выберите снова.",
        "У вас слишком цветное ТВ": "Спасибо, мы стараемся, чтобы ваши глаза были в раю",
        "У меня нет каналов с мультиками": "За то есть много каналов по программированию(это послание свыше!)"
    }
}
@bot.message_handler(content_types=['text', 'document', 'audio'])
def get_text_messages(message):
    if message.text == 'Привет':
        bot.send_message(message.from_user.id,'Добрый день! Выберите категорию: ТВ, Интернет')
    if message.text == 'ТВ':
        bot.send_message(message.from_user.id,'Какой у вас вопрос?')
    if message.text in list(PROBLEMS["ТВ"].keys()):
        bot.send_message(message.from_user.id,PROBLEMS["ТВ"][message.text])
    # elif message:
    #     bot.send_message(message.from_user.id,'Извините пожалуйста, я не знаю ответ и свяжу вас со специалистом.')

bot.polling(non_stop=True, interval=0)