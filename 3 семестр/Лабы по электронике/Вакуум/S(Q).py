import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

def read_data_with_semicolon(csv_file):
    """
    Чтение данных с разделителем точка с запятой и десятичными запятыми
    """
    data = []
    
    with open(csv_file, 'r', encoding='utf-8') as f:
        for line in f:
            line = line.strip()
            if not line or 'B3' in line and 'Torr' in line:  # пропускаем заголовки
                continue
                
            parts = line.split(';')
            if len(parts) >= 2:
                try:
                    p_b3 = float(parts[0].replace(',', '.'))
                    s_val = float(parts[1].replace(',', '.'))
                    data.append((p_b3, s_val))
                except ValueError as e:
                    print(f"Пропущена строка: {line} - ошибка: {e}")
    
    return data

def plot_turbopump_semicolon(csv_file):
    """
    Построение графика для данных с разделителем точка с запятой
    """
    data = read_data_with_semicolon(csv_file)
    
    if not data:
        print("Не удалось загрузить данные")
        return
    
    P_B3, S = zip(*data)
    P_B3 = np.array(P_B3)
    S = np.array(S)
    
    print(f"Загружено {len(P_B3)} точек")
    print(f"Диапазон P_B3: {P_B3.min():.2e} - {P_B3.max():.2e} Торр")
    print(f"Диапазон S: {S.min():.1f} - {S.max():.1f} л/с")
    
    # Создаем график с маленькими точками и соединяющими линиями
    plt.figure(figsize=(10, 6))
    
    # Используем plot с маленькими точками и соединяющими линиями
    plt.plot(P_B3 * 1e6, S, 'bo-', alpha=0.7, linewidth=1, markersize=2, label='Экспериментальные данные')
    
    plt.xlabel('Давление P_B3, мкТорр', fontsize=12)
    plt.ylabel('Быстрота действия S, л/с', fontsize=12)
    plt.title('Характеристика турбомолекулярного насоса', fontsize=14)
    plt.grid(True, alpha=0.3)
    plt.legend()
    
    plt.tight_layout()
    plt.show()

# Основная программа
if __name__ == "__main__":
    print("Программа для обработки данных турбомолекулярного насоса")
    print("=" * 60)
    
    csv_file = r"C:\Users\olezh\OneDrive\Рабочий стол\Лабы\Электроника\Вакуум\S(Q).csv"
    
    plot_turbopump_semicolon(csv_file)