import telebot,random,os,json # Импортирует модуль для тг-ботов и для загрузки интернет-ссылок
with open('token_8gr.txt') as f: # Импортирует модуль с токеном
    TOKEN = f.read()
import Map

COMMAND_LIST = """
Ваша задача проста: дойти до выхода

Список команд:

/start - Регистрирует игрока и начинает игру
/help или /command_list - Показывает список команд

/move - Переместиться (Или зайти в торговлю)
/battle - Показать действия в бою
/items - Показывает список предметов и позволяет их использовать
/sell - Если Вы можете торговать - продаёт ваши предметы
/take - Берёт предметы с клетки (Если есть)

/map - Регистрирует новую изменяемую карту
/delete_pers - Удаляет персонажа
"""

bot = telebot.TeleBot(TOKEN) # Загружает бота в программу, используя токен из модуля conf, для загрузки токена достаточно создать в генеральной папке файл conf.py и в константу TOKEN загрузить токен
User = {
    "class":'',
    
    "parameters":{
        "Здоровье":100,
        "Энергия":100,
        "Защита":0,
    },
    
    "characteristics":{
        "Дальнозоркость":1,
        "Максимальное Здоровье":100,
        "Максимальная Энергия":100,
        },
    
    "items":[],
    "money":50,
    "weapon":"",
    
    "position":(0,0),
    "monsters":[],
}

characteristics_control = {
    "Здоровье":"Максимальное Здоровье",
    "Энергия":"Максимальная Энергия"
}

Weapons = {
    "Меч":{
        "Диапазон Урона":(3,5),
        "Энергозатратность":15,
    },
    "Клинок":{
        "Диапазон Урона":(2,4),
        "Энергозатратность":10,
    },
    "Алебарда":{
        "Диапазон Урона":(10,12),
        "Энергозатратность":30
    },
    "Копьё":{
        "Диапазон Урона":(3,8),
        "Энергозатратность":20
    },
}

Items = {
    "Зелье Здоровья":{
        
        "type":"potion",
        "price":25,
        
        "potion_effect_on":"Здоровье",
        "potion_effectiveness":20,
    },
    "Большое Зелье Здоровья":{
        
        "type":"potion",
        "price":40,
        
        "potion_effect_on":"Здоровье",
        "potion_effectiveness":40,   
    },
    "Зелье Энергии":{
        
        "type":"potion",
        "price":25,
        
        "potion_effect_on":"Энергия",
        "potion_effectiveness":30,
    },
    "Большое Зелье Энергии":{
        
        "type":"potion",
        "price":35,
        
        "potion_effect_on":"Энергия",
        "potion_effectiveness":45, 
    },
    
    "Свиток Железной Кожи":{
        
        "type":"scroll",
        "price":40,
        
        "scroll_effect":"parameters",
        "scroll_effect_on":"Защита",
        "scroll_effectiveness":10
    },
    "Свиток Орлиного Хрусталя":{
        
        "type":"scroll",
        "price":70,
        
        "scroll_effect":"characteristics",
        "scroll_effect_on":"Дальнозоркость",
        "scroll_effectiveness":1
    },
    "Свиток Сердечного Панциря":{
        
        "type":"scroll",
        "price":50,
        
        "scroll_effect":"characteristics",
        "scroll_effect_on":"Максимальное Здоровье",
        "scroll_effectiveness":20
    },
    "Свиток Неистяжимой Стойкости":{
        
        "type":"scroll",
        "price":45,
        
        "scroll_effect":"characteristics",
        "scroll_effect_on":"Максимальная Энергия",
        "scroll_effectiveness":20
    },
    
    "Алебарда":{
        
        "type":"weapon",
        "price":125
    },
    "Копьё":{
        
        "type":"weapon",
        "price":85
    },
    "Меч":{
        
        "type":"weapon",
        "price":60
    },
    "Клинок":{
        
        "type":"weapon",
        "price":50
    },
}


MAP_SIZE = 20

