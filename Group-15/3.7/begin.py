#Словари
# users = {
#     1: {'name': 'Gleb', 'age':32},
#     2: {'name': 'Sabina', 'age':17},
#     3: {'name': 'Eugeniya', 'age': 23}
# }
# print(users[2]['name']) #Sabina
# print(users[3]['age']) #23
# users['Новый'] = {'name': 'NewGleb', 'age': 'NotStar'}
# print(users)
# users.pop('Новый')
# print(users)

##########################################
#Списки
pets = ['Murka','Murzik','Chernysh']
print(*pets)

#Добавление
pets.insert(10,'Хлеб') #list.insert(index,object)
pets.insert(9,'Батон')
pets.insert(-3,'Бургер')
pets.insert(2,'Ход-дог')
pets.append('Круасан')
print(*pets)