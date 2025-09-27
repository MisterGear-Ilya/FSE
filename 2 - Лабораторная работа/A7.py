#A7 
x1 = int(input())
y1 = int(input())
x2 = int(input())
y2 = int(input())

result = ['NO','YES'][(x1 + y1) % 2 == (x2 + y2) % 2]

ans = ('YES')
if result == ans:
    print(result)
    color = ['White','Black'] [(x1 + y1) % 2 == 1]
    print(color)
else:
    print(result)
