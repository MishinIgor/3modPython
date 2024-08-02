from PIL import Image, ImageDraw, ImageEnhance
import json,os,random
from TimBot import Items

SIZE = 1

Objects = [
    {
        "name":"Торговец",
        "chance":2.0,
        "passability":True
    },
    {
        "name":"Дыра",
        "chance":15.0,
        "passability":False
    },
    {
        "name":"Затопление",
        "chance":10.0,
        "passability":False
    },
    {
        "name":"Мешок",
        "chance":10.0,
        "passability":True
    }
]
Monsters = [
    {
        "name":"Амфибия",
        "spawnrate":20.0,
        "bioms": ["Затопление"],
        "can_walk":["Затопление","Комната"],
        
        "Здоровье":20,
        "Диапазон Урона":(1,2),
        "Защита":8
    },
    {
        "name":"Волк",
        "spawnrate":4.0,
        "bioms": ["Комната"],
        "can_walk":["Комната"],
        
        "Здоровье":20,
        "Диапазон Урона":(2,2),
        "Защита":6
    },
    {
        "name":"Гоблин",
        "spawnrate":6.0,
        "bioms": ["Комната"],
        "can_walk":["Комната"],
        
        "Здоровье":15,
        "Диапазон Урона":(1,2),
        "Защита":2
    },
    {
        "name":"Медведь",
        "spawnrate":2.5,
        "bioms": ["Комната"],
        "can_walk":["Комната"],
        
        "Здоровье":40,
        "Диапазон Урона":(2,6),
        "Защита":12
    },
    {
        "name":"Летучая Мышь",
        "spawnrate":35.5,
        "bioms":["Дыра"],
        "can_walk":["Все"],
        
        "Здоровье":12,
        "Диапазон Урона":(2,4),
        "Защита":60
    },
    {
        "name":"Скелет",
        "spawnrate":5.0,
        "bioms":["Комната"],
        "can_walk":["Комната"],
        
        "Здоровье":25,
        "Диапазон Урона":(3,5),
        "Защита":0
    },
    {
        "name":"Циклоп",
        "spawnrate":2.0,
        "bioms":["Комната"],
        "can_walk":["Комната"],
        
        "Здоровье":60,
        "Диапазон Урона":(2,3),
        "Защита":20
    },
]
monsters = []


def generate(row_count,column_count,user_pos):
    exit_coord = (random.randint(0,1)*(row_count-1),random.randint(0,1)*(column_count-1))
    map = []
    Background = Image.new("RGBA",(row_count*60*SIZE,column_count*60*SIZE),(0,0,0,255))
    for row in range(row_count):
        map.append([])
        for column in range(column_count):
            map[row].append([])
            map[row][column] = {}
            
            map[row][column]["X"] = column
            map[row][column]["Y"] = row
            
            if row == exit_coord[1] and column == exit_coord[0]:
                map[row][column]["object"] = {}
                map[row][column]["object"]["name"] = "Выход"
                map[row][column]["object"]["passability"] = True
            for object in range(len(Objects)):
                if not "object" in map[row][column] and not(row == user_pos[1] and column != user_pos[1]):
                    if random.randint(0,10000)/100 <= Objects[object]["chance"]:
                        map[row][column]["object"] = {}
                        map[row][column]["object"]["name"] = Objects[object]["name"]
                        map[row][column]["object"]["passability"] = Objects[object]["passability"]
                        
                        if map[row][column]["object"]["name"] == "Торговец":
                            can_trade_list = Items.copy()
                            trade_list = []
                            for suggestion in range(0,3):
                                avaible_trade_items = list(can_trade_list)
                                add_trade_item = random.choice(avaible_trade_items)
                                trade_list.append(add_trade_item)
                                can_trade_list.pop(avaible_trade_items[avaible_trade_items.index(add_trade_item)])
                            map[row][column]["object"]["trade_list"] = trade_list
                            map[row][column]["object"]["price_factor"] = random.randint(50,150)/100
                            map[row][column]["object"]["can_buy"] = random.choice([True,False])
                            map[row][column]["object"]["store_bank"] = 100
                        
                        break
                else:
                    break
            
            if not(row == user_pos[1] and column != user_pos[1]):
                for mob in range(len(Monsters)):
                    if ("object" in map[row][column] and map[row][column]["object"]["name"] in Monsters[mob]["bioms"]) or (not ("object" in map[row][column]) and ("Комната" in Monsters[mob]["bioms"])) or ("Все" in Monsters[mob]["bioms"]):
                        if random.randint(0,10000)/100 <= Monsters[mob]["spawnrate"]:
                            new_monster = {
                                "name":"",
                                "can_walk":[]
                            }
                            new_monster["name"] = Monsters[mob]["name"]
                            new_monster["position"] = [column,row]
                            new_monster["can_walk"] = Monsters[mob]["can_walk"]
                            
                            new_monster["Здоровье"] = Monsters[mob]["Здоровье"]
                            new_monster["Диапазон Урона"] = Monsters[mob]["Диапазон Урона"]
                            new_monster["Защита"] = Monsters[mob]["Защита"]
                            monsters.append(new_monster)
                            break
                    
    return map,Background,monsters



