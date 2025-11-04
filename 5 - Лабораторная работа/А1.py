text = str(input("Выведите строку"))
while '(' in text and ')' in text:
    left = text.find('(')
    right = text.find(')',left)
    if right == -1:
        break
    s = text[left:right + 1]
    text = text.replace(s,'')

print(text)