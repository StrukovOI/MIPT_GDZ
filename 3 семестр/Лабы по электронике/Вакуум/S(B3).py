import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

def plot_turbopump_performance(csv_file):
    """
    Построение графика зависимости S(л/с) от P_B3(Торр)
    """
    # Чтение данных из CSV
    df = pd.read_csv(csv_file, 
                    sep=';',           # разделитель - точка с запятой
                    decimal=',',       # десятичный разделитель - запятая
                    header=None,       # нет заголовка
                    names=['P_B3', 'S'])  # названия столбцов
    
    print(f"Загружено {len(df)} точек")
    print("Первые 5 строк данных:")
    print(df.head())
    
    # Преобразуем в numpy массивы
    P_B3 = df['P_B3'].values
    S = df['S'].values
    
    # Создаем график
    plt.figure(figsize=(10, 6))
    
    plt.plot(P_B3, S, 'bo-', markersize=3, linewidth=1)
    plt.xlabel(r'Давление $B_3$, Торр', fontsize=12)
    plt.ylabel('Быстрота действия S, л/с', fontsize=12)
    # plt.title(r'Зависимость производительности турбомолекулярного насоса от давления $В_3$', fontsize=14)
    plt.grid(True, alpha=0.3)
    
    # Добавляем статистику на график
    # avg_S = np.mean(S)
    # plt.axhline(y=avg_S, color='r', linestyle='--', alpha=0.7, 
    #            label=f'Среднее: {avg_S:.1f} л/с')
    # plt.legend()
    
    plt.tight_layout()
    plt.show()
    
    # Выводим статистику
    # print(f"\nСтатистика:")
    # print(f"Диапазон давлений: {P_B3.min():.2e} - {P_B3.max():.2e} Торр")
    # print(f"Диапазон S: {S.min():.1f} - {S.max():.1f} л/с")
    # print(f"Средняя S: {avg_S:.1f} л/с")
    # print(f"Медиана S: {np.median(S):.1f} л/с")

# Основная программа
if __name__ == "__main__":
    csv_file = r"C:\Users\olezh\OneDrive\Рабочий стол\Лабы\Электроника\Вакуум\S(B3).csv"
    plot_turbopump_performance(csv_file)