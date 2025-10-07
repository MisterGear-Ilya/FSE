from math import *


def wrap(val, size):
    return ((val - 1) % size) + 1


def solve(filename: str):

    outname = filename.replace("ChaseData","PursuitLog")
    with open(filename, "r", encoding="utf-8") as f:
        lines = f.readline().split()
        n = int(lines[0])
        m = int(lines[1])
        a = []
        for line in f:
            line = line.split()
            if line != "":
                a.append(line)

    print("Cat and Mouse", end='\n\n')

    print("  Cat        Mouse    Distance", end='\n')
    print("------------------------------\n")
    cat = ['?','?']
    mouse = ['?','?']
    dist_cat = 0
    dist_mouse = 0
    caught = False

    for i in range(len(a)):
         p = a[i]
        # print(len(p))
         c = a[i][0]
         if c != 'P':
             x = int(a[i][1])
             y = int(a[i][2])

         if c == "M":
            if mouse[0] == '?':
                mouse = [wrap(x,n), wrap(y,m)]
            else:
                # суммарное расстояние по ходу: |dx| + |dy|
                dist_mouse += abs(x) + abs(y)
                mouse = [wrap(mouse[0] + x, n), wrap(mouse[1] + y, m)]

         elif c == "C":
             if cat[0] == '?':
                 cat = [wrap(x,n), wrap(y,m)]
             else:
                 dist_cat += abs(x) + abs(y)
                 cat = [wrap(cat[0] + x, n), wrap(cat[1] + y, m)]

         if c == 'P':
             if cat[0] == '?' or mouse[0] == '?':
                 cat_str = "( ?, ?)" if cat[0] == '?' else f"({cat[0]:2d}, {cat[1]:2d})"
                 mouse_str = "( ?, ?)" if mouse[0] == '?' else f"({mouse[0]:2d}, {mouse[1]:2d})"
                 print(f"{cat_str}     {mouse_str}")
             else:
                 dist = abs(cat[0]-mouse[0]) + abs(cat[1]-mouse[1])
                 if dist == 0:
                     caught = True
                     break
                 print(f"({cat[0]:2d}, {cat[1]:2d})     ({mouse[0]:2d}, {mouse[1]:2d})      {dist:2d}")


    print("------------------------------\n")
    print("Distance   Mouse    Cat")
    print(f"              {dist_mouse:2d}     {dist_cat:2d}\n")
    if caught:
        print("Mouse caught at: ",sep='',end='')
        print(f"({cat[0]:2d}, {cat[1]:2d})")

    else:
        print("Mouse evaded Cat.")


if __name__ == "__main__":
    files = ["1.ChaseData.txt","2.ChaseData.txt","3.ChaseData.txt","4.ChaseData.txt","5.ChaseData.txt"]
    for file in files:
        solve(file)
        print('\n')
