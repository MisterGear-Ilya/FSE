import pandas as pd
import openpyxl as xl
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np
from matplotlib import rcParams
import warnings

warnings.filterwarnings('ignore')

# Настройка стиля для красивых графиков
plt.style.use('seaborn-v0_8')
rcParams['figure.figsize'] = (12, 8)
rcParams['font.size'] = 12

file_path = "Input-Output_table_system_2021.xlsx"


def prepare_data_for_visualization(df):
    """Подготовка данных для визуализации с правильной обработкой"""
    try:
        # Пропускаем строки с заголовками и находим начало числовых данных
        numeric_data_start = 0
        for i in range(len(df)):
            row_has_numbers = False
            for j in range(1, min(10, len(df.columns))):
                try:
                    float(str(df.iloc[i, j]).replace(',', '.'))
                    row_has_numbers = True
                    break
                except (ValueError, TypeError):
                    continue

            if row_has_numbers:
                numeric_data_start = i
                break

        print(f"Числовые данные начинаются с строки {numeric_data_start + 1}")

        # Извлекаем названия отраслей и числовые данные
        industry_names = []
        numeric_data = []

        for i in range(numeric_data_start, len(df)):
            if pd.notna(df.iloc[i, 0]) and isinstance(df.iloc[i, 0], str) and len(str(df.iloc[i, 0])) > 2:
                industry_name = str(df.iloc[i, 0]).strip()
                row_data = []
                valid_row = False

                for j in range(1, len(df.columns)):
                    cell_value = df.iloc[i, j]
                    try:
                        if pd.notna(cell_value):
                            num_value = float(str(cell_value).replace(',', '.'))
                            row_data.append(num_value)
                            valid_row = True
                        else:
                            row_data.append(0.0)
                    except (ValueError, TypeError):
                        row_data.append(0.0)

                if valid_row:
                    industry_names.append(industry_name)
                    numeric_data.append(row_data)

        data = pd.DataFrame(numeric_data)
        print(f"Подготовлено {len(industry_names)} отраслей с числовыми данными")

        return industry_names, data

    except Exception as e:
        print(f"Ошибка при подготовке данных: {e}")
        return [], pd.DataFrame()


def create_visualizations():
    """Создание графиков и диаграмм на основе данных"""
    print("\n" + "=" * 60)
    print("СОЗДАНИЕ ГРАФИКОВ И ДИАГРАММ")
    print("=" * 60)

    try:
        # Загружаем данные
        df = pd.read_excel(file_path, sheet_name='Коэффициенты', header=None)
        print("Данные успешно загружены для визуализации!")

        # Подготавливаем данные для графиков
        industry_names, data = prepare_data_for_visualization(df)

        if len(industry_names) == 0:
            print("Не удалось найти подходящие данные для визуализации")
            return

        # Меню выбора типа визуализации
        while True:
            print(f"\nНайдено {len(industry_names)} отраслей с данными")
            print("Выберите тип визуализации:")
            print("1 - Тепловая карта коэффициентов")
            print("2 - Столбчатая диаграмма (топ-15 отраслей)")
            print("3 - Круговая диаграмма распределения")
            print("4 - Линейные графики по отраслям")
            print("5 - Все графики сразу")
            print("6 - Вернуться в главное меню")

            choice = input("Введите номер (1-6): ").strip()

            if choice == "1":
                create_heatmap(data, industry_names)
            elif choice == "2":
                create_bar_chart(data, industry_names)
            elif choice == "3":
                create_pie_chart(data, industry_names)
            elif choice == "4":
                create_line_chart(data, industry_names)
            elif choice == "5":
                create_all_charts(data, industry_names)
            elif choice == "6":
                print("Возврат в главное меню...")
                break
            else:
                print("Неверный выбор. Попробуйте снова.")

    except Exception as e:
        print(f"Ошибка при создании графиков: {e}")


def create_heatmap(data, industry_names):
    """Тепловая карта коэффициентов"""
    if data.empty:
        print("Нет данных для построения тепловой карты")
        return

    plt.figure(figsize=(16, 12))

    # Берем только первые 20 отраслей для читаемости
    plot_data = data.iloc[:20, :20]
    plot_names = [name[:30] + '...' if len(name) > 30 else name for name in industry_names[:20]]

    # Заменяем NaN на 0
    plot_data = plot_data.fillna(0)

    sns.heatmap(plot_data,
                annot=False,
                cmap='YlOrRd',
                xticklabels=False,
                yticklabels=plot_names,
                cbar_kws={'label': 'Коэффициент затрат'})

    plt.title('Тепловая карта коэффициентов прямых затрат\n(первые 20 отраслей)', fontsize=16, pad=20)
    plt.ylabel('Отрасли', fontsize=14)
    plt.xlabel('Виды продукции/услуг', fontsize=14)
    plt.tight_layout()
    plt.show()


def create_bar_chart(data, industry_names):
    """Столбчатая диаграмма суммарных коэффициентов по отраслям"""
    if data.empty:
        print("Нет данных для построения столбчатой диаграммы")
        return

    plt.figure(figsize=(14, 10))

    # Суммируем коэффициенты по строкам (по отраслям)
    total_coefficients = data.sum(axis=1)

    # Берем топ-15 отраслей по суммарным коэффициентам
    top_15 = total_coefficients.nlargest(15)
    top_industries = [industry_names[i][:40] + '...' if len(industry_names[i]) > 40 else industry_names[i]
                      for i in top_15.index]

    bars = plt.barh(range(len(top_15)), top_15.values, color='steelblue', alpha=0.7)

    for i, bar in enumerate(bars):
        plt.text(bar.get_width() + 0.1, bar.get_y() + bar.get_height() / 2,
                 f'{bar.get_width():.1f}', ha='left', va='center', fontsize=10)

    plt.yticks(range(len(top_15)), top_industries, fontsize=10)
    plt.xlabel('Суммарный коэффициент затрат', fontsize=14)
    plt.title('Топ-15 отраслей по суммарным коэффициентам прямых затрат', fontsize=16, pad=20)
    plt.gca().invert_yaxis()
    plt.grid(axis='x', alpha=0.3)
    plt.tight_layout()
    plt.show()


