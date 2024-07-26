def square(x):
    return x*x
print(square(17))
square2 = lambda x: x*x
print(square2(19))

result = lambda x,y,z: x+y*z
print(result(2,6,3))

numbers = list(map(lambda x: x*x,[1,2,3,4,5,6,7,8,9]))
print(numbers)