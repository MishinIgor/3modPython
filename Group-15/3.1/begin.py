def my_decorator(func):
    def wrapper(a,b):
        c = 'Привет господин! Мы для вас сделали вычисления господин!'
        d = 'Надеюсь всё правильно господин, и вы довольны!'
        print(c)
        func(a,b)
        print(d)
    return wrapper

@my_decorator
def summa(a,b):
    print(f'{a} + {b} = {a+b}')
def multi(a,b):
    print(f'{a} * {b} = {a*b}')
    
summa(7,12)
multi(12,18)