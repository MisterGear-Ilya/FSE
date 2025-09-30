x1 = int(input())
y1 = int(input())
x2 = int(input())
y2 = int(input())

result = ['NO','YES'][(x1 + y1) % 2 == (x2 + y2) % 2] # Проверка на клетки покрашены в один цвет

ans = ('YES')
if result == ans:
    print(result)
    color = ['White','Black'] [(x1 + y1) % 2 == 1] # Проверка , какой цвет у клетки
    print(color)
else:
    print(result)
