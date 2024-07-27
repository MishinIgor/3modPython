import copy
users = {
    1 : {'name' : 'Ivan', 'age' : 32},
    2 : {'name' : 'Milana', 'age' : 17}
}
#Глубокая копия
users1 = copy.deepcopy(users)
users1[2]['age'] = 38
print(id(users[2]['age']),users)
print(id(users1[2]['age']),users1)
print('------------------!!!!!!!!!!!!!-----------------------')
#Копирование
users1 = copy.copy(users)
users1[1] = {'name' : 'Vladislav', 'age' : 151}
print(id(users),users)
print(id(users1),users1)
print('------------------!!!!!!!!!!!!!-----------------------')
#НО!
users1[2]['age'] = 38
print(id(users[2]['age']),users)
print(id(users1[2]['age']),users1)
print('------------------!!!!!!!!!!!!!-----------------------')
#Поверхностная копия
users1 = users
users1[1] = {'name' : 'Nikolay', 'age' : 51}
print(id(users),users)
print(id(users1),users1)

