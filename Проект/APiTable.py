import requests
import pandas as pd
import matplotlib.pyplot as plt
import json
from datetime import datetime
import io


class WeatherVisualCrossing:
    def __init__(self, api_key):
        self.api_key = api_key
        self.base_url = "https://weather.visualcrossing.com/VisualCrossingWebServices/rest/services/retrievebulkdataset"

    def get_weather_data_json(self, task_id):
        """Получаем данные в JSON формате"""
        url = f"{self.base_url}?&key={self.api_key}&taskId={task_id}&zip=false"

        try:
            response = requests.get(url)
            response.raise_for_status()

            # Пытаемся разобрать JSON
            data = response.json()
            return data
        except requests.exceptions.RequestException as e:
            print(f"Ошибка при запросе: {e}")
            return None
        except json.JSONDecodeError as e:
            print(f"Ошибка при разборе JSON: {e}")
            print(f"Ответ сервера: {response.text[:500]}...")
            return None

    def get_weather_data_zip(self, task_id):
        """Получаем данные в ZIP формате"""
        url = f"{self.base_url}?&key={self.api_key}&taskId={task_id}&zip=true"

        try:
            response = requests.get(url)
            response.raise_for_status()

            # Сохраняем ZIP файл
            with open('weather_data.zip', 'wb') as f:
                f.write(response.content)
            print("ZIP файл сохранен как 'weather_data.zip'")

            return 'weather_data.zip'
        except requests.exceptions.RequestException as e:
            print(f"Ошибка при запросе: {e}")
            return None


def create_sample_weather_data():
    """Создаем примерные погодные данные если API недоступно"""
    dates = pd.date_range(start='2024-01-01', end='2024-01-30', freq='D')

    # Генерируем реалистичные погодные данные
    base_temp = 15
    temperatures = [base_temp + 10 * abs((i % 20 - 10) / 10) + np.random.normal(0, 2) for i in range(len(dates))]
    humidity = [60 + 20 * np.sin(i * 0.3) + np.random.normal(0, 5) for i in range(len(dates))]
    precipitation = [max(0, np.random.exponential(2) - 1) for i in range(len(dates))]

    return pd.DataFrame({
        'datetime': dates,
        'temp': temperatures,
        'humidity': humidity,
        'precip': precipitation
    })


def plot_weather_data(df, parameter='temp'):
    """Строим график погодных данных"""
    if df is None or df.empty:
        print("Нет данных для построения графика")
        return

    # Настройки графиков в зависимости от параметра
    config = {
        'temp': {'title': 'Температура по дням', 'ylabel': 'Температура (°C)', 'color': 'red'},
        'humidity': {'title': 'Влажность по дням', 'ylabel': 'Влажность (%)', 'color': 'blue'},
        'precip': {'title': 'Осадки по дням', 'ylabel': 'Осадки (mm)', 'color': 'green'}
    }

    if parameter not in config:
        print(f"Параметр {parameter} не поддерживается. Используйте: temp, humidity, precip")
        return

    plt.figure(figsize=(14, 8))

    # Основной график
    plt.subplot(2, 1, 1)
    plt.plot(df['datetime'], df[parameter],
             marker='o', linewidth=2, markersize=4,
             color=config[parameter]['color'], label=config[parameter]['ylabel'])

    plt.title(config[parameter]['title'], fontsize=16, fontweight='bold')
    plt.ylabel(config[parameter]['ylabel'])
    plt.grid(True, alpha=0.3)
    plt.legend()
    plt.xticks(rotation=45)

    # Дополнительная информация
    plt.subplot(2, 1, 2)
    parameters_to_plot = [p for p in ['temp', 'humidity', 'precip'] if p != parameter]

    for i, param in enumerate(parameters_to_plot):
        plt.plot(df['datetime'], df[param],
                 marker='s', linewidth=1, markersize=3,
                 label=config[param]['ylabel'], alpha=0.7)

    plt.title('Дополнительные параметры погоды', fontsize=14)
    plt.ylabel('Значения')
    plt.xlabel('Дата')
    plt.grid(True, alpha=0.3)
    plt.legend()
    plt.xticks(rotation=45)

    plt.tight_layout()
    plt.show()

    # Выводим статистику
    print(f"\nСтатистика для {config[parameter]['title']}:")
    print(f"Среднее: {df[parameter].mean():.2f}")
    print(f"Максимум: {df[parameter].max():.2f}")
    print(f"Минимум: {df[parameter].min():.2f}")
    print(f"Стандартное отклонение: {df[parameter].std():.2f}")


# Основной код
if __name__ == "__main__":
    # Ваши данные
    API_KEY = "UUBKQCTK22ZVEUAXRLSENNWPN"
    TASK_ID = "a7423dec518dce39833606cb5176e9e8"

    # Создаем экземпляр класса
    weather_api = WeatherVisualCrossing(API_KEY)

    # Пытаемся получить данные через API
    print("Пытаемся получить данные через API...")
    data = weather_api.get_weather_data_json(TASK_ID)

    df = None

    if data:
        print("Данные получены успешно!")
        print("Структура данных:")
        print(json.dumps(data, indent=2)[:1000] + "..." if len(json.dumps(data)) > 1000 else json.dumps(data, indent=2))

        # Здесь нужно адаптировать код под структуру ваших данных
        # Создаем DataFrame из полученных данных
        # Это пример - замените на реальную обработку ваших данных
        try:
            # Предполагаем, что данные имеют locations с данными по дням
            if 'locations' in data:
                # Берем первую локацию
                location_name = list(data['locations'].keys())[0]
                location_data = data['locations'][location_name]

                # Извлекаем данные по дням
                weather_records = []
                for date_str, day_data in location_data.items():
                    if 'values' in day_data and len(day_data['values']) > 0:
                        daily_data = day_data['values'][0]
                        daily_data['datetime'] = pd.to_datetime(date_str)
                        weather_records.append(daily_data)

                df = pd.DataFrame(weather_records)
                print(f"Успешно создан DataFrame с {len(df)} записями")

        except Exception as e:
            print(f"Ошибка при обработке данных: {e}")
            df = None

    # Если API не сработал, используем примерные данные
    if df is None or df.empty:
        print("\nИспользуем примерные данные...")
        import numpy as np

        df = create_sample_weather_data()

    # Строим графики для разных параметров
    parameters = ['temp', 'humidity', 'precip']

    for param in parameters:
        print(f"\n{'=' * 50}")
        print(f"Построение графика для параметра: {param}")
        print(f"{'=' * 50}")
        plot_weather_data(df, param)

        # Спрашиваем пользователя, продолжать ли
        if param != parameters[-1]:
            continue_input = input("\nНажмите Enter для следующего графика или 'q' для выхода: ")
            if continue_input.lower() == 'q':
                break

    # Дополнительно: попробуем получить ZIP файл
    print("\nПытаемся получить данные в ZIP формате...")
    zip_file = weather_api.get_weather_data_zip(TASK_ID)
    if zip_file:
        print(f"ZIP файл получен: {zip_file}")