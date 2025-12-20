import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

def read_flow_data_semicolon(csv_file):
    """
    Чтение данных потока через диафрагму с разделителем точка с запятой
    """
    print("Чтение данных с разделителем ';'...")
    
    try:
        # Читаем с разделителем точка с запятой и десятичной запятой
        df = pd.read_csv(csv_file, 
                        sep=';',           # разделитель - точка с запятой
                        decimal=',',       # десятичный разделитель - запятая
                        header=None,       # нет заголовка
                        names=['Time', 'Flow'])  # названия столбцов
        
        print(f"Успешно прочитано {len(df)} строк")
        print("Первые 5 строк данных:")
        print(df.head())
        
        # Проверяем, что данные прочитаны правильно
        if df['Time'].isna().any() or df['Flow'].isna().any():
            print("Обнаружены пропущенные значения. Пробуем альтернативный метод...")
            return read_flow_data_manual(csv_file)
        
        return df['Time'].values, df['Flow'].values
        
    except Exception as e:
        print(f"Ошибка при чтении с разделителем ';': {e}")
        return read_flow_data_manual(csv_file)

def read_flow_data_manual(csv_file):
    """
    Ручное чтение данных для сложных случаев
    """
    print("Ручное чтение данных...")
    times = []
    flows = []
    
    with open(csv_file, 'r', encoding='utf-8') as f:
        lines = f.readlines()
        print(f"Найдено {len(lines)} строк в файле")
        
        for i, line in enumerate(lines):
            line = line.strip()
            if not line:
                continue
                
            # Разделяем по точке с запятой
            parts = line.split(';')
            if len(parts) >= 2:
                try:
                    # Преобразуем оба числа, заменяя запятые на точки
                    time_val = float(parts[0].replace(',', '.'))
                    flow_val = float(parts[1].replace(',', '.'))
                    times.append(time_val)
                    flows.append(flow_val)
                except ValueError as e:
                    print(f"Ошибка преобразования в строке {i}: {line} - {e}")
            else:
                print(f"Пропущена строка {i}: недостаточно частей - {parts}")
    
    if times and flows:
        print(f"Ручное чтение: успешно загружено {len(times)} точек")
        return np.array(times), np.array(flows)
    else:
        print("Не удалось извлечь данные из файла")
        return None, None

