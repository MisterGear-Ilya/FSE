import xml.etree.ElementTree as ET
import matplotlib.pyplot as plt
import matplotlib

matplotlib.rcParams['font.family'] = 'DejaVu Sans'  # Для поддержки кириллицы
from collections import defaultdict, Counter
import numpy as np
import pandas as pd


def load_users_data(filename='users.xml'):
    """
    Загружает данные о пользователях из XML файла
    """
    try:
        tree = ET.parse(filename)
        root = tree.getroot()
        users = []

        for user_elem in root.findall('user'):
            user = {
                'user_id': int(user_elem.find('user_id').text),
                'name': user_elem.find('name').text,
                'age': int(user_elem.find('age').text),
                'weight': int(user_elem.find('weight').text),
                'fitness_level': user_elem.find('fitness_level').text
            }
            users.append(user)

        print(f"Загружено {len(users)} пользователей")
        return users

    except FileNotFoundError:
        print(f"Файл {filename} не найден")
        return []
    except Exception as e:
        print(f"Ошибка при загрузке данных пользователей: {e}")
        return []


def load_workouts_data(filename='workouts.xml'):
    """
    Загружает данные о тренировках из XML файла
    """
    try:
        tree = ET.parse(filename)
        root = tree.getroot()
        workouts = []

        for workout_elem in root.findall('workout'):
            workout = {
                'workout_id': int(workout_elem.find('workout_id').text),
                'user_id': int(workout_elem.find('user_id').text),
                'date': workout_elem.find('date').text,
                'type': workout_elem.find('type').text,
                'duration': int(workout_elem.find('duration').text),
                'distance': float(workout_elem.find('distance').text),
                'calories': int(workout_elem.find('calories').text),
                'avg_heart_rate': int(workout_elem.find('avg_heart_rate').text),
                'intensity': workout_elem.find('intensity').text
            }
            workouts.append(workout)

        print(f"Загружено {len(workouts)} тренировок")
        return workouts

    except FileNotFoundError:
        print(f"Файл {filename} не найден")
        return []
    except Exception as e:
        print(f"Ошибка при загрузке данных тренировок: {e}")
        return []


def get_stats(users, workouts):
    """
    Рассчитывает общую статистику по всем тренировкам
    """
    total_workouts = len(workouts)
    total_users = len(users)
    total_calories = sum(workout['calories'] for workout in workouts)
    total_time_hours = sum(workout['duration'] for workout in workouts) / 60.0
    total_distance = sum(workout['distance'] for workout in workouts)

    print("=" * 35)
    print("ОБЩАЯ СТАТИСТИКА")
    print("=" * 35)
    print(f"Всего тренировок: {total_workouts}")
    print(f"Всего пользователей: {total_users}")
    print(f"Сожжено калорий: {total_calories}")
    print(f"Общее время: {total_time_hours:.1f} часов")
    print(f"Пройдено дистанции: {total_distance:.1f} км")
    print("=" * 35)

    return {
        'total_workouts': total_workouts,
        'total_users': total_users,
        'total_calories': total_calories,
        'total_time_hours': total_time_hours,
        'total_distance': total_distance
    }


def analyze_user_activity(users, workouts):
    """
    Анализирует активность пользователей и выводит ТОП-3
    """
    # Создаем словарь для сбора статистики по пользователям
    user_stats = {}

    for user in users:
        user_workouts = [w for w in workouts if w['user_id'] == user['user_id']]
        user_stats[user['user_id']] = {
            'name': user['name'],
            'fitness_level': user['fitness_level'],
            'workout_count': len(user_workouts),
            'total_calories': sum(w['calories'] for w in user_workouts),
            'total_time_hours': sum(w['duration'] for w in user_workouts) / 60.0,
            'total_distance': sum(w['distance'] for w in user_workouts)
        }

    # Сортируем по количеству тренировок (по убыванию)
    sorted_users = sorted(user_stats.items(),
                          key=lambda x: x[1]['workout_count'],
                          reverse=True)

    print("\nТОП-3 АКТИВНЫХ ПОЛЬЗОВАТЕЛЕЙ:")
    print("-" * 40)

    for i, (user_id, stats) in enumerate(sorted_users[:3], 1):
        print(f"{i}. {stats['name']} ({stats['fitness_level']}):")
        print(f"   Тренировок: {stats['workout_count']}")
        print(f"   Калорий: {stats['total_calories']}")
        print(f"   Время: {stats['total_time_hours']:.1f} часов")
        print()

    return user_stats


