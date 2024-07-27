########################### Словари #####################
users = { # object = {id1 : {'name': name, 'age': int(age)}, id2: {...} ...}
    1: {'name': 'Ivan', 'age': 32},
    2: {'name': 'Milana', 'age': 17},
    
}
users[3] = {'name': 'Руслан', 'age': 16} #Добавим элемент с key = 3, value = {...}
users.pop(1)
print(users)
########################################################

########################### Списки ##################################

pets = ['Murka','Murzic', 'Chernysh']

#Вывод
print(*pets)

#Добавление
pets.append('Alisa')
pets.insert(2,'Bars')
print(*pets)

#Удаление
pets.pop(2)
pets.remove('Chernysh')
print(*pets)