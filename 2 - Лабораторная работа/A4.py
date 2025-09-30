a = int(input())
b = int(input())

result = [a, b][a <= b] # Проверка , если a <= b - то это выражение true значит, что b - это максимум и он записывается в переменную result , если нет то записывается a.
print (result)