def analyze_workout_types(workouts):
    """
    Анализирует распределение по типам тренировок с сортировкой по минутам
    """
    # Группируем тренировки по типу
    workouts_by_type = defaultdict(list)
    for workout in workouts:
        workouts_by_type[workout['type']].append(workout)

    total_workouts = len(workouts)

    print("\nРАСПРЕДЕЛЕНИЕ ПО ТИПАМ ТРЕНИРОВОК:")
    print("-" * 40)

    # Создаем список для сортировки по средней длительности (по убыванию)
    type_stats = []

    for workout_type, type_workouts in workouts_by_type.items():
        count = len(type_workouts)
        percentage = (count / total_workouts) * 100
        avg_duration = sum(w['duration'] for w in type_workouts) / count
        avg_calories = sum(w['calories'] for w in type_workouts) / count
        avg_distance = sum(w['distance'] for w in type_workouts) / count

        type_stats.append({
            'type': workout_type,
            'count': count,
            'percentage': percentage,
            'avg_duration': avg_duration,
            'avg_calories': avg_calories,
            'avg_distance': avg_distance
        })

    # Сортировка по средней длительности (по убыванию)
    type_stats.sort(key=lambda x: x['avg_duration'], reverse=True)

    # Вывод отсортированных результатов
    for stat in type_stats:
        print(f"{stat['type']}: {stat['count']} тренировок ({stat['percentage']:.1f}%)")
        print(f"  Средняя длительность: {stat['avg_duration']:.0f} мин")
        print(f"  Средние калории: {stat['avg_calories']:.0f} ккал")
        print(f"  Средняя дистанция: {stat['avg_distance']:.1f} км")
        print()

    return workouts_by_type, type_stats


def find_user_workouts(users, workouts, user_name):
    """
    Находит все тренировки пользователя по имени
    """
    # Находим пользователя по имени
    user = next((u for u in users if u['name'].lower() == user_name.lower()), None)

    if user:
        user_workouts = [w for w in workouts if w['user_id'] == user['user_id']]
        return user, user_workouts
    else:
        print(f"Пользователь '{user_name}' не найден")
        return None, []


def analyze_user(user, user_workouts):
    """
    Выполняет детальный анализ тренировок пользователя
    """
    if not user or not user_workouts:
        return

    workout_count = len(user_workouts)
    total_calories = sum(w['calories'] for w in user_workouts)
    total_time_hours = sum(w['duration'] for w in user_workouts) / 60.0
    total_distance = sum(w['distance'] for w in user_workouts)
    avg_calories_per_workout = total_calories / workout_count if workout_count > 0 else 0
    avg_duration_per_workout = sum(w['duration'] for w in user_workouts) / workout_count if workout_count > 0 else 0

    # Находим самый частый тип тренировки
    workout_types = [w['type'] for w in user_workouts]
    most_common_type = Counter(workout_types).most_common(1)[0][0] if workout_types else "нет данных"

    print("\n" + "=" * 50)
    print(f"ДЕТАЛЬНЫЙ АНАЛИЗ ДЛЯ ПОЛЬЗОВАТЕЛЯ: {user['name']}")
    print("=" * 50)
    print(f"Возраст: {user['age']} лет, Вес: {user['weight']} кг")
    print(f"Уровень: {user['fitness_level']}")
    print(f"Тренировок: {workout_count}")
    print(f"Сожжено калорий: {total_calories}")
    print(f"Общее время: {total_time_hours:.1f} часов")
    print(f"Пройдено дистанции: {total_distance:.1f} км")
    print(f"Средние калории за тренировку: {avg_calories_per_workout:.0f}")
    print(f"Средняя длительность тренировки: {avg_duration_per_workout:.0f} мин")
    print(f"Любимый тип тренировки: {most_common_type}")
    print("=" * 50)

    return {
        'workout_count': workout_count,
        'total_calories': total_calories,
        'total_time_hours': total_time_hours,
        'total_distance': total_distance,
        'avg_calories_per_workout': avg_calories_per_workout,
        'avg_duration_per_workout': avg_duration_per_workout,
        'favorite_workout': most_common_type
    }