@bot.message_handler(commands=['start'])
def start(message):
    global User
    
    if not os.path.exists(f"Data/{message.from_user.id}.json"):
        User["position"] = [random.randint(MAP_SIZE//2-MAP_SIZE//4,MAP_SIZE//2+MAP_SIZE//4),random.randint(MAP_SIZE//2-MAP_SIZE//4,MAP_SIZE//2+MAP_SIZE//4)]
        map_list,image,monsters = Map.generate(MAP_SIZE,MAP_SIZE,User["position"])
        User["monsters"] = monsters
        User["map"] = map_list
        User["Map_Message"] = 0
        User["status"] = "Free"
        Map.Map_save(image,f"Data/{message.from_user.id}.png")
        classes = telebot.types.InlineKeyboardMarkup(row_width=1,)
        class_knight = telebot.types.InlineKeyboardButton("Рыцарь",callback_data=f"рыцарь {message.from_user.id}")
        class_rogue = telebot.types.InlineKeyboardButton("Разбойник",callback_data=f"разбойник {message.from_user.id}")
        classes.add(class_knight,class_rogue)
        bot.send_message(message.chat.id,f"Выберите Класс Персонажа",reply_markup=classes)
    else:
        bot.send_message(message.chat.id,f"{message.from_user.username} уже зарегистрирован")

@bot.callback_query_handler(func= lambda call: 'рыцарь' in call.data)
def class_knigth(call):
    bot.edit_message_reply_markup(call.message.chat.id,call.message.id)
    user_id = call.data.replace('рыцарь ','')
    User["class"] = "Рыцарь"
    User["parameters"]["Защита"] = 10
    User["weapon"] = "Меч"
    with open(f"Data/{user_id}.json","w",encoding='utf-8') as newuserfile:
        json.dump(User,newuserfile,ensure_ascii=False)
    Map.render(user_id)
    User["Map_Message"] = bot.send_photo(call.message.chat.id,open(f"Data/{user_id}.png","rb")).message_id
    with open(f"Data/{user_id}.json","w",encoding='utf-8') as newuserfile:
        json.dump(User,newuserfile,ensure_ascii=False)
    bot.send_message(call.message.chat.id,f"Игрок зарегистрирован")
    
@bot.callback_query_handler(func= lambda call: 'разбойник' in call.data)
def class_rogue(call):
    bot.edit_message_reply_markup(call.message.chat.id,call.message.id)
    user_id = call.data.replace('разбойник ','')
    User["class"] = "Разбойник"
    User["parameters"]["Защита"] = 3
    User["weapon"] = "Клинок"
    with open(f"Data/{user_id}.json","w",encoding='utf-8') as newuserfile:
        json.dump(User,newuserfile,ensure_ascii=False)
    Map.render(user_id)
    User["Map_Message"] = bot.send_photo(call.message.chat.id,open(f"Data/{call.message.from_user.id}.png","rb")).message_id
    with open(f"Data/{user_id}.json","w",encoding='utf-8') as newuserfile:
        json.dump(User,newuserfile,ensure_ascii=False)
    bot.send_message(call.message.chat.id,f"Игрок зарегистрирован")
    
    
    
    
@bot.message_handler(commands=['map'])
def map_show(message):
    Map.render(message.from_user.id)
    with open(f"Data/{message.from_user.id}.json","r",encoding='utf-8') as userfile:
        user = json.load(userfile)
    user["Map_Message"] = bot.send_photo(message.chat.id,open(f"Data/{message.from_user.id}.png","rb")).message_id
    with open(f"Data/{message.from_user.id}.json","w",encoding='utf-8') as newuserfile:
        json.dump(user,newuserfile,ensure_ascii=False)
    
def map_update(user_id,chat_id):
    Map.render(user_id)
    with open(f"Data/{user_id}.json","r",encoding='utf-8') as userfile:
        user = json.load(userfile)
    bot.edit_message_media(telebot.types.InputMediaPhoto(open(f"Data/{user_id}.png","rb")),chat_id,user["Map_Message"])
    
    
    
    
@bot.message_handler(commands=['move'])
def move(message):
    with open(f"Data/{message.from_user.id}.json","r",encoding='utf-8') as user_file:
        user = json.load(user_file)
    move_sides = telebot.types.InlineKeyboardMarkup()
    
    character_tile = user["map"][user["position"][1]][user["position"][0]]
    
    if user["status"] == "Free" or user["status"] == "Trade":
        if user["status"] == "Trade":
            move_trade = telebot.types.InlineKeyboardButton("Торговать",callback_data=f'trade {message.from_user.id}')
            move_sides.add(move_trade)
        
        if user["position"][0] > 0 and ("object" in user["map"][user["position"][1]][user["position"][0]-1] and user["map"][user["position"][1]][user["position"][0]-1]["object"]["passability"] or not "object" in user["map"][user["position"][1]][user["position"][0]-1]):
            move_left = telebot.types.InlineKeyboardButton("Идти Влево",callback_data=f"move_left {message.from_user.id}")
            move_sides.add(move_left)
            
        if user["position"][1] > 0 and ("object" in user["map"][user["position"][1]-1][user["position"][0]] and user["map"][user["position"][1]-1][user["position"][0]]["object"]["passability"] or not "object" in user["map"][user["position"][1]-1][user["position"][0]]):
            move_up = telebot.types.InlineKeyboardButton("Идти Вверх",callback_data=f"move_up {message.from_user.id}")
            move_sides.add(move_up)
            
        if user["position"][0] < MAP_SIZE-1 and ("object" in user["map"][user["position"][1]][user["position"][0]+1] and user["map"][user["position"][1]][user["position"][0]+1]["object"]["passability"] or not ("object" in user["map"][user["position"][1]][user["position"][0]+1])) :
            move_right = telebot.types.InlineKeyboardButton("Идти Вправо",callback_data=f"move_right {message.from_user.id}")
            move_sides.add(move_right)
            
        if user["position"][1] < MAP_SIZE-1 and ("object" in user["map"][user["position"][1]+1][user["position"][0]] and user["map"][user["position"][1]+1][user["position"][0]]["object"]["passability"] or not ("object" in user["map"][user["position"][1]+1][user["position"][0]])):
            move_down = telebot.types.InlineKeyboardButton("Идти Вниз",callback_data=f"move_down {message.from_user.id}")
            move_sides.add(move_down)
        
        bot.send_message(message.chat.id,f"Выберите, в какую сторону желаете идти",reply_markup=move_sides)
    elif user["status"] == "Battle":
        bot.send_message(message.chat.id,f"Вы вступили в бой с {user['monsters'][user['Battle_with']]['name']}\nВведите /battle для ведения боя")
    
@bot.callback_query_handler(func = lambda call: "move_left" in call.data)
def move_left(call):
    user_id = call.data.replace("move_left ",'')
    with open(f"Data/{user_id}.json","r",encoding='utf-8') as user_file:
        user = json.load(user_file)
    if user["parameters"]["Энергия"]<= user["characteristics"]["Максимальная Энергия"] - 5:
        user["parameters"]["Энергия"] += 5
    elif user["parameters"]["Энергия"] < user["characteristics"]["Максимальная Энергия"]:
        user["parameters"]["Энергия"] = user["characteristics"]["Максимальная Энергия"]
    user["position"][0] -= 1
    with open(f"Data/{user_id}.json","w",encoding='utf-8') as user_file:
        json.dump(user,user_file,ensure_ascii=False)
    bot.edit_message_reply_markup(call.message.chat.id,call.message.id)
    bot.send_message(call.message.chat.id,"Вы пошли налево")
    map_update(user_id,call.message.chat.id)
    monsters_move(user_id,call.message.chat.id)
    on_exit(user,user_id,call.message.chat.id)

@bot.callback_query_handler(func = lambda call: "move_up" in call.data)
def move_up(call):
    user_id = call.data.replace("move_up ",'')
    with open(f"Data/{user_id}.json","r",encoding='utf-8') as user_file:
        user = json.load(user_file)
    if user["parameters"]["Энергия"]<= user["characteristics"]["Максимальная Энергия"] - 5:
        user["parameters"]["Энергия"] += 5
    elif user["parameters"]["Энергия"] < user["characteristics"]["Максимальная Энергия"]:
        user["parameters"]["Энергия"] = user["characteristics"]["Максимальная Энергия"]
    user["position"][1] -= 1
    with open(f"Data/{user_id}.json","w",encoding='utf-8') as user_file:
        json.dump(user,user_file,ensure_ascii=False)
    bot.edit_message_reply_markup(call.message.chat.id,call.message.id)
    bot.send_message(call.message.chat.id,"Вы пошли вверх")
    map_update(user_id,call.message.chat.id)
    monsters_move(user_id,call.message.chat.id)
    on_exit(user,user_id,call.message.chat.id)
    
@bot.callback_query_handler(func = lambda call: "move_right" in call.data)
def move_right(call):
    user_id = call.data.replace("move_right ",'')
    with open(f"Data/{user_id}.json","r",encoding='utf-8') as user_file:
        user = json.load(user_file)
    if user["parameters"]["Энергия"]<= user["characteristics"]["Максимальная Энергия"] - 5:
        user["parameters"]["Энергия"] += 5
    elif user["parameters"]["Энергия"] < user["characteristics"]["Максимальная Энергия"]:
        user["parameters"]["Энергия"] = user["characteristics"]["Максимальная Энергия"]
    user["position"][0] += 1
    with open(f"Data/{user_id}.json","w",encoding='utf-8') as user_file:
        json.dump(user,user_file,ensure_ascii=False)
    bot.edit_message_reply_markup(call.message.chat.id,call.message.id)
    bot.send_message(call.message.chat.id,"Вы пошли направо")
    map_update(user_id,call.message.chat.id)
    monsters_move(user_id,call.message.chat.id)
    on_exit(user,user_id,call.message.chat.id)
    
@bot.callback_query_handler(func = lambda call: "move_down" in call.data)
def move_down(call):
    user_id = call.data.replace("move_down ",'')
    with open(f"Data/{user_id}.json","r",encoding='utf-8') as user_file:
        user = json.load(user_file)
    if user["parameters"]["Энергия"]<= user["characteristics"]["Максимальная Энергия"] - 5:
        user["parameters"]["Энергия"] += 5
    elif user["parameters"]["Энергия"] < user["characteristics"]["Максимальная Энергия"]:
        user["parameters"]["Энергия"] = user["characteristics"]["Максимальная Энергия"]
    user["position"][1] += 1
    with open(f"Data/{user_id}.json","w",encoding='utf-8') as user_file:
        json.dump(user,user_file,ensure_ascii=False)
    bot.edit_message_reply_markup(call.message.chat.id,call.message.id)
    bot.send_message(call.message.chat.id,"Вы пошли вниз")
    map_update(user_id,call.message.chat.id)
    monsters_move(user_id,call.message.chat.id)
    on_exit(user,user_id,call.message.chat.id)
    
@bot.callback_query_handler(func = lambda call: "trade" in call.data)
def trade(call):
    bot.edit_message_reply_markup(call.message.chat.id,call.message.id)
    user_id = call.data.replace("trade ",'')
    with open(f"Data/{user_id}.json","r",encoding='utf-8') as user_file:
        user = json.load(user_file)
    trader = user["map"][user["Trade_with"][1]][user["Trade_with"][0]]["object"]
    trade_list = trader["trade_list"]
    items_on_sell = telebot.types.InlineKeyboardMarkup()
    for item in trade_list:
        item_on_sell = telebot.types.InlineKeyboardButton(f"{item} - {round(Items[item]['price']*trader['price_factor'])}",callback_data=f"buy{item} {user_id}")
        items_on_sell.add(item_on_sell)
    bot.send_message(call.message.chat.id,f"Ваши монеты:{user['money']}\nВыберите предмет, который хотите купить:",reply_markup=items_on_sell)
    
@bot.callback_query_handler(func = lambda call: "buy" in call.data)
def buy(call):
    call_data = call.data
    
    user_id = ''
    while call_data[len(call_data)-1] != ' ':
        user_id = call_data[len(call_data)-1] + user_id
        call_data = call_data[:-1]
    call_data = call_data[3:-1]
    
    item = call_data
    
    with open(f"Data/{user_id}.json","r",encoding='utf-8') as user_file:
        user = json.load(user_file)
        
    if user["money"] >= round(Items[item]["price"]*user["map"][user["Trade_with"][1]][user["Trade_with"][0]]["object"]["price_factor"]):
        user["items"].append(item)
        user["money"] -= round(Items[item]["price"]*user["map"][user["Trade_with"][1]][user["Trade_with"][0]]["object"]["price_factor"])
        user["map"][user["Trade_with"][1]][user["Trade_with"][0]]["object"]["store_bank"] += round(Items[item]["price"]*user["map"][user["Trade_with"][1]][user["Trade_with"][0]]["object"]["price_factor"])
        bot.send_message(call.message.chat.id,f"Вы приобрели {item} за {round(Items[item]['price']*user['map'][user['Trade_with'][1]][user['Trade_with'][0]]['object']['price_factor'])} монет\nУ Вас осталось {user['money']} монет")
    else:
        bot.send_message(call.message.chat.id,"Недостаточно средств")
        
    bot.edit_message_reply_markup(call.message.chat.id,call.message.id)
    monsters_move(user_id,call.message.chat.id)
    
    with open(f"Data/{user_id}.json","w",encoding='utf-8') as user_file:
        json.dump(user,user_file,ensure_ascii=False)

@bot.message_handler(commands=['battle'])
def battle(message):
    with open(f"Data/{message.from_user.id}.json","r",encoding='utf-8') as user_file:
        user = json.load(user_file)
    if user["status"] == "Battle":
        battle_actions = telebot.types.InlineKeyboardMarkup()
        
        if user["parameters"]["Энергия"] >= Weapons[user["weapon"]]["Энергозатратность"]:
            battle_attack = telebot.types.InlineKeyboardButton("Атака",callback_data=f"attack {message.from_user.id}")
            battle_actions.add(battle_attack)
        battle_defend = telebot.types.InlineKeyboardButton("Защита",callback_data=f"defend {message.from_user.id}")
        battle_wait = telebot.types.InlineKeyboardButton("Ожидание",callback_data=f"wait {message.from_user.id}")
        if len(user["items"]) > 0:
            battle_items = telebot.types.InlineKeyboardButton("Предметы",callback_data=f"battle_items {message.from_user.id}")
            battle_actions.add(battle_items)
            
        battle_actions.add(battle_defend,battle_wait)
        bot.send_message(message.chat.id,f"БИТВА\nВраг: {user['monsters'][user['Battle_with']]['name']}\n\nВаше здоровье: {user['parameters']['Здоровье']}\nВаша энергия:{user['parameters']['Энергия']}\n\nЗдоровье врага:{user['monsters'][user['Battle_with']]['Здоровье']}\n\nВыберите действие:",reply_markup=battle_actions)
    elif user["status"] == "Trade" and user["map"][user["Trade_with"][1]][user["Trade_with"][0]]["object"]["store_bank"] > 0:
        user["money"] += user["map"][user["Trade_with"][1]][user["Trade_with"][0]]["object"]["store_bank"]
        user["map"][user["Trade_with"][1]][user["Trade_with"][0]]["object"]["store_bank"] = 0
        bot.send_message(message.chat.id,f"Торговец отдал вам все деньги, лишь бы Вы сохранили ему жизнь")
        user["status"] = "Free"
        user["map"][user["Trade_with"][1]][user["Trade_with"][0]].pop("object")
        user.pop("Trade_with")
        with open(f"Data/{message.from_user.id}.json","w",encoding="utf-8") as user_file:
            json.dump(user,user_file)
        map_update(message.from_user.id,message.chat.id)
    else:
        bot.send_message(message.chat.id,"Вы не находитесь в состоянии битвы")

@bot.callback_query_handler(func = lambda call: "attack" in call.data)
def battle_attack(call):
    user_id = call.data.replace("attack ",'')
    with open(f"Data/{user_id}.json","r",encoding='utf-8') as user_file:
        user = json.load(user_file)
    user["parameters"]["Энергия"] -= Weapons[user["weapon"]]["Энергозатратность"]
    damage = random.randint(Weapons[user["weapon"]]["Диапазон Урона"][0],Weapons[user["weapon"]]["Диапазон Урона"][1])
    user["monsters"][user["Battle_with"]]["Здоровье"] -= damage
    bot.send_message(call.message.chat.id,f"Вы атакуете и наносите {damage} ед. урона")
    if user["monsters"][user["Battle_with"]]["Здоровье"] <= 0:
        bot.send_message(call.message.chat.id,f"Вы одержали победу над {user['monsters'][user['Battle_with']]['name']}")
        user["monsters"].pop(user["Battle_with"])
        user.pop("Battle_with")
        user["status"] = "Free"
        with open(f"Data/{user_id}.json","w",encoding="utf-8") as user_file:
            json.dump(user,user_file)
        bot.send_message(call.message.chat.id,f"У Вас осталось:\n{user['parameters']['Здоровье']} ед. здоровья\n{user['parameters']['Энергия']} ед. энергии")
        map_update(user_id,call.message.chat.id)
    else:
        monster_battle_move(user,user_id,call.message.chat.id,False)
    bot.edit_message_reply_markup(call.message.chat.id,call.message.id)
    
@bot.callback_query_handler(func = lambda call: "defend" in call.data)
def battle_defend(call):
    user_id = call.data.replace("defend ",'')
    if user["parameters"]["Энергия"]<= user["characteristics"]["Максимальная Энергия"] - 10:
        user["parameters"]["Энергия"] += 10
    elif user["parameters"]["Энергия"] < user["characteristics"]["Максимальная Энергия"]:
        user["parameters"]["Энергия"] = user["characteristics"]["Максимальная Энергия"]
    with open(f"Data/{user_id}.json","r",encoding='utf-8') as user_file:
        user = json.load(user_file)
    bot.send_message(call.messsage.chat.id,f"Вы защищаетесь")
    monster_battle_move(user,user_id,call.message.chat.id,True)
    bot.edit_message_reply_markup(call.message.chat.id,call.message.id)
    
@bot.callback_query_handler(func = lambda call: "wait" in call.data)
def battle_wait(call):
    user_id = call.data.replace("wait ",'')
    with open(f"Data/{user_id}.json","r",encoding='utf-8') as user_file:
        user = json.load(user_file)
    if user["parameters"]["Энергия"]<= user["characteristics"]["Максимальная Энергия"] - 20:
        user["parameters"]["Энергия"] += 20
    elif user["parameters"]["Энергия"] < user["characteristics"]["Максимальная Энергия"]:
        user["parameters"]["Энергия"] = user["characteristics"]["Максимальная Энергия"]
    monster_battle_move(user,user_id,call.message.chat.id,False)
    bot.edit_message_reply_markup(call.message.chat.id,call.message.id)
    
@bot.callback_query_handler(func = lambda call: "battle_items" in call.data)
def battle_items(call):
    user_id = call.data.replace("battle_items ",'')
    with open(f"Data/{user_id}.json","r",encoding='utf-8') as user_file:
        user = json.load(user_file)
    
    item_list = telebot.types.InlineKeyboardMarkup()
    item_true = False
    
    for item in user["items"]:
        if Items[item]["type"] == "potion":
            item_true = True
            potion = telebot.types.InlineKeyboardButton(f"{item}",callback_data=f"use_battle{item} {user_id}")
            item_list.add(potion)
    
    if item_true:
        bot.send_message(call.message.chat.id,f"Вы можете использовать эти предметы:",reply_markup=item_list)
    bot.edit_message_reply_markup(call.message.chat.id,call.message.id)
    
@bot.callback_query_handler(func = lambda call: "use_battle" in call.data)
def use_item_battle(call):
    call_data = call.data
    
    user_id = ''
    while call_data[len(call_data)-1] != ' ':
        user_id = call_data[len(call_data)-1] + user_id
        call_data = call_data[:-1]
    call_data = call_data[10:-1]
    
    item = call_data
    
    with open(f"Data/{user_id}.json","r",encoding='utf-8') as user_file:
        user = json.load(user_file)
    
    user["items"].remove(item)
    if user["parameters"][Items[item]["potion_effect_on"]] + Items[item]["potion_effectiveness"] <= user["characteristics"][characteristics_control[Items[item]["potion_effect_on"]]]:
        user["parameters"][Items[item]["potion_effect_on"]] += Items[item]["potion_effectiveness"]
        bot.send_message(call.message.chat.id,f"Вы использовали {item}, параметр {Items[item]['potion_effect_on']} был увеличен на {Items[item]['potion_effectiveness']} единиц")
    else:
        user["parameters"][Items[item]["potion_effect_on"]] = user["characteristics"][characteristics_control[Items[item]["potion_effect_on"]]]
        bot.send_message(call.message.chat.id,f"Вы использовали {item}, параметр {Items[item]['potion_effect_on']} был увеличен на {user['characteristics'][characteristics_control[Items[item]['potion_effect_on']]]-user['parameters'][Items[item]['potion_effect_on']]} единиц")
    
    with open(f"Data/{user_id}.json","w",encoding='utf-8') as user_file:
        json.dump(user, user_file)
    
    bot.edit_message_reply_markup(call.message.chat.id,call.message.id)
    monster_battle_move(user,user_id,call.message.chat.id,True)
    

def monsters_move(user_id,chat_id):
    with open(f"Data/{user_id}.json","r",encoding='utf-8') as user_file:
        user = json.load(user_file)
        
    busy_fields = []
    for monster in range(0,len(user["monsters"])):
        busy_fields.append((user["monsters"][monster]["position"][0], user["monsters"][monster]["position"][1]))
        
    for monster in range(0,len(user["monsters"])):
        if (not("Battle_with" in user)) or ("Battle_with" in user and monster != user["Battle_with"]):
            can_move = ["no_move"]
            if (user["monsters"][monster]["position"][0] > 0) and (("object" in user["map"][user["monsters"][monster]["position"][1]][user["monsters"][monster]["position"][0]-1] and user["map"][user["monsters"][monster]["position"][1]][user["monsters"][monster]["position"][0]-1]["object"]["name"] in user["monsters"][monster]["can_walk"]) or (not ("object" in user["map"][user["monsters"][monster]["position"][1]][user["monsters"][monster]["position"][0]-1]) and "Комната" in user["monsters"][monster]["can_walk"]) or ("Все" in user["monsters"][monster]["can_walk"])) and (not ((user["monsters"][monster]["position"][0]-1, user["monsters"][monster]["position"][1]) in busy_fields)):
                can_move.append("left")
            if (user["monsters"][monster]["position"][1] > 0) and (("object" in user["map"][user["monsters"][monster]["position"][1]-1][user["monsters"][monster]["position"][0]] and user["map"][user["monsters"][monster]["position"][1]-1][user["monsters"][monster]["position"][0]]["object"]["name"] in user["monsters"][monster]["can_walk"]) or (not ("object" in user["map"][user["monsters"][monster]["position"][1]-1][user["monsters"][monster]["position"][0]]) and "Комната" in user["monsters"][monster]["can_walk"]) or ("Все" in user["monsters"][monster]["can_walk"])) and (not ((user["monsters"][monster]["position"][0], user["monsters"][monster]["position"][1]-1) in busy_fields)):
                can_move.append("up")
            if (user["monsters"][monster]["position"][0] < MAP_SIZE-1) and (("object" in user["map"][user["monsters"][monster]["position"][1]][user["monsters"][monster]["position"][0]+1] and user["map"][user["monsters"][monster]["position"][1]][user["monsters"][monster]["position"][0]+1]["object"]["name"] in user["monsters"][monster]["can_walk"]) or (not ("object" in user["map"][user["monsters"][monster]["position"][1]][user["monsters"][monster]["position"][0]+1]) and "Комната" in user["monsters"][monster]["can_walk"]) or ("Все" in user["monsters"][monster]["can_walk"])) and (not ((user["monsters"][monster]["position"][0]+1, user["monsters"][monster]["position"][1]) in busy_fields)):
                can_move.append("right")
            if (user["monsters"][monster]["position"][1] < MAP_SIZE-1) and (("object" in user["map"][user["monsters"][monster]["position"][1]+1][user["monsters"][monster]["position"][0]] and user["map"][user["monsters"][monster]["position"][1]+1][user["monsters"][monster]["position"][0]]["object"]["name"] in user["monsters"][monster]["can_walk"]) or (not ("object" in user["map"][user["monsters"][monster]["position"][1]+1][user["monsters"][monster]["position"][0]]) and "Комната" in user["monsters"][monster]["can_walk"]) or ("Все" in user["monsters"][monster]["can_walk"])) and (not ((user["monsters"][monster]["position"][0], user["monsters"][monster]["position"][1]+1) in busy_fields)):
                can_move.append("down")
            
            action = random.choice(can_move)
            
            if action == "left":
                user["monsters"][monster]["position"][0] -= 1
            elif action == "up":
                user["monsters"][monster]["position"][1] -= 1
            elif action == "right":
                user["monsters"][monster]["position"][0] += 1
            elif action == "down":
                user["monsters"][monster]["position"][1] += 1
            
        busy_fields[monster] = (user["monsters"][monster]["position"][0], user["monsters"][monster]["position"][1])
        
    
    with open(f"Data/{user_id}.json","w",encoding='utf-8') as user_file:
        json.dump(user, user_file)
    
    map_update(user_id,chat_id)
    
def monster_battle_move(user_data,user_id,chat_id,defend_or_not = False):
    possible_moves = ["nothing","attack","defend"]
    battle_moves = {
        "nothing":"nothing",
        "attack": random.randint(user_data["monsters"][user_data["Battle_with"]]["Диапазон Урона"][0],user_data["monsters"][user_data["Battle_with"]]["Диапазон Урона"][1]),
        "defend": user_data["monsters"][user_data["Battle_with"]]["Защита"]
    }
    chose_move = random.choice(possible_moves)
    if chose_move == "nothing":
        bot.send_message(chat_id,f"{user_data['monsters'][user_data['Battle_with']]['name']} ждёт")
    elif chose_move == "attack":
        bot.send_message(chat_id,f"{user_data['monsters'][user_data['Battle_with']]['name']} атакует")
        damage = battle_moves["attack"]
        if defend_or_not:
            damage = round(damage-damage/100*user_data["parameters"]["Защита"])
            user_data["parameters"]["Здоровье"] -= damage
        else:
            user_data["parameters"]["Здоровье"] -= damage
        bot.send_message(chat_id,f"{user_data['monsters'][user_data['Battle_with']]['name']} наносит вам {damage} ед. урона")
        if user_data["parameters"]["Здоровье"] <= 0:
            bot.send_message(chat_id,f"ВЫ ПОГИБЛИ\nВведите /start для перезапуска")
            os.remove(f"Data/{user_id}.json")
            os.remove(f"Data/{user_id}.png")
    elif chose_move == "defend":
        bot.send_message(chat_id,f"{user_data['monsters'][user_data['Battle_with']]['name']} защищается")
        defend = round(random.randint(Weapons[user_data["weapon"]]["Диапазон Урона"][0],Weapons[user_data["weapon"]]["Диапазон Урона"][1])/100*battle_moves["defend"])
        user_data["monsters"][user_data["Battle_with"]]["Здоровье"] += defend
        bot.send_message(chat_id,f"{user_data['monsters'][user_data['Battle_with']]['name']} отразил {defend} ед. урона")
    
    bot.send_message(chat_id,f"Ваше здоровье:{user_data['parameters']['Здоровье']}\nВаша энергия:{user_data['parameters']['Энергия']}\n\nЗдоровье врага: {user_data['monsters'][user_data['Battle_with']]['Здоровье']}")
    
    with open(f"Data/{user_id}.json","w",encoding='utf-8') as user_file:
        json.dump(user_data,user_file,ensure_ascii=False)
        
def on_exit(user_data,user_id,chat_id):
    if "object" in user_data["map"][user_data["position"][1]][user_data["position"][0]] and user_data["map"][user_data["position"][1]][user_data["position"][0]]["object"]["name"] == "Выход":
        exit_move = telebot.types.InlineKeyboardMarkup()
        exit_button = telebot.types.InlineKeyboardButton("Выход",callback_data=f"exit {user_id}")
        exit_move.add(exit_button)
        bot.send_message(chat_id,f"Вы достигли выхода, желаете выйти из этого злосчастного места?",reply_markup=exit_move)
        
@bot.callback_query_handler(func = lambda call: "exit" in call.data)
def exit_win(call):
    user_id = call.data.replace("exit ","")
    bot.send_message(call.message.chat.id,f"Поздравляю, Вы прошли игру!\nЧтобы начать новую игру введите /start")
    os.remove(f"Data/{user_id}.json")
    os.remove(f"Data/{user_id}.png")
    bot.edit_message_reply_markup(call.message.chat.id,call.message.id)
    
@bot.message_handler(commands=['items'])
def show_items(message):
    
    with open(f"Data/{message.from_user.id}.json","r",encoding='utf-8') as user_file:
        user = json.load(user_file)
    if len(user["items"]) > 0:
        item_list = telebot.types.InlineKeyboardMarkup()
        
        for item in user["items"]:
            new_item = telebot.types.InlineKeyboardButton(f"{item}",callback_data=f"use_item {item} {message.from_user.id}")
            item_list.add(new_item)
        bot.send_message(message.chat.id,f"Оружие: {user['weapon']}\nМонеты: {user['money']}\nНажмите на предмет для использования:",reply_markup=item_list)
    else:
        bot.send_message(message.chat.id,f"Оружие: {user['weapon']}\nМонеты: {user['money']}")
        
@bot.callback_query_handler(func = lambda call: "use_item" in call.data)
def use_item(call):
    call_data = call.data
    
    user_id = ''
    while call_data[len(call_data)-1] != ' ':
        user_id = call_data[len(call_data)-1] + user_id
        call_data = call_data[:-1]
    call_data = call_data[9:-1]
    
    item = call_data
    
    with open(f"Data/{user_id}.json","r",encoding='utf-8') as user_file:
        user = json.load(user_file)
        
    if Items[item]["type"] == "potion":
        user["items"].remove(item)
        if user["parameters"][Items[item]["potion_effect_on"]] + Items[item]["potion_effectiveness"] <= user["characteristics"][characteristics_control[Items[item]["potion_effect_on"]]]:
            user["parameters"][Items[item]["potion_effect_on"]] += Items[item]["potion_effectiveness"]
            bot.send_message(call.message.chat.id,f"Вы использовали {item}, параметр {Items[item]['potion_effect_on']} был увеличен на {Items[item]['potion_effectiveness']} единиц")
        else:
            user["parameters"][Items[item]["potion_effect_on"]] = user["characteristics"][characteristics_control[Items[item]["potion_effect_on"]]]
            bot.send_message(call.message.chat.id,f"Вы использовали {item}, параметр {Items[item]['potion_effect_on']} был увеличен на {user['characteristics'][characteristics_control[Items[item]['potion_effect_on']]]-user['parameters'][Items[item]['potion_effect_on']]} единиц")
    
    if Items[item]["type"] == "scroll":
        user["items"].remove(item)
        user[Items[item]["scroll_effect"]][Items[item]["scroll_effect_on"]] += Items[item]["scroll_effectiveness"]
        bot.send_message(call.message.chat.id,f"Вы использовали {item}, повысив свой параметр {Items[item]['scroll_effect_on']} на {Items[item]['scroll_effectiveness']} единиц")
    
    if Items[item]["type"] == "weapon":
        user["items"].append(user["weapon"])
        user["items"].remove(item)
        user["weapon"] = item
        bot.send_message(call.message.chat.id,f"Вы взяли в руки {user['weapon']}")
    
    with open(f"Data/{user_id}.json","w",encoding='utf-8') as user_file:
        json.dump(user, user_file)
        
    monsters_move(user_id,call.message.chat.id)
    bot.edit_message_reply_markup(call.message.chat.id,call.message.id)


@bot.message_handler(commands=['sell'])
def sell(message):
    with open(f"Data/{message.from_user.id}.json","r",encoding='utf-8') as user_file:
        user = json.load(user_file)
    if user["status"] == "Trade":
        trader = user["map"][user["Trade_with"][1]][user["Trade_with"][0]]["object"]
        if trader["can_buy"]:
            if len(user["items"]) > 0:
                item_list = telebot.types.InlineKeyboardMarkup()
            
                for item in user["items"]:
                    new_item = telebot.types.InlineKeyboardButton(f"Продать {item} за {round(Items[item]['price']/2/trader['price_factor'])} монет",callback_data=f"sell_item {item} {message.from_user.id}")
                    item_list.add(new_item)
            else:
                bot.send_message(message.chat.id,f"У Вас нечего продавать")
            
            bot.send_message(message.chat.id,f"Торговец готов купить Ваши вещи, предложите что-нибудь на продажу:",reply_markup=item_list)
        else:
            bot.send_message(message.chat.id,f"Торговец не хочет ничего покупать")
    else:
        bot.send_message(message.chat.id,f"Вы сейчас не торгуете")
        
@bot.callback_query_handler(func = lambda call: "sell_item" in call.data)
def sell_item(call):
    call_data = call.data
    
    user_id = ''
    while call_data[len(call_data)-1] != ' ':
        user_id = call_data[len(call_data)-1] + user_id
        call_data = call_data[:-1]
    call_data = call_data[10:-1]
    
    item = call_data
    
    with open(f"Data/{user_id}.json","r",encoding='utf-8') as user_file:
        user = json.load(user_file)
        
    trader = user["map"][user["Trade_with"][1]][user["Trade_with"][0]]["object"]
    if trader["store_bank"] >= round(Items[item]["price"]/2/trader["price_factor"]):
        user["items"].remove(item)
        user["money"] += round(Items[item]["price"]/2/trader["price_factor"])
        trader["store_bank"] -= round(Items[item]["price"]/2/trader["price_factor"])
        bot.edit_message_reply_markup(call.message.chat.id,call.message.id)
        with open(f"Data/{user_id}.json","w",encoding='utf-8') as user_file:
            json.dump(user,user_file,ensure_ascii=False)
        monsters_move(user_id,call.message.chat.id)
    else:
        bot.send_message(call.message.chat.id,f"У торговца не хватает денег, чтобы приобрести Ваш предмет")
        

@bot.message_handler(commands=['take'])
def take_bag(message):
    with open(f"Data/{message.from_user.id}.json","r",encoding='utf-8') as user_file:
        user = json.load(user_file)
    
    if "object" in user["map"][user["position"][1]][user["position"][0]] and user["map"][user["position"][1]][user["position"][0]]["object"]["name"] == "Мешок":
        user["map"][user["position"][1]][user["position"][0]].pop("object")
        money_in_bag = random.randint(10,30)
        user["money"] += money_in_bag
        bot.send_message(message.chat.id,f"Вы подобрали {money_in_bag} монет")
        monsters_move(message.from_user.id,message.chat.id)
        with open(f"Data/{message.from_user.id}.json","w",encoding='utf-8') as user_file:
            json.dump(user,user_file,ensure_ascii=False)
    else:
        bot.send_message(message.chat.id,f"Нечего брать")


@bot.message_handler(commands=['hero'])
def hero(message):
    with open(f"Data/{message.from_user.id}.json","r",encoding='utf-8') as user_file:
        user = json.load(user_file)
    
    item_list = ''

    if len(user["items"]) > 0:
        for item in user["items"]:
            if user["items"].index(item) != len(user["items"])-1:
                item_list = item_list + item + ', '
            else:
                item_list = item_list + item
                
    if item_list == '':
        item_list = "Ваш Инвентарь Пуст"
    
    bot.send_message(message.chat.id,f"ВАШ ГЕРОЙ\nВаш Класс: {user['class']}\n\nЗдоровье: {user['parameters']['Здоровье']} / {user['characteristics']['Максимальное Здоровье']}\nЭнергия: {user['parameters']['Энергия']} / {user['characteristics']['Максимальная Энергия']}\n\nВаша Защита: {user['parameters']['Защита']}\n\nВаше Оружие: {user['weapon']}\nВаши Предметы: {item_list}")

@bot.message_handler(commands=['help'])
def help(message):
    bot.send_message(message.chat.id,COMMAND_LIST)

@bot.message_handler(commands=['command_list'])
def command_list(message):
    bot.send_message(message.chat.id,COMMAND_LIST)

@bot.message_handler(commands=['delete_pers'])
def deluser(message):
    if os.path.exists(f"Data/{message.from_user.id}.json"):
        os.remove(f"Data/{message.from_user.id}.json")
        os.remove(f"Data/{message.from_user.id}.png")
        bot.send_message(message.chat.id,f"Персонаж удалён")
    else:    
        bot.send_message(message.chat.id,f"Персонажа не существует")
           
if __name__ == "__main__":
    bot.infinity_polling()