square = lambda x: x*x # Название функции = lambda аргуент1,аргумент2...: действие с аргументами(как return)
print(square(7))

result = lambda x, y:  x+y
print(result(2,3))

print(list(map(lambda x: x*x, [1,2,3,4,5]))) # map(функция-обработчик,данные)

a,b,c,d,e,f = map(lambda a: a*5, [1,2,3,4,5,6])
print(a,b,c,d,e,f)