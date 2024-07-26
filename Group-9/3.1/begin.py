def my_decorator(trulyalya):
    def wrapper(a,b):
        print(f'Хозяин, мы нашли какие-то числа {a} и {b}. Мы сейчас их для вас посчитаем!')
        trulyalya(a,b)
        print(f'Хозяин, мы для вас посчитали, надеемся Вы довольный хозяина!')
    return wrapper
@my_decorator
def summa(a,b):
    print(f'{a}+{b}={a+b}')
@my_decorator
def multi(a,b):
    print(f'{a}*{b}={a*b}')

summa(15,12)
multi(15,12)