import pandas as pd
import openpyxl as xl

file_path = "Input-Output_table_system_2021.xlsx"
def read():
    """
    Основная функция для чтения и отображения данных из Excel файла
    """
    print("ПРОГРАММА ДЛЯ ПРОСМОТРА EXCEL ФАЙЛОВ")
    print("=" * 60)

    # Выбор режима работы
    print("Выберите как показать данные:")
    print("1 - Полный вывод (первые 100 строк, красивое форматирование)")
    print("2 - Постраничный вывод (удобно для больших файлов)")

    choice = input("Введите 1 или 2: ").strip()

    if choice == "1":
        # Показать все сразу с красивым форматированием
        data = read_input_output_table(file_path)
    elif choice == "2":
        # Показать по страницам
        read_with_pagination(file_path)
    else:
        # Если ввели что-то неправильно - используем режим по умолчанию
        print("Не понял ваш выбор. Показываю полный вывод...")
        data = read_input_output_table(file_path)


def read_input_output_table(file_path):
    try:
        # Открываем Excel файл
        xls = pd.ExcelFile(file_path)

        # Показываем все листы в файле
        print("В этом файле есть следующие листы:")
        for sheet_name in xls.sheet_names:
            print(f"  - {sheet_name}")

        # Читаем данные с листа "Коэффициенты"
        df = pd.read_excel(file_path, sheet_name='Коэффициенты', header=None)

        # Показываем информацию о файле
        print(f"\n" + "=" * 100)
        print(f"ФАЙЛ: {file_path}")
        print(f"ЛИСТ: Коэффициенты")
        print(f"РАЗМЕР: {df.shape[0]} строк, {df.shape[1]} столбцов")
        print("=" * 100)

        # Определяем ширину для названий (первый столбец)
        name_width = 80

        # Показываем данные построчно
        for i in range(min(len(df), 100)):
            # Формируем строку с названием
            name_cell = df.iloc[i, 0]
            if pd.isna(name_cell):
                name_part = " " * name_width
            else:
                name_text = str(name_cell)
                # Если название слишком длинное, переносим на новую строку
                if len(name_text) > name_width:
                    # Разбиваем название на части
                    words = name_text.split()
                    current_line = ""
                    name_lines = []

                    for word in words:
                        if len(current_line + " " + word) <= name_width:
                            if current_line:
                                current_line += " " + word
                            else:
                                current_line = word
                        else:
                            name_lines.append(current_line)
                            current_line = word

                    if current_line:
                        name_lines.append(current_line)

                    # Первая строка с названием
                    name_part = f"{name_lines[0]:<{name_width}}"
                else:
                    name_part = f"{name_text:<{name_width}}"

            # Формируем числовую часть
            number_part = ""
            for j in range(1, min(len(df.columns), 50)):
                cell_value = df.iloc[i, j]

                if pd.isna(cell_value):
                    number_part += " " * 12
                else:
                    if isinstance(cell_value, (int, float)):
                        number_part += f"{cell_value:>12.3f}"
                    else:
                        short_text = str(cell_value)[:10]
                        number_part += f"{short_text:>12}"

            # Печатаем первую строку
            print(f"Строка {i + 1:3}: {name_part}{number_part}")

            # Если название было разбито на несколько строк, печатаем остальные
            if not pd.isna(name_cell) and len(str(name_cell)) > name_width:
                words = str(name_cell).split()
                current_line = ""
                name_lines = []

                for word in words:
                    if len(current_line + " " + word) <= name_width:
                        if current_line:
                            current_line += " " + word
                        else:
                            current_line = word
                    else:
                        name_lines.append(current_line)
                        current_line = word

                if current_line:
                    name_lines.append(current_line)

                # Печатаем остальные строки названия
                for line_num in range(1, len(name_lines)):
                    print(f"       : {name_lines[line_num]:<{name_width}}")

        # Показываем сколько всего вывели
        print(f"\nПоказано {min(len(df), 100)} строк из {len(df)}")
        print(f"Показано {min(len(df.columns), 50)} столбцов из {len(df.columns)}")

        # Статистика файла
        print(f"\nСТАТИСТИКА ФАЙЛА:")
        total_cells = df.shape[0] * df.shape[1]
        filled_cells = df.count().sum()
        empty_cells = df.isna().sum().sum()

        print(f"Всего ячеек: {total_cells}")
        print(f"Заполненных ячеек: {filled_cells}")
        print(f"Пустых ячеек: {empty_cells}")

        return df

    except FileNotFoundError:
        print(f"Ошибка: Файл {file_path} не найден!")
        print("Проверьте правильность имени файла и путь")
        return None
    except Exception as e:
        print(f"Ошибка при чтении файла: {e}")
        return None


def read_with_pagination(file_path, rows_per_page=20, cols_per_page=10):
    """
    Показывает данные постранично - удобно для больших файлов
    """
    try:
        # Читаем файл
        df = pd.read_excel(file_path, sheet_name='Коэффициенты', header=None)

        total_rows = len(df)
        total_cols = len(df.columns)

        # Проходим по всем строкам блоками
        for start_row in range(0, total_rows, rows_per_page):
            end_row = min(start_row + rows_per_page, total_rows)

            # Проходим по всем столбцам блоками
            for start_col in range(0, total_cols, cols_per_page):
                end_col = min(start_col + cols_per_page, total_cols)

                # Показываем заголовок блока
                print(f"\n" + "=" * 100)
                print(f"БЛОК ДАННЫХ:")
                print(f"Строки: {start_row + 1}-{end_row}")
                print(f"Столбцы: {start_col + 1}-{end_col}")
                print("=" * 100)

                # Показываем строки текущего блока
                for i in range(start_row, end_row):
                    # Формируем строку с названием
                    name_cell = df.iloc[i, 0]
                    name_width = 60

                    if pd.isna(name_cell):
                        name_part = " " * name_width
                    else:
                        name_text = str(name_cell)
                        if len(name_text) > name_width:
                            name_part = name_text[:name_width - 3] + "..."
                        else:
                            name_part = f"{name_text:<{name_width}}"

                    # Формируем числовую часть
                    number_part = ""
                    for j in range(max(1, start_col), end_col):
                        cell_value = df.iloc[i, j]

                        if pd.isna(cell_value):
                            number_part += " " * 12
                        else:
                            if isinstance(cell_value, (int, float)):
                                number_part += f"{cell_value:>12.3f}"
                            else:
                                short_text = str(cell_value)[:10]
                                number_part += f"{short_text:>12}"

                    # Печатаем строку
                    print(f"Строка {i + 1:3}: {name_part}{number_part}")

                # Ждем пока пользователь нажмет Enter
                input("\nНажмите Enter чтобы посмотреть следующий блок...")

    except Exception as e:
        print(f"Ошибка: {e}")


# Запуск основной функции
if __name__ == "__main__":
   read()
   # data = read_input_output_table(file_path)
 #   data = pd.read_excel(file_path, sheet_name='Коэффициенты', header=None)
 #   print('Файлы прочитаны из excel!',sep='',end='\n\n')






