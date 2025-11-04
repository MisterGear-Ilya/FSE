text = str(input("Выведите строку "))

i = 0

s = ''
cnt = 0
while i < len(text):
    s += text[i]
    if (text[i] == '.' or text[i] == '?' or text[i] == '!'):
        print(s)
        s = ''
        cnt += 1
        i = i + 1


    i = i + 1


print("Предложений в тексте: ",cnt,sep = ' ')