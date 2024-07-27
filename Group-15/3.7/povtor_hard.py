users = {
    1: {'name': 'Gleb',
        'age': 32,
        'pets': [{'type': 'dog', 'name': 'Charly'},
                 {'type': 'cat', 'name': 'Murzik'}]},
    2: {'name': 'Milana', 
        'age': 17,
        'pets': [{'type': 'hamster', 'name': 'Homa'},
                 {'type': 'cat', 'name': 'Murka'}]},
    3: {'name': 'Sabina',
        'age': 23,
        'pets': [{'type': 'beaver', 'name':'Pak'}]}
}

#Цикл для вывода имён людей
# for i in users.values():
#     print(i['name'])

#Цикл для вывода имён людей и имён их питомцев. Например: Глеб живёт с dog cat
for i in users.values():
    print(f'{i['name']} живёт с ', end='')
    for j in i['pets']:
        print(j['name'],end=' ')
    print()