def plot_average_values(workouts, type_stats):
    """
    Строит график средних значений по типам тренировок
    """
    # Сортируем статистику по средней длительности
    type_stats_sorted = sorted(type_stats, key=lambda x: x['avg_duration'], reverse=False)

    # Создаем данные для графика
    types = [stat['type'] for stat in type_stats_sorted]
    avg_durations = [stat['avg_duration'] for stat in type_stats_sorted]
    avg_calories = [stat['avg_calories'] for stat in type_stats_sorted]
    avg_distances = [stat['avg_distance'] for stat in type_stats_sorted]

    # Нормализуем данные для сравнения (приводим к шкале 0-1)
    def normalize(data):
        min_val = min(data)
        max_val = max(data)
        if max_val - min_val == 0:
            return [0] * len(data)
        return [(x - min_val) / (max_val - min_val) for x in data]

    norm_durations = normalize(avg_durations)
    norm_calories = normalize(avg_calories)
    norm_distances = normalize(avg_distances)

    # Создаем график
    fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(12, 10))

    # График 1: Барчарт с реальными значениями
    x = np.arange(len(types))
    width = 0.25

    bars1 = ax1.bar(x - width, avg_durations, width, label='Средняя длительность (мин)', color='skyblue')
    bars2 = ax1.bar(x, avg_calories, width, label='Средние калории (ккал)', color='lightgreen')
    bars3 = ax1.bar(x + width, avg_distances, width, label='Средняя дистанция (км)', color='salmon')

    ax1.set_xlabel('Тип тренировки')
    ax1.set_ylabel('Значения')
    ax1.set_title('Средние показатели по типам тренировок (отсортировано по длительности)', fontsize=14,
                  fontweight='bold')
    ax1.set_xticks(x)
    ax1.set_xticklabels(types, rotation=45, ha='right')
    ax1.legend()
    ax1.grid(True, alpha=0.3)

    # Добавляем значения на столбцы
    for bars in [bars1, bars2, bars3]:
        for bar in bars:
            height = bar.get_height()
            ax1.text(bar.get_x() + bar.get_width() / 2., height + 0.5,
                     f'{height:.1f}', ha='center', va='bottom', fontsize=8)

    # График 2: Нормализованные значения (для сравнения)
    ax2.plot(types, norm_durations, marker='o', label='Длительность (норм.)', color='skyblue', linewidth=2)
    ax2.plot(types, norm_calories, marker='s', label='Калории (норм.)', color='lightgreen', linewidth=2)
    ax2.plot(types, norm_distances, marker='^', label='Дистанция (норм.)', color='salmon', linewidth=2)

    ax2.set_xlabel('Тип тренировки')
    ax2.set_ylabel('Нормализованные значения (0-1)')
    ax2.set_title('Нормализованные средние показатели (для сравнения)', fontsize=14, fontweight='bold')
    ax2.set_xticks(range(len(types)))
    ax2.set_xticklabels(types, rotation=45, ha='right')
    ax2.legend()
    ax2.grid(True, alpha=0.3)
    ax2.fill_between(range(len(types)), norm_durations, alpha=0.1, color='skyblue')
    ax2.fill_between(range(len(types)), norm_calories, alpha=0.1, color='lightgreen')
    ax2.fill_between(range(len(types)), norm_distances, alpha=0.1, color='salmon')

    plt.tight_layout()
    plt.show()

    # Также построим тепловую карту корреляции
    fig, ax = plt.subplots(figsize=(10, 8))

    # Создаем матрицу данных
    data_matrix = np.array([avg_durations, avg_calories, avg_distances])

    im = ax.imshow(data_matrix, cmap='YlOrRd', aspect='auto')

    # Настраиваем оси
    ax.set_xticks(np.arange(len(types)))
    ax.set_yticks(np.arange(3))
    ax.set_xticklabels(types, rotation=45, ha='right')
    ax.set_yticklabels(['Длительность (мин)', 'Калории (ккал)', 'Дистанция (км)'])

    # Добавляем значения в ячейки
    for i in range(3):
        for j in range(len(types)):
            text = ax.text(j, i, f'{data_matrix[i, j]:.1f}',
                           ha="center", va="center", color="black", fontweight='bold')

    ax.set_title("Тепловая карта средних значений по типам тренировок", fontsize=14, fontweight='bold')
    fig.colorbar(im, ax=ax, label='Значение')
    plt.tight_layout()
    plt.show()


