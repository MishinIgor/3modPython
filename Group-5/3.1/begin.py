def my_decorator(func):
    def wrapper(a,b):
        print('Привет хозяин! Я тебя очень ждал!')
        func(a,b)
        print('Доброго дня Вам хозяин, буду ждать Вас снова!')
    return wrapper
@my_decorator
def summa(a,b):
    print(f'{a}+{b}={a+b}')

@my_decorator
def multi(a,b):
    print(f'{a}*{b}={a*b}')

summa(5,13)
multi(12,15)