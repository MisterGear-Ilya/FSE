import math


def is_leap_year(year):
    """Проверяет, является ли год високосным"""
    return (year % 4 == 0 and year % 100 != 0) or (year % 400 == 0)


def get_days_in_month(month, year):
    """Возвращает количество дней в месяце с учётом високосного года"""
    month_days = {
        "January": 31, "March": 31, "May": 31, "July": 31,
        "August": 31, "October": 31, "December": 31,
        "April": 30, "June": 30, "September": 30, "November": 30,
        "February": 29 if is_leap_year(year) else 28
    }
    return month_days.get(month, 0)


def process_file(filename: str):
    """Обрабатывает один файл и генерирует отчёт"""
    outname = filename.replace("Precip", "Report")

    try:
        with open(filename, "r", encoding="utf-8") as f:
            lines = f.readlines()
    except FileNotFoundError:
        print(f"Ошибка: файл {filename} не найден")
        return

    # Удаляем символы новой строки и пустые строки
    lines = [line.strip() for line in lines if line.strip()]

    if len(lines) < 3:
        print(f"Ошибка: файл {filename} содержит недостаточно данных")
        return

    # Чтение данных из файла
    location = lines[1]  # Вторая строка - местоположение

    # Третья строка - месяц и год
    month_year_str = lines[2]
    month_part = month_year_str.split(',')[0].strip()
    year_part = month_year_str.split(',')[1].strip()

    month = month_part
    try:
        year = int(year_part)
    except ValueError:
        print(f"Ошибка: неверный формат года '{year_part}' в файле {filename}")
        return

    days_in_month = get_days_in_month(month, year)
    if days_in_month == 0:
        print(f"Ошибка: неизвестный месяц '{month}' в файле {filename}")
        return

    # Обработка данных об осадках
    precipitation = [None] * (days_in_month + 1)  # Индексы 1..days_in_month
    day_occurrences = {}  # Для отслеживания повторяющихся дней
    errors = []
    line_number = 3  # Начинаем с 4-й строки (индекс 3)

    for i in range(3, len(lines)):
        line = lines[i]
        line_number += 1

        # Разбиваем строку на день и осадки
        parts = line.split()
        if len(parts) < 2:
            continue

        try:
            day = int(parts[0])
            precip = float(parts[1])
        except ValueError:
            continue

        # Проверка на неверный день
        if day < 1 or day > days_in_month:
            errors.append(("Invalid", day, line_number))
            continue

        # Проверка на повторение дня
        if day in day_occurrences:
            errors.append(("Repeated", day, line_number))
            # Не обновляем данные для повторяющегося дня
            continue

        day_occurrences[day] = True
        precipitation[day] = precip

    # Генерация отчёта
    try:
        with open(outname, "w", encoding="utf-8") as f:
            # Заголовки отчёта
            f.write("Programmer: Ilya Alferovich\n")
            f.write("CS 1044 Project 5 Fall 2008\n")
            f.write("\n")

            # Местоположение и дата
            f.write(f"Precipitation report for {location} during {month}, {year}\n")
            f.write("\n")

            # Вывод ошибок
            if errors:
                f.write("Error         Day       Line\n")
                for error_type, day, line_num in errors:
                    f.write(f"{error_type:<12} {day:>3} {line_num:>10}\n")
                f.write("\n")

            # Заголовок гистограммы
            f.write("Day Amount Graph\n")

            # Гистограмма
            for day in range(1, days_in_month + 1):
                f.write(f"{day:>3}   ")
                if precipitation[day] is None:
                    f.write("  NA")
                else:
                    f.write(f"{precipitation[day]:5.2f} ")
                    # Звёздочки: одна звезда на каждые 0.25 дюйма
                    if precipitation[day] > 0:
                        stars_count = math.ceil(precipitation[day] / 0.25)
                        f.write("*" * stars_count)
                f.write("\n")
            f.write("\n")

            # Статистика
            valid_precipitation = [p for p in precipitation[1:] if p is not None and p >= 0]

            f.write("Minimum     Maximum     Average\n")
            if valid_precipitation:
                min_precip = min(valid_precipitation)
                max_precip = max(valid_precipitation)
                avg_precip = sum(valid_precipitation) / get_days_in_month(month, year)

                f.write(f"{min_precip:>7.2f} {max_precip:>11.2f} {avg_precip:>11.2f}\n")
            else:
                f.write("   NA         NA         NA\n")

        print(f"Отчёт успешно сгенерирован в файле {outname}")

    except Exception as e:
        print(f"Ошибка при записи отчёта {outname}: {e}")


if __name__ == "__main__":
    files = ["Precip.txt", "Precip1.txt", "Precip2.txt"]
    for fname in files:
        print(f"Обработка файла: {fname}")
        process_file(fname)
        print()