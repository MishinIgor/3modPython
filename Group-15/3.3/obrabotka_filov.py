# r: Открывает файл для чтения. (по умолчанию)
# w: Открывает файл для записи. Создает новый файл, если он не существует, или усекает файл, если он существует.
# x: Открывает файл для эксклюзивного создания. Если файл уже существует, операция завершается неудачей.
# a: Открывает файл для добавления в конце файла без его усечения. Создает новый файл, если он не существует.
try:
    f = open('test.txt','a',encoding='utf-8')
    f.write(input('Введите информацию для записи: ')+'\n')
except FileExistsError:
    f = open('test.txt','a',encoding='utf-8')
    f.write('На этом не всё заканчивается'+'\n')