def Map_save(image,path):
    image.save(path)
    
def Map_open(path):
    return Image.open(path)



def render(user_id):
    if os.path.exists(f"Data/{user_id}.json"):
        
        with open(f"Data/{user_id}.json","r",encoding='utf-8') as user_file:
            User = json.load(user_file)
            
        map_img = Image.open(f"Data/{user_id}.png")
        map_list = User["map"]
        
        monster_with_user = False
        monster_with_user_id = ''
        
        vision = User["characteristics"]["Дальнозоркость"]
        
        for row in range(len(map_list)):
            for column in range(len(map_list[row])):
                
                Room = Image.open("UI/Room.png")
                Room = Room.resize((Room.width*SIZE,Room.height*SIZE)).convert("RGBA")
                if not (abs(map_list[row][column]["X"]-User["position"][0]) <= vision and abs(map_list[row][column]["Y"]-User["position"][1]) <= vision):
                    Room = ImageEnhance.Brightness(Room).enhance(0.45)
                map_img.paste(Room,(map_list[row][column]["X"]*60*SIZE,map_list[row][column]["Y"]*60*SIZE),mask = Room)  
                
                if abs(map_list[row][column]["X"]-User["position"][0]) <= vision and abs(map_list[row][column]["Y"]-User["position"][1]) <= vision:
                    
                    if "object" in map_list[row][column]:
                        Object = Image.open(f"UI/Объекты/{map_list[row][column]['object']['name']}.png")
                        Object = Object.resize((Object.width*SIZE,Object.height*SIZE)).convert("RGBA")
                        map_img.paste(Object,(map_list[row][column]["X"]*60*SIZE,map_list[row][column]["Y"]*60*SIZE),mask=Object)
                    
                    for monster in range(len(User["monsters"])):
                        if row == User["monsters"][monster]["position"][1] and User["monsters"][monster]["position"][0] == column:
                            Monster = Image.open(f"UI/Монстры/{User['monsters'][monster]['name']}.png")
                            Monster = Monster.resize((Monster.width*SIZE,Monster.height*SIZE)).convert("RGBA")
                            if User["monsters"][monster]["position"][1] == User["position"][1] and User["monsters"][monster]["position"][0] == User["position"][0]:
                                monster_with_user = True
                                monster_with_user_id = monster
                            else: 
                                map_img.paste(Monster,(User["monsters"][monster]["position"][0]*60*SIZE+10*SIZE,User["monsters"][monster]["position"][1]*60*SIZE+10*SIZE),mask=Monster)
                            
        Pers = Image.open(f"UI/Персонажи/{User['class']}.png")
        Pers = Pers.resize((Pers.width*SIZE,Pers.height*SIZE)).convert("RGBA")
        if not monster_with_user:
            map_img.paste(Pers,(User["position"][0]*60*SIZE+10*SIZE,User["position"][1]*60*SIZE+10*SIZE),mask=Pers)
            if "object" in map_list[User["position"][1]][User["position"][0]] and map_list[User["position"][1]][User["position"][0]]["object"]["name"] == "Торговец":
                User["status"] = "Trade"
                User["Trade_with"] = (User["position"])
            else:
                User["status"] = "Free"
                if "Trade_with" in User:
                    User.pop("Trade_with")
            with open(f"Data/{user_id}.json","w",encoding='utf-8') as user_file:
                json.dump(User,user_file,ensure_ascii=False)
        else:
            Battle = Image.open("UI/Battle.png")
            Battle = Battle.resize((Battle.width*SIZE,Battle.height*SIZE)).convert("RGBA")
            map_img.paste(Battle,(User["position"][0]*60*SIZE-2*SIZE,User["position"][1]*60*SIZE-2*SIZE),mask=Battle)
            
            map_img.paste(Pers,(User["position"][0]*60*SIZE+10*SIZE-20*SIZE,User["position"][1]*60*SIZE+10*SIZE),mask=Pers)
            
            Monster = Image.open(f"UI/Монстры/{User['monsters'][monster_with_user_id]['name']}.png")
            Monster = Monster.resize((Monster.width*SIZE,Monster.height*SIZE)).convert("RGBA")
            map_img.paste(Monster,(User["monsters"][monster_with_user_id]["position"][0]*60*SIZE+10*SIZE+20*SIZE,User["monsters"][monster_with_user_id]["position"][1]*60*SIZE+10*SIZE),mask=Monster)
            monster_with_user = False
            User["status"] = "Battle"
            User["Battle_with"] = monster_with_user_id
            monster_with_user_id = ''
            with open(f"Data/{user_id}.json","w",encoding='utf-8') as user_file:
                json.dump(User,user_file,ensure_ascii=False)
            
        Map_save(map_img,f"Data/{user_id}.png")
        