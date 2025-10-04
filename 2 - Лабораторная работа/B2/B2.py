from math import *

def wind_chill(Tf, V):
    #Вычесление температуры
    return 35.74 + 0.6125 * Tf + (0.4275 * Tf - 35.75) * (V ** 0.16)

def solve(filename: str):
    outname = filename.replace("WCData", "WindChillReport")

    times = []
    wc_temps = []
    wc_effects = []

    with open(filename, "r", encoding="utf-8") as f:
        lines = f.readlines()

    # начиная с 3-й строки идут данные
    for line in lines[2:]:
        parts = line.strip().split()
        if len(parts) < 3:
            continue
        time = parts[0]
        temp_f = int(parts[1])
        wind = int(parts[2])

        wc = wind_chill(temp_f, wind)
        effect = wc - temp_f

        times.append(time)
        wc_temps.append(wc)
        wc_effects.append(effect)

    # средняя скорректированная температура
    avg_wc = sum(wc_temps) / len(wc_temps)

    # создаю отчет
    output_lines = []
    output_lines.append("Time     WC temp     WC Effect")
    output_lines.append("------------------------------")
    for t, wc, eff in zip(times, wc_temps, wc_effects):
        output_lines.append(f"{t:>8}    {wc:5.1f}        {eff:6.1f}")
    output_lines.append("------------------------------")
    output_lines.append("")
    output_lines.append(
        f"The average adjusted temperature, based on {len(wc_temps)} observations, was {avg_wc:.1f}"
    )

    # вывод в консоль
    for line in output_lines:
        print(line)

    # запись в файл
    with open(outname, "w", encoding="utf-8") as f:
        for line in output_lines:
            f.write(line + "\n")


if __name__ == "__main__":
    files = ["1.WCData.txt", "2.WCData.txt", "3.WCData.txt"]
    for fname in files:
        solve(fname)
        print("\n")
# код выводит виде файла , а также и выводит в консоль. Нужны все 3 файла , если какие не надо проверять удалите с к файл с название, который не нужен