def create_pie_chart(data, industry_names):
    """Круговая диаграмма распределения коэффициентов"""
    if data.empty:
        print("Нет данных для построения круговой диаграммы")
        return

    plt.figure(figsize=(12, 12))

    total_coefficients = data.sum(axis=1)
    if len(total_coefficients) < 8:
        print("Недостаточно данных для построения круговой диаграммы")
        return

    top_8 = total_coefficients.nlargest(8)
    other_sum = total_coefficients.sum() - top_8.sum()

    sizes = list(top_8.values) + [other_sum]
    labels = [industry_names[i][:20] + '...' if len(industry_names[i]) > 20 else industry_names[i]
              for i in top_8.index] + ['Остальные отрасли']

    colors = plt.cm.Set3(np.linspace(0, 1, len(sizes)))

    wedges, texts, autotexts = plt.pie(sizes, labels=labels, colors=colors, autopct='%1.1f%%',
                                       startangle=90, textprops={'fontsize': 10})

    for autotext in autotexts:
        autotext.set_color('white')
        autotext.set_fontweight('bold')

    plt.title('Распределение коэффициентов затрат по отраслям\n(топ-8 отраслей)', fontsize=16, pad=20)
    plt.axis('equal')
    plt.tight_layout()
    plt.show()


def create_line_chart(data, industry_names):
    """Линейный график коэффициентов для выбранных отраслей"""
    if data.empty:
        print("Нет данных для построения линейного графика")
        return

    plt.figure(figsize=(14, 8))

    # Выбираем до 5 отраслей для отображения
    num_industries = min(5, len(industry_names))
    selected_indices = list(range(num_industries))
    selected_industries = [industry_names[i][:30] + '...' if len(industry_names[i]) > 30 else industry_names[i]
                           for i in selected_indices]

    for i, idx in enumerate(selected_indices):
        if idx < len(data):
            # Берем первые 20 коэффициентов или меньше, если данных меньше
            num_coefficients = min(20, len(data.columns))
            coefficients = data.iloc[idx, :num_coefficients]
            plt.plot(range(len(coefficients)), coefficients.values,
                     marker='o', linewidth=2, markersize=6, label=selected_industries[i])

    plt.xlabel('Номер коэффициента', fontsize=14)
    plt.ylabel('Значение коэффициента', fontsize=14)
    plt.title('Динамика коэффициентов затрат для выбранных отраслей', fontsize=16, pad=20)
    plt.legend(bbox_to_anchor=(1.05, 1), loc='upper left')
    plt.grid(True, alpha=0.3)
    plt.xticks(range(0, min(20, len(data.columns)), 2))
    plt.tight_layout()
    plt.show()


def create_all_charts(data, industry_names):
    """Создание всех графиков сразу"""
    if data.empty:
        print("Нет данных для построения графиков")
        return

    print("Создаю все графики...")

    create_heatmap(data, industry_names)
    create_bar_chart(data, industry_names)
    create_pie_chart(data, industry_names)
    create_line_chart(data, industry_names)

    print("Все графики созданы!")


def read():
    """
    Основная функция для чтения и отображения данных из Excel файла
    """
    print("ПРОГРАММА ДЛЯ АНАЛИЗА INPUT-OUTPUT TABLE")
    print("=" * 60)

    while True:
        print("\nВыберите действие:")
        print("1 - Просмотреть данные таблицы")
        print("2 - Постраничный просмотр данных")
        print("3 - Создать графики и диаграммы")
        print("4 - Выйти из программы")

        choice = input("Введите номер (1-4): ").strip()

        if choice == "1":
            data = read_input_output_table(file_path)
        elif choice == "2":
            read_with_pagination(file_path)
        elif choice == "3":
            create_visualizations()
        elif choice == "4":
            print("Выход из программы. До свидания!")
            break
        else:
            print("Неверный выбор. Попробуйте снова.")


# Ваши существующие функции read_input_output_table и read_with_pagination остаются без изменений
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
                    # Пробуем преобразовать в число, если не получается - показываем как текст
                    try:
                        num_value = float(str(cell_value).replace(',', '.'))
                        number_part += f"{num_value:>12.3f}"
                    except (ValueError, TypeError):
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

        # Считаем заполненные ячейки (не пустые и не текст "Б" и подобные)
        filled_cells = 0
        for i in range(len(df)):
            for j in range(len(df.columns)):
                cell_value = df.iloc[i, j]
                if pd.notna(cell_value):
                    try:
                        float(str(cell_value).replace(',', '.'))
                        filled_cells += 1
                    except (ValueError, TypeError):
                        if str(cell_value).strip() != '':
                            filled_cells += 1

        empty_cells = total_cells - filled_cells

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
                            try:
                                num_value = float(str(cell_value).replace(',', '.'))
                                number_part += f"{num_value:>12.3f}"
                            except (ValueError, TypeError):
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