def plot_flow_vs_time_semicolon(csv_file):
    """
    Построение графика зависимости потока через диафрагму от времени
    для данных с разделителем точка с запятой
    """
    # Чтение данных
    time, flow = read_flow_data_semicolon(csv_file)
    
    if time is None or flow is None:
        print("Не удалось загрузить данные. Проверьте формат файла.")
        return
    
    print(f"\nУспешно загружено {len(time)} точек")
    print(f"Диапазон времени: {time.min():.1f} - {time.max():.1f} с")
    print(f"Диапазон потока: {flow.min():.2e} - {flow.max():.2e} Торр·л/с")
    
    # Проверяем, есть ли временной тренд (увеличивается/уменьшается время)
    if len(time) > 1 and time[0] > time[-1]:
        print("Время убывает - сортируем по возрастанию")
        # Сортируем по времени
        sort_idx = np.argsort(time)
        time = time[sort_idx]
        flow = flow[sort_idx]
    
    # Статистика
    flow_mean = flow.mean()
    flow_std = flow.std()
    flow_median = np.median(flow)
    
    print(f"\nСтатистика потока:")
    print(f"Средний поток: {flow_mean:.2e} Торр·л/с")
    print(f"Медиана потока: {flow_median:.2e} Торр·л/с")
    print(f"Стандартное отклонение: {flow_std:.2e} Торр·л/с")
    print(f"Относительное отклонение: {(flow_std/flow_mean*100):.1f}%")
    
    # Создаем график
    plt.figure(figsize=(12, 8))
    
    # Основной график
    # plt.subplot(2, 1, 1)
    plt.plot(time, flow, 'b-', linewidth=1, label='Поток через диафрагму')
    plt.xlabel('Время, с')
    plt.ylabel('Поток Q, Торр·л/с')
    # plt.title('Зависимость потока через диафрагму от времени', fontsize=14)
    plt.grid(True, alpha=0.3)
    
    # # Добавляем горизонтальную линию для среднего значения
    # plt.axhline(y=flow_mean, color='r', linestyle='--', alpha=0.7, 
    #            label=f'Среднее: {flow_mean:.2e} Торр·л/с')
    # plt.axhline(y=flow_mean + flow_std, color='r', linestyle=':', alpha=0.5, 
    #            label=f'±1σ: {flow_std:.2e} Торр·л/с')
    # plt.axhline(y=flow_mean - flow_std, color='r', linestyle=':', alpha=0.5)
    # plt.legend()
    
    # # Гистограмма распределения потоков
    # plt.subplot(2, 1, 2)
    # plt.hist(flow, bins=50, alpha=0.7, color='green', edgecolor='black')
    # plt.xlabel('Поток Q, Торр·л/с')
    # plt.ylabel('Частота')
    # plt.title('Распределение значений потока', fontsize=14)
    # plt.grid(True, alpha=0.3)
    
    # # Добавляем вертикальные линии для статистики
    # plt.axvline(flow_mean, color='r', linestyle='--', label=f'Среднее: {flow_mean:.2e}')
    # plt.axvline(flow_median, color='orange', linestyle='--', label=f'Медиана: {flow_median:.2e}')
    # plt.legend()
    
    plt.tight_layout()
    plt.show()
    
    # Анализ стабильности потока
    print(f"\nАнализ стабильности потока:")
    
    # Разделяем данные на сегменты для анализа тренда
    n_segments = min(5, len(flow) // 10)  # не более 5 сегментов, минимум 10 точек на сегмент
    if n_segments > 1:
        segment_size = len(flow) // n_segments
        segment_means = []
        
        for i in range(n_segments):
            start_idx = i * segment_size
            end_idx = (i + 1) * segment_size if i < n_segments - 1 else len(flow)
            segment_mean = flow[start_idx:end_idx].mean()
            segment_means.append(segment_mean)
            print(f"Сегмент {i+1}: средний поток = {segment_mean:.2e} Торр·л/с")
        
        # Проверяем наличие тренда
        segment_change = (segment_means[-1] - segment_means[0]) / segment_means[0] * 100
        print(f"Изменение потока за время измерения: {segment_change:.1f}%")
        
        if abs(segment_change) > 5:
            print("Обнаружен значительный тренд в данных!")
        else:
            print("Поток стабилен в течение времени измерения.")
    
    # Сохранение результатов
    # save_choice = input("\nСохранить график и данные? (y/n): ").lower()
    # if save_choice == 'y':
    #     filename = input("Введите имя файла (без расширения): ")
        
    #     # Сохраняем обработанные данные
    #     df = pd.DataFrame({'Time_s': time, 'Flow_Torr_l_s': flow})
    #     df.to_csv(f'{filename}_data.csv', index=False, float_format='%.8e')
    #     print(f"Данные сохранены в {filename}_data.csv")
        
    #     # Сохраняем график
    #     plt.figure(figsize=(10, 6))
    #     plt.plot(time, flow, 'b-', linewidth=1, label='Поток через диафрагму')
    #     plt.axhline(y=flow_mean, color='r', linestyle='--', alpha=0.7, 
    #                label=f'Среднее: {flow_mean:.2e} Торр·л/с')
    #     plt.axhline(y=flow_mean + flow_std, color='r', linestyle=':', alpha=0.5)
    #     plt.axhline(y=flow_mean - flow_std, color='r', linestyle=':', alpha=0.5)
    #     plt.xlabel('Время t, с')
    #     plt.ylabel('Поток Q, Торр·л/с')
    #     plt.title('Зависимость потока через диафрагму от времени')
    #     plt.grid(True, alpha=0.3)
    #     plt.legend()
    #     plt.savefig(f'{filename}.png', dpi=300, bbox_inches='tight')
    #     plt.savefig(f'{filename}.pdf', bbox_inches='tight')
    #     print(f"График сохранен как {filename}.png и {filename}.pdf")
        
    #     # Сохраняем отчет
    #     with open(f'{filename}_report.txt', 'w', encoding='utf-8') as f:
    #         f.write(f"ОТЧЕТ ПО РЕЗУЛЬТАТАМ ИЗМЕРЕНИЯ ПОТОКА\n")
    #         f.write("=" * 50 + "\n")
    #         f.write(f"Общее количество точек: {len(time)}\n")
    #         f.write(f"Время измерения: от {time.min():.1f} до {time.max():.1f} с\n")
    #         f.write(f"Длительность: {time.max() - time.min():.1f} с\n\n")
    #         f.write("СТАТИСТИКА ПОТОКА:\n")
    #         f.write(f"Средний поток: {flow_mean:.2e} Торр·л/с\n")
    #         f.write(f"Медиана потока: {flow_median:.2e} Торр·л/с\n")
    #         f.write(f"Стандартное отклонение: {flow_std:.2e} Торр·л/с\n")
    #         f.write(f"Относительное отклонение: {flow_std/flow_mean*100:.1f}%\n\n")
        
    #     print(f"Отчет сохранен в {filename}_report.txt")

# Создаем тестовый файл с правильным форматом (точка с запятой)
def create_test_file_semicolon():
    """Создание тестового файла с данными в формате с разделителем ';'"""
    test_data = """5640,25;0,000764348
5640,78;0,000764348
5641,36;0,000773448
5641,89;0,000764348
5642,45;0,000773448
5643,03;0,000773448
5643,61;0,000764348
5644,13;0,000773448
5644,69;0,000773448
5645,27;0,000773448
5645,85;0,000773448
5646,42;0,000773448
5646,95;0,000773448
5647,53;0,000773448
5648,11;0,000773448
5648,69;0,000773448
5649,21;0,000773448
5649,77;0,000773448
5650,35;0,000773448
5650,93;0,000773448"""
    
    with open('test_flow_data_semicolon.csv', 'w', encoding='utf-8') as f:
        f.write(test_data)
    return 'test_flow_data_semicolon.csv'

# Основная программа
if __name__ == "__main__":
    print("Программа для построения зависимости потока через диафрагму от времени")
    print("Формат данных: время;поток (разделитель - точка с запятой)")
    print("Десятичный разделитель: запятая")
    print("=" * 60)
    
    csv_file = r"C:\Users\olezh\OneDrive\Рабочий стол\Лабы\Электроника\Вакуум\Поток через диафрагму.csv"
    
    if not csv_file:
        csv_file = create_test_file_semicolon()
        print(f"Создан тестовый файл: {csv_file}")
    
    plot_flow_vs_time_semicolon(csv_file)