from math import *
def solve(filename: str, name: str = "Ilya Alferovich"):
    with open(filename, "r", encoding="utf-8") as f:
        # первая строка: количество локаций и масштаб
        first_line = f.readline().strip().split()
        n = int(first_line[0])
        scale = float(first_line[1])

        # остальные строки: расстояния в дюймах
        distances_inches = []
        for line in f:
            line = line.strip()
            if line != "":
                distances_inches.append(float(line))

    # переводим в мили
    distances_miles = []
    for d in distances_inches:
        distances_miles.append(ceil(d * scale * 10) / 10)

    # общая сумма
    total_distance = 0
    for d in distances_miles:
        total_distance += d

    # вывод
    print(name)
    print("Simple Map Distance Computations\n")
    print(f"Map Scale Factor:    {scale:.2f} miles per inch\n")
    print("      Map       Mileage")
    print("      Measure   Distance")
    print("=" * 60)

    i = 0
    while i < len(distances_inches):
        map_val = distances_inches[i]
        mile_val = distances_miles[i]
        print(f"# {i + 1:2d}    {map_val:4.1f}       {mile_val:4.1f}")
        i += 1


    print("=" * 60)
    print(f"Total Distance:    {total_distance:.1f} miles")
    print()


# пример запуска
if __name__ == "__main__":
    files = ["inmap0.dat", "inmap1.dat", "inmap2.dat"]
    for fname in files:
        solve(fname)
# Чтобы запустить код нужны 3 файла, если нужно по 1. Уберите с массива файлы ,которые не хотите проверять