def visualize_data(users, workouts, user_stats, workouts_by_type, type_stats):
    """
    Создает визуализации данных
    """
    # 1. Круговая диаграмма типов тренировок
    plt.figure(figsize=(16, 12))

    plt.subplot(2, 3, 1)
    workout_types = [stat['type'] for stat in type_stats]
    workout_counts = [stat['count'] for stat in type_stats]
    colors = plt.cm.Set3(np.arange(len(workout_types)))

    plt.pie(workout_counts, labels=workout_types, autopct='%1.1f%%',
            colors=colors, startangle=90, textprops={'fontsize': 9})
    plt.title('Распределение по типам тренировок', fontsize=12, fontweight='bold')
    plt.axis('equal')

    # 2. Столбчатая диаграмма активности пользователей (сортировка по минутам)
    plt.subplot(2, 3, 2)
    user_names = [user['name'] for user in users]
    user_workout_counts = []
    user_total_minutes = []

    for user in users:
        user_workouts = [w for w in workouts if w['user_id'] == user['user_id']]
        user_workout_counts.append(len(user_workouts))
        user_total_minutes.append(sum(w['duration'] for w in user_workouts))

    # Сортировка пользователей по общему количеству минут (по убыванию)
    sorted_data = sorted(zip(user_names, user_workout_counts, user_total_minutes),
                         key=lambda x: x[2], reverse=True)
    sorted_names = [item[0] for item in sorted_data]
    sorted_counts = [item[1] for item in sorted_data]
    sorted_minutes = [item[2] for item in sorted_data]

    x = np.arange(len(sorted_names))
    bars = plt.bar(x, sorted_minutes, color=plt.cm.viridis(np.linspace(0, 1, len(sorted_names))))
    plt.title('Общее время тренировок (минуты)', fontsize=12, fontweight='bold')
    plt.xlabel('Пользователи')
    plt.ylabel('Минуты тренировок')
    plt.xticks(x, sorted_names, rotation=45, ha='right', fontsize=9)

    # Добавляем значения на столбцы
    for i, (bar, count, minutes) in enumerate(zip(bars, sorted_counts, sorted_minutes)):
        height = bar.get_height()
        plt.text(bar.get_x() + bar.get_width() / 2., height + 0.5,
                 f'{int(minutes)} мин\n({count} тр.)', ha='center', va='bottom', fontsize=8)

    # 3. Столбчатая диаграмма эффективности тренировок (калории/минута)
    plt.subplot(2, 3, 3)
    efficiency_scores = []

    for user in users:
        user_workouts = [w for w in workouts if w['user_id'] == user['user_id']]
        if user_workouts:
            total_calories = sum(w['calories'] for w in user_workouts)
            total_minutes = sum(w['duration'] for w in user_workouts)
            efficiency = total_calories / total_minutes if total_minutes > 0 else 0
        else:
            efficiency = 0
        efficiency_scores.append(efficiency)

    # Сортировка по эффективности (по убыванию)
    sorted_efficiency = sorted(zip(user_names, efficiency_scores),
                               key=lambda x: x[1], reverse=True)
    sorted_names_eff = [item[0] for item in sorted_efficiency]
    sorted_scores = [item[1] for item in sorted_efficiency]

    x = np.arange(len(sorted_names_eff))
    bars = plt.bar(x, sorted_scores, color=plt.cm.plasma(np.linspace(0, 1, len(sorted_names_eff))))
    plt.title('Эффективность тренировок (калории/минуту)', fontsize=12, fontweight='bold')
    plt.xlabel('Пользователи')
    plt.ylabel('Калории/минуту')
    plt.xticks(x, sorted_names_eff, rotation=45, ha='right', fontsize=9)

    for bar, score in zip(bars, sorted_scores):
        height = bar.get_height()
        plt.text(bar.get_x() + bar.get_width() / 2., height + 0.01,
                 f'{score:.2f}', ha='center', va='bottom', fontsize=8)

    # 4. Сравнительная диаграмма пользователей
    plt.subplot(2, 3, 4)

    # Собираем несколько показателей для сравнения
    metrics_names = ['Тренировки', 'Минуты', 'Калории', 'Дистанция']
    metrics_data = []

    for user in users:
        user_workouts = [w for w in workouts if w['user_id'] == user['user_id']]
        metrics_data.append([
            len(user_workouts),
            sum(w['duration'] for w in user_workouts),
            sum(w['calories'] for w in user_workouts),
            sum(w['distance'] for w in user_workouts)
        ])

    # Нормализуем данные для сравнения
    metrics_data = np.array(metrics_data)
    normalized_data = (metrics_data - metrics_data.min(axis=0)) / (
                metrics_data.max(axis=0) - metrics_data.min(axis=0) + 1e-10)

    x = np.arange(len(user_names))
    width = 0.2

    for i in range(4):
        plt.bar(x + i * width, normalized_data[:, i], width, label=metrics_names[i])

    plt.title('Сравнительный анализ пользователей (нормализованные значения)', fontsize=12, fontweight='bold')
    plt.xlabel('Пользователи')
    plt.ylabel('Нормализованные значения')
    plt.xticks(x + 1.5 * width, user_names, rotation=45, ha='right', fontsize=9)
    plt.legend(loc='upper right', fontsize=8)

    # 5. График средней длительности по типам тренировок
    plt.subplot(2, 3, 5)

    # Сортируем типы тренировок по средней длительности
    sorted_by_duration = sorted(type_stats, key=lambda x: x['avg_duration'], reverse=True)
    types_sorted = [stat['type'] for stat in sorted_by_duration]
    durations_sorted = [stat['avg_duration'] for stat in sorted_by_duration]
    calories_sorted = [stat['avg_calories'] for stat in sorted_by_duration]

    x = np.arange(len(types_sorted))
    bars = plt.bar(x, durations_sorted, color=plt.cm.coolwarm(np.linspace(0, 1, len(types_sorted))))
    plt.title('Средняя длительность по типам тренировок', fontsize=12, fontweight='bold')
    plt.xlabel('Тип тренировки')
    plt.ylabel('Средняя длительность (минуты)')
    plt.xticks(x, types_sorted, rotation=45, ha='right', fontsize=9)

    for bar, duration, calories in zip(bars, durations_sorted, calories_sorted):
        height = bar.get_height()
        plt.text(bar.get_x() + bar.get_width() / 2., height + 0.5,
                 f'{duration:.0f} мин\n{calories:.0f} ккал',
                 ha='center', va='bottom', fontsize=8)

    # 6. Распределение интенсивности тренировок
    plt.subplot(2, 3, 6)

    intensities = [w['intensity'] for w in workouts]
    intensity_counts = Counter(intensities)

    labels = list(intensity_counts.keys())
    values = list(intensity_counts.values())

    # Сортируем по количеству
    sorted_intensity = sorted(zip(labels, values), key=lambda x: x[1], reverse=True)
    labels_sorted = [item[0] for item in sorted_intensity]
    values_sorted = [item[1] for item in sorted_intensity]

    colors_intensity = ['#FF6B6B', '#FFD166', '#06D6A0']  # Красный для высокой, желтый для средней, зеленый для низкой

    # Находим правильный порядок цветов
    color_map = {'высокая': '#FF6B6B', 'средняя': '#FFD166', 'низкая': '#06D6A0'}
    colors_sorted = [color_map[label] for label in labels_sorted]

    bars = plt.bar(labels_sorted, values_sorted, color=colors_sorted)
    plt.title('Распределение по интенсивности тренировок', fontsize=12, fontweight='bold')
    plt.xlabel('Интенсивность')
    plt.ylabel('Количество тренировок')

    for bar, value in zip(bars, values_sorted):
        height = bar.get_height()
        plt.text(bar.get_x() + bar.get_width() / 2., height + 0.1,
                 f'{value}', ha='center', va='bottom', fontsize=10)

    plt.tight_layout()
    plt.show()


