import copy
users = {
    1: {'name': 'Ivan', 
        'age': 32,
        'pets': [{'type': 'dog', 'name': 'Charly'},
                 {'type': 'cat', 'name': 'Murzic'},
                 {'type': 'fish', 'name': 'GoldBurzhui'}]},
    2: {'name': 'Milana',
        'age': 17,
        'pets': [{'type': 'hamster', 'name':'Homa'},
                 {'type': 'cat', 'name': 'Murka'}]},
    3: {'name': 'Vladislav',
        'age': 25,
        'pets': [{'type': 'cat', 'name':'Archibald'},
                 {'type': 'hamster', 'name': 'virtualpet'}]}
}
#Цикл который выводит имена людей
# for i in users.values():
#     print(i['name'])

#Цикл который выводит имена людей и их питомцев. "У NAME есть питомцы PNAME1,PNAME2..."
# for i in users.values():
#     print(f'У {i['name']} есть питомцы ', end='')
#     for j in i['pets']:
#         print(f'{j['name']}',end=' ')
#     print()
users1 = copy.deepcopy(users)
users1[1] = {'name': 'Nikolay','age':34}
print(id(users), users)
print(id(users1),users1)

#НО
users1[2]['age']=38
print(id(users[2]['age']),users)
print(id(users1[2]['age']),users1)