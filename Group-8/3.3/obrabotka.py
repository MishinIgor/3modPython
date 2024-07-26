file = open('test.txt', 'w',encoding='utf-8')
file.write('Hello, my group 8\n')
file.write('Привет, моя любимая группа №8')
file.close

while True:
    file = open('text.txt','a',encoding='utf-8')
    file.write(input('Введите информацию в файл: ')+'\n')
    file.close
    vibor = input('Введите - чтобы закончить, или что угодно другое для продолжения-> ')
    if vibor == '-':
        break