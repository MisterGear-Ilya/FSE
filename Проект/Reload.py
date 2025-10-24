import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np
from matplotlib import rcParams
import warnings
import tkinter as tk
from tkinter import ttk, messagebox, scrolledtext
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import matplotlib

matplotlib.use('TkAgg')

warnings.filterwarnings('ignore')

# Настройка стиля для красивых графиков
plt.style.use('seaborn-v0_8')
rcParams['figure.figsize'] = (12, 8)
rcParams['font.size'] = 12

file_path = "Input-Output_table_system_2021.xlsx"


class InputOutputAnalyzer:
    def __init__(self, root):
        self.root = root
        self.root.title("Анализатор Input-Output таблиц")
        self.root.geometry("1200x800")
        self.root.configure(bg='#f0f0f0')

        # Загружаем данные при запуске
        self.df = None
        self.industry_names = []
        self.data = pd.DataFrame()

        self.load_data()
        self.setup_ui()

    def load_data(self):
        """Загрузка данных из файла"""
        try:
            self.df = pd.read_excel(file_path, sheet_name='Коэффициенты', header=None)
            self.industry_names, self.data = self.prepare_data_for_visualization(self.df)
            return True
        except Exception as e:
            messagebox.showerror("Ошибка", f"Не удалось загрузить данные: {e}")
            return False

    def prepare_data_for_visualization(self, df):
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

    def setup_ui(self):
        """Создание пользовательского интерфейса"""
        # Создаем Notebook (вкладки)
        self.notebook = ttk.Notebook(self.root)
        self.notebook.pack(fill='both', expand=True, padx=10, pady=10)

        # Вкладка "Обзор"
        self.overview_frame = ttk.Frame(self.notebook)
        self.notebook.add(self.overview_frame, text="Обзор данных")
        self.setup_overview_tab()

        # Вкладка "Визуализация"
        self.viz_frame = ttk.Frame(self.notebook)
        self.notebook.add(self.viz_frame, text="Визуализация")
        self.setup_visualization_tab()

        # Вкладка "Данные"
        self.data_frame = ttk.Frame(self.notebook)
        self.notebook.add(self.data_frame, text="Просмотр данных")
        self.setup_data_tab()

        # Статус бар
        self.status_var = tk.StringVar()
        self.status_var.set(f"Загружено {len(self.industry_names)} отраслей")
        status_bar = ttk.Label(self.root, textvariable=self.status_var, relief='sunken')
        status_bar.pack(side='bottom', fill='x')

    def setup_overview_tab(self):
        """Настройка вкладки обзора"""
        # Заголовок
        title_label = ttk.Label(self.overview_frame,
                                text="Анализатор Input-Output таблиц",
                                font=('Arial', 16, 'bold'))
        title_label.pack(pady=10)

        # Информация о данных
        info_frame = ttk.LabelFrame(self.overview_frame, text="Информация о данных")
        info_frame.pack(fill='x', padx=10, pady=5)

        info_text = scrolledtext.ScrolledText(info_frame, height=8, width=100)
        info_text.pack(fill='both', expand=True, padx=5, pady=5)

        # Заполняем информацию
        info_content = f"""
Файл: {file_path}
Лист: Коэффициенты
Размер данных: {self.df.shape[0]} строк, {self.df.shape[1]} столбцов
Количество отраслей: {len(self.industry_names)}

Статистика:
- Всего ячеек: {self.df.shape[0] * self.df.shape[1]}
- Числовых данных: {self.data.size}
- Отрасли с данными: {len(self.industry_names)}

Доступные функции:
1. Просмотр данных таблицы
2. Постраничный просмотр
3. Создание графиков и диаграмм
        """
        info_text.insert('1.0', info_content)
        info_text.config(state='disabled')

        # Быстрые действия
        actions_frame = ttk.LabelFrame(self.overview_frame, text="Быстрые действия")
        actions_frame.pack(fill='x', padx=10, pady=5)

        ttk.Button(actions_frame, text="Просмотреть данные",
                   command=self.show_data_table).pack(side='left', padx=5, pady=5)
        ttk.Button(actions_frame, text="Создать тепловую карту",
                   command=lambda: self.create_heatmap()).pack(side='left', padx=5, pady=5)
        ttk.Button(actions_frame, text="Топ отраслей",
                   command=lambda: self.create_bar_chart()).pack(side='left', padx=5, pady=5)

    def setup_visualization_tab(self):
        """Настройка вкладки визуализации"""
        # Выбор типа графика
        viz_type_frame = ttk.LabelFrame(self.viz_frame, text="Тип визуализации")
        viz_type_frame.pack(fill='x', padx=10, pady=5)

        # Кнопки для разных типов графиков
        ttk.Button(viz_type_frame, text="Тепловая карта",
                   command=self.create_heatmap).pack(side='left', padx=5, pady=5)
        ttk.Button(viz_type_frame, text="Столбчатая диаграмма",
                   command=self.create_bar_chart).pack(side='left', padx=5, pady=5)
        ttk.Button(viz_type_frame, text="Круговая диаграмма",
                   command=self.create_pie_chart).pack(side='left', padx=5, pady=5)
        ttk.Button(viz_type_frame, text="Линейные графики",
                   command=self.create_line_chart).pack(side='left', padx=5, pady=5)
        ttk.Button(viz_type_frame, text="Все графики",
                   command=self.create_all_charts).pack(side='left', padx=5, pady=5)

        # Область для отображения графиков
        self.viz_canvas_frame = ttk.Frame(self.viz_frame)
        self.viz_canvas_frame.pack(fill='both', expand=True, padx=10, pady=5)

    def setup_data_tab(self):
        """Настройка вкладки просмотра данных"""
        # Панель управления
        control_frame = ttk.Frame(self.data_frame)
        control_frame.pack(fill='x', padx=10, pady=5)

        ttk.Button(control_frame, text="Показать все данные",
                   command=self.show_data_table).pack(side='left', padx=5)
        ttk.Button(control_frame, text="Постраничный просмотр",
                   command=self.show_paginated_data).pack(side='left', padx=5)

        # Область для отображения данных
        self.data_text = scrolledtext.ScrolledText(self.data_frame, height=30, width=120)
        self.data_text.pack(fill='both', expand=True, padx=10, pady=5)

    def show_data_table(self):
        """Показать данные таблицы"""
        if self.df is None:
            messagebox.showwarning("Предупреждение", "Данные не загружены")
            return

        self.data_text.delete('1.0', 'end')

        # Показываем первые 50 строк и столбцов
        display_rows = min(50, len(self.df))
        display_cols = min(50, len(self.df.columns))

        output = f"Данные таблицы (показано {display_rows} из {len(self.df)} строк, {display_cols} из {len(self.df.columns)} столбцов)\n\n"

        for i in range(display_rows):
            # Название отрасли
            name_cell = self.df.iloc[i, 0]
            name_text = str(name_cell) if pd.notna(name_cell) else ""
            if len(name_text) > 60:
                name_text = name_text[:57] + "..."

            output += f"Строка {i + 1:3}: {name_text:<60}"

            # Числовые данные
            for j in range(1, display_cols):
                cell_value = self.df.iloc[i, j]
                if pd.isna(cell_value):
                    output += " " * 12
                else:
                    try:
                        num_value = float(str(cell_value).replace(',', '.'))
                        output += f"{num_value:>12.3f}"
                    except (ValueError, TypeError):
                        short_text = str(cell_value)[:10]
                        output += f"{short_text:>12}"

            output += "\n"

        self.data_text.insert('1.0', output)
        self.status_var.set(f"Показано {display_rows} строк данных")

    def show_paginated_data(self):
        """Постраничный просмотр данных"""
        if self.df is None:
            messagebox.showwarning("Предупреждение", "Данные не загружены")
            return

        # Создаем новое окно для постраничного просмотра
        pagination_window = tk.Toplevel(self.root)
        pagination_window.title("Постраничный просмотр данных")
        pagination_window.geometry("1000x700")

        # Переменные для пагинации
        current_page = tk.IntVar(value=0)
        rows_per_page = 20
        total_pages = (len(self.df) // rows_per_page) + 1

        def update_display():
            page = current_page.get()
            start_row = page * rows_per_page
            end_row = min((page + 1) * rows_per_page, len(self.df))

            text_widget.delete('1.0', 'end')
            output = f"Страница {page + 1} из {total_pages} (строки {start_row + 1}-{end_row})\n\n"

            for i in range(start_row, end_row):
                name_cell = self.df.iloc[i, 0]
                name_text = str(name_cell) if pd.notna(name_cell) else ""
                if len(name_text) > 50:
                    name_text = name_text[:47] + "..."

                output += f"Строка {i + 1:3}: {name_text:<50}"

                # Показываем первые 10 числовых столбцов
                for j in range(1, min(11, len(self.df.columns))):
                    cell_value = self.df.iloc[i, j]
                    if pd.isna(cell_value):
                        output += " " * 10
                    else:
                        try:
                            num_value = float(str(cell_value).replace(',', '.'))
                            output += f"{num_value:>10.2f}"
                        except (ValueError, TypeError):
                            short_text = str(cell_value)[:8]
                            output += f"{short_text:>10}"

                output += "\n"

            text_widget.insert('1.0', output)

        # Элементы управления пагинацией
        control_frame = ttk.Frame(pagination_window)
        control_frame.pack(fill='x', padx=10, pady=5)

        ttk.Button(control_frame, text="Первая",
                   command=lambda: [current_page.set(0), update_display()]).pack(side='left', padx=2)
        ttk.Button(control_frame, text="Предыдущая",
                   command=lambda: [current_page.set(max(0, current_page.get() - 1)), update_display()]).pack(
            side='left', padx=2)
        ttk.Button(control_frame, text="Следующая",
                   command=lambda: [current_page.set(min(total_pages - 1, current_page.get() + 1)),
                                    update_display()]).pack(side='left', padx=2)
        ttk.Button(control_frame, text="Последняя",
                   command=lambda: [current_page.set(total_pages - 1), update_display()]).pack(side='left', padx=2)

        # Область отображения
        text_widget = scrolledtext.ScrolledText(pagination_window, width=120, height=35)
        text_widget.pack(fill='both', expand=True, padx=10, pady=5)

        update_display()

    def clear_viz_canvas(self):
        """Очистка области визуализации"""
        for widget in self.viz_canvas_frame.winfo_children():
            widget.destroy()

    def create_heatmap(self):
        """Тепловая карта коэффициентов"""
        if self.data.empty:
            messagebox.showwarning("Предупреждение", "Нет данных для построения тепловой карты")
            return

        self.clear_viz_canvas()

        fig, ax = plt.subplots(figsize=(14, 10))

        # Берем только первые 20 отраслей для читаемости
        plot_data = self.data.iloc[:20, :20]
        plot_names = [name[:30] + '...' if len(name) > 30 else name for name in self.industry_names[:20]]

        # Заменяем NaN на 0
        plot_data = plot_data.fillna(0)

        sns.heatmap(plot_data,
                    annot=False,
                    cmap='YlOrRd',
                    xticklabels=False,
                    yticklabels=plot_names,
                    cbar_kws={'label': 'Коэффициент затрат'},
                    ax=ax)

        ax.set_title('Тепловая карта коэффициентов прямых затрат\n(первые 20 отраслей)', fontsize=16, pad=20)
        ax.set_ylabel('Отрасли', fontsize=14)
        ax.set_xlabel('Виды продукции/услуг', fontsize=14)

        # Встраиваем график в tkinter
        canvas = FigureCanvasTkAgg(fig, self.viz_canvas_frame)
        canvas.draw()
        canvas.get_tk_widget().pack(fill='both', expand=True)

        self.status_var.set("Создана тепловая карта коэффициентов")

    def create_bar_chart(self):
        """Столбчатая диаграмма суммарных коэффициентов по отраслям"""
        if self.data.empty:
            messagebox.showwarning("Предупреждение", "Нет данных для построения столбчатой диаграммы")
            return

        self.clear_viz_canvas()

        fig, ax = plt.subplots(figsize=(12, 8))

        # Суммируем коэффициенты по строкам (по отраслям)
        total_coefficients = self.data.sum(axis=1)

        # Берем топ-15 отраслей по суммарным коэффициентам
        top_15 = total_coefficients.nlargest(15)
        top_industries = [
            self.industry_names[i][:40] + '...' if len(self.industry_names[i]) > 40 else self.industry_names[i]
            for i in top_15.index]

        bars = ax.barh(range(len(top_15)), top_15.values, color='steelblue', alpha=0.7)

        for i, bar in enumerate(bars):
            ax.text(bar.get_width() + 0.1, bar.get_y() + bar.get_height() / 2,
                    f'{bar.get_width():.1f}', ha='left', va='center', fontsize=10)

        ax.set_yticks(range(len(top_15)))
        ax.set_yticklabels(top_industries, fontsize=10)
        ax.set_xlabel('Суммарный коэффициент затрат', fontsize=14)
        ax.set_title('Топ-15 отраслей по суммарным коэффициентам прямых затрат', fontsize=16, pad=20)
        ax.invert_yaxis()
        ax.grid(axis='x', alpha=0.3)

        canvas = FigureCanvasTkAgg(fig, self.viz_canvas_frame)
        canvas.draw()
        canvas.get_tk_widget().pack(fill='both', expand=True)

        self.status_var.set("Создана столбчатая диаграмма топ-15 отраслей")

    def create_pie_chart(self):
        """Круговая диаграмма распределения коэффициентов"""
        if self.data.empty:
            messagebox.showwarning("Предупреждение", "Нет данных для построения круговой диаграммы")
            return

        self.clear_viz_canvas()

        fig, ax = plt.subplots(figsize=(10, 8))

        total_coefficients = self.data.sum(axis=1)
        if len(total_coefficients) < 8:
            messagebox.showwarning("Предупреждение", "Недостаточно данных для построения круговой диаграммы")
            return

        top_8 = total_coefficients.nlargest(8)
        other_sum = total_coefficients.sum() - top_8.sum()

        sizes = list(top_8.values) + [other_sum]
        labels = [self.industry_names[i][:20] + '...' if len(self.industry_names[i]) > 20 else self.industry_names[i]
                  for i in top_8.index] + ['Остальные отрасли']

        colors = plt.cm.Set3(np.linspace(0, 1, len(sizes)))

        wedges, texts, autotexts = ax.pie(sizes, labels=labels, colors=colors, autopct='%1.1f%%',
                                          startangle=90, textprops={'fontsize': 10})

        for autotext in autotexts:
            autotext.set_color('white')
            autotext.set_fontweight('bold')

        ax.set_title('Распределение коэффициентов затрат по отраслям\n(топ-8 отраслей)', fontsize=16, pad=20)

        canvas = FigureCanvasTkAgg(fig, self.viz_canvas_frame)
        canvas.draw()
        canvas.get_tk_widget().pack(fill='both', expand=True)

        self.status_var.set("Создана круговая диаграмма распределения")

    def create_line_chart(self):
        """Линейный график коэффициентов для выбранных отраслей"""
        if self.data.empty:
            messagebox.showwarning("Предупреждение", "Нет данных для построения линейного графика")
            return

        self.clear_viz_canvas()

        fig, ax = plt.subplots(figsize=(12, 6))

        # Выбираем до 5 отраслей для отображения
        num_industries = min(5, len(self.industry_names))
        selected_indices = list(range(num_industries))
        selected_industries = [
            self.industry_names[i][:30] + '...' if len(self.industry_names[i]) > 30 else self.industry_names[i]
            for i in selected_indices]

        for i, idx in enumerate(selected_indices):
            if idx < len(self.data):
                # Берем первые 20 коэффициентов или меньше, если данных меньше
                num_coefficients = min(20, len(self.data.columns))
                coefficients = self.data.iloc[idx, :num_coefficients]
                ax.plot(range(len(coefficients)), coefficients.values,
                        marker='o', linewidth=2, markersize=6, label=selected_industries[i])

        ax.set_xlabel('Номер коэффициента', fontsize=14)
        ax.set_ylabel('Значение коэффициента', fontsize=14)
        ax.set_title('Динамика коэффициентов затрат для выбранных отраслей', fontsize=16, pad=20)
        ax.legend(bbox_to_anchor=(0.8, 1), loc='upper left')
        ax.grid(True, alpha=0.3)
        ax.set_xticks(range(0, min(20, len(self.data.columns)), 2))

        canvas = FigureCanvasTkAgg(fig, self.viz_canvas_frame)
        canvas.draw()
        canvas.get_tk_widget().pack(fill='both', expand=True)

        self.status_var.set("Созданы линейные графики по отраслям")

    def create_all_charts(self):
        """Создание всех графиков в отдельных окнах"""
        if self.data.empty:
            messagebox.showwarning("Предупреждение", "Нет данных для построения графиков")
            return

        self.create_heatmap()
        messagebox.showinfo("Информация", "Все графики созданы! Переключайтесь между вкладками для просмотра.")
        self.status_var.set("Созданы все типы графиков")


def main():
    root = tk.Tk()
    app = InputOutputAnalyzer(root)
    root.mainloop()


if __name__ == "__main__":
    main()