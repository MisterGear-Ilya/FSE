py v  = int(input())
#A6
a = v // 3600
b = (v % 3600) // 60
c = v % 60

print('{}:{:02}:{:02}'.format(a,b,c))
