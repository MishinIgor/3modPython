def my_decorator(func):
    def wrapper(a,b):
        print('Добрый день, пользователь!')
        func(a,b)
        print('Хорошего дня, пользователь!')
    return wrapper

@my_decorator
def summa(a,b):
    print(f'{a} + {b} = {a+b}')
    
@my_decorator   
def mult(a,b):
    print(f'{a} * {b} = {a*b}')

summa(9,12)
mult(3,7)