def main():
    """
    Основная функция для выполнения всех задач
    """
    print("=" * 60)
    print("АНАЛИЗ ДАННЫХ ФИТНЕС-ТРЕКЕРА")
    print("=" * 60)

    # Загрузка данных
    print("\n1. ЗАГРУЗКА ДАННЫХ")
    print("-" * 30)
    users = load_users_data('users.xml')
    workouts = load_workouts_data('workouts.xml')

    if not users or not workouts:
        print("Не удалось загрузить данные. Проверьте файлы users.xml и workouts.xml")
        return

    # Задача 1: Общая статистика
    print("\n2. ОБЩАЯ СТАТИСТИКА")
    print("-" * 30)
    stats = get_stats(users, workouts)

    # Задача 2: Анализ данных
    print("\n3. АНАЛИЗ ДАННЫХ")
    print("-" * 30)

    # ТОП-3 активных пользователей
    user_stats = analyze_user_activity(users, workouts)

    # Распределение по типам тренировок
    workouts_by_type, type_stats = analyze_workout_types(workouts)

    # Детальный анализ для конкретного пользователя (пример)
    user_name = "Борис"
    user, user_workouts = find_user_workouts(users, workouts, user_name)

    if user:
        analyze_user(user, user_workouts)

    # Задача 3: Визуализация данных
    print("\n4. ВИЗУАЛИЗАЦИЯ ДАННЫХ")
    print("-" * 30)
    print("Строим диаграммы...")

    # Основные графики
    visualize_data(users, workouts, user_stats, workouts_by_type, type_stats)

    # Дополнительный график средних значений
    print("\n5. ГРАФИК СРЕДНИХ ЗНАЧЕНИЙ")
    print("-" * 30)
    plot_average_values(workouts, type_stats)

    # Дополнительный анализ: статистика по месяцам с сортировкой
    print("\n6. ДОПОЛНИТЕЛЬНЫЙ АНАЛИЗ")
    print("-" * 30)

    # Анализ тренировок по месяцам с сортировкой по минутам
    if workouts:
        # Создаем DataFrame для удобного анализа
        df = pd.DataFrame(workouts)
        df['date'] = pd.to_datetime(df['date'])
        df['month'] = df['date'].dt.month
        df['month_name'] = df['date'].dt.strftime('%B')

        # Группируем по месяцам
        monthly_stats = df.groupby(['month', 'month_name']).agg({
            'duration': ['sum', 'mean', 'count'],
            'calories': 'sum',
            'distance': 'sum'
        }).round(1)

        monthly_stats.columns = ['total_minutes', 'avg_minutes', 'workout_count', 'total_calories', 'total_distance']
        monthly_stats = monthly_stats.reset_index()

        # Сортируем по общему количеству минут (по убыванию)
        monthly_stats = monthly_stats.sort_values('total_minutes', ascending=False)

        print("Активность по месяцам (отсортировано по времени тренировок):")
        print("-" * 60)
        for _, row in monthly_stats.iterrows():
            print(f"{row['month_name']}:")
            print(f"  Тренировок: {row['workout_count']}")
            print(f"  Всего минут: {row['total_minutes']}")
            print(f"  Средняя длительность: {row['avg_minutes']:.0f} мин")
            print(f"  Всего калорий: {row['total_calories']}")
            print(f"  Всего дистанции: {row['total_distance']:.1f} км")
            print()

    print("\n" + "=" * 60)
    print("АНАЛИЗ ЗАВЕРШЕН УСПЕШНО!")
    print("=" * 60)


if __name__ == "__main__":
    main()