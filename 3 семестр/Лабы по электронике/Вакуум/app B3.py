import pandas as pd
import matplotlib.pyplot as plt

def plot_pressure_comparison(csv_file):
    """
    Построение графика сравнения действительного и аппроксимированного давления
    """
    # Чтение данных из CSV
    df = pd.read_csv(csv_file, sep=';', decimal=',', header=None, 
                    names=['Time', 'P_measured', 'P_approximated'])
    
    # Извлечение данных
    time = df['Time'].values
    p_measured = df['P_measured'].values
    p_approximated = df['P_approximated'].values
    
    # Построение графика
    plt.figure(figsize=(10, 6))
    
    # График в линейном масштабе
    # plt.subplot(1, 2, 1)
    plt.plot(time, p_measured, 'b-', linewidth=1, label='Измеренное давление')
    plt.plot(time, p_approximated, 'r--', linewidth=1, label='Аппроксимированное давление')
    plt.xlabel('Время, с')
    plt.ylabel('Давление, Торр')
    # plt.title('Сравнение давлений (линейная шкала)')
    plt.legend()
    plt.grid(True, alpha=0.3)
    
    # # График в логарифмическом масштабе по Y
    # plt.subplot(1, 2, 2)
    # plt.semilogy(time, p_measured, 'b-', linewidth=1, label='Измеренное давление')
    # plt.semilogy(time, p_approximated, 'r--', linewidth=1, label='Аппроксимированное давление')
    # plt.xlabel('Время, с')
    # plt.ylabel('Давление, Торр')
    # plt.title('Сравнение давлений (логарифмическая шкала)')
    # plt.legend()
    # plt.grid(True, alpha=0.3)
    
    plt.tight_layout()
    plt.show()
    
    # Вывод статистики
    print(f"Количество точек: {len(time)}")
    print(f"Время: от {time[0]:.1f} до {time[-1]:.1f} с")
    print(f"Измеренное давление: от {p_measured.min():.2e} до {p_measured.max():.2e} Торр")
    print(f"Аппроксимированное давление: от {p_approximated.min():.2e} до {p_approximated.max():.2e} Торр")

# Основная программа
if __name__ == "__main__":
    csv_file = r"C:\Users\olezh\OneDrive\Рабочий стол\Лабы\Электроника\Вакуум\V.csv"
    plot_pressure_comparison(csv_file)