users = {
    1 : {'name' : 'Ivan', 'age' : 32},
    2 : {'name' : 'Milana', 'age' : 17}
}
print(users[1]['name'])
print(users[1]['age'])


# добавление
users[3] = {'name' : 'Mark', 'age' : 20}
print(users)


# удаление
users.pop(1)
print(users)

# Списки
pets = ['Murka', 'Murzic', 'Chernysh']


# Вывод
print(*pets)


# Добавление
pets.append('Alisa')
pets.insert(0, 'Bars')
print(*pets)


# Удаление
pets.pop(2)
pets.remove('Chernysh')
print(*pets)


# Обращение по индексу
print(pets[2])
