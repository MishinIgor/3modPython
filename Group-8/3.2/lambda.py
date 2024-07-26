double = lambda x: x**2

def doub(x):
    return x**2

formula = lambda x,y,z: x+y*z
print(formula(5,7,12))

od, dv, tr, ch, pya, she, sem, vos, dev = map(lambda x: x*x,[1,2,3,4,5,6,7,8,9]) # map(обработчик, данные)
print(od, dv, tr, ch, pya, she, sem, vos, dev)

print(doub(5),double(5))