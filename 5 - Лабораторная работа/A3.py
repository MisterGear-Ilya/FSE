text = str(input("Выведите строку "))

world = text.split()

for w in world:
    if len(w) >= 3:
        print(w[0].upper(),end = '')


