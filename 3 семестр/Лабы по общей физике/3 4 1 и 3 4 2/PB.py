import matplotlib.pyplot as plt
import numpy as np
from scipy import stats

# Данные для графита
B2_graphite = np.array([0.7885, 0.7067, 0.6199, 0.5302, 0.4635, 0.3864, 
                       0.3031, 0.2243, 0.1481, 0.0876, 0.0442, 0.0219, 
                       0.0035, 0.0000])
dP_graphite = np.array([0.00, 39.24, 78.48, 127.53, 166.77, 215.82, 
                       274.68, 323.73, 382.59, 431.64, 461.07, 480.69, 
                       490.50, 490.50])

# Данные для вольфрама
B2_tungsten = np.array([0.794, 0.639, 0.500, 0.386, 0.284, 0.197, 
                       0.126, 0.086, 0.043, 0.023, 0.000])
dP_tungsten = np.array([0.00, 225.63, 470.88, 706.32, 931.95, 1128.15, 
                       1314.54, 1393.02, 1510.74, 1569.60, 1628.46])

# Данные для меди
B2_copper = np.array([0.794, 0.639, 0.500, 0.386, 0.284, 0.195, 
                     0.126, 0.069, 0.022, 0.005, 0.000])
dP_copper = np.array([0.00, 29.43, 58.86, 88.29, 117.72, 147.15, 
                     166.77, 186.39, 206.01, 215.82, 215.82])

# Данные для алюминия
B2_aluminum = np.array([0.794, 0.643, 0.513, 0.390, 0.293, 0.208, 
                       0.139, 0.086, 0.032, 0.008, 0.000])
dP_aluminum = np.array([0.00, 58.86, 127.53, 196.20, 264.87, 323.73, 
                       382.59, 412.02, 461.07, 490.50, 490.50])

# Погрешности (одинаковые для всех материалов)
dB2 = 0.005  # погрешность B²
d_dP = 10    # погрешность ΔP

# Создание графика
plt.figure(figsize=(12, 8))

# Функция для аппроксимации и построения
def plot_with_fit(B2, dP, label, color, marker, point_alpha=0.7, line_alpha=1.0):
    # Аппроксимирующая прямая (линейная регрессия)
    slope, intercept, r_value, p_value, std_err = stats.linregress(B2, dP)
    
    # Создаем более темный оттенок для линии
    line_color = color
    point_color = color
    
    # Построение экспериментальных точек с погрешностями
    plt.errorbar(B2, dP, xerr=dB2, yerr=d_dP, fmt=marker, color=point_color, 
                 capsize=3, capthick=1, markersize=4, label=label, 
                 alpha=point_alpha, markeredgewidth=0.5)
    
    # Построение аппроксимирующей прямой
    B2_fit = np.linspace(min(B2), max(B2), 100)
    dP_fit = slope * B2_fit + intercept
    plt.plot(B2_fit, dP_fit, color=line_color, linestyle='-', linewidth=2, 
             alpha=line_alpha)
    
    return slope, intercept

# Определяем цвета с разными оттенками
graphite_color = '#1f77b4'  # синий
tungsten_color = '#d62728'  # красный
copper_color = '#2ca02c'    # зеленый
aluminum_color = '#9467bd'  # фиолетовый

# Построение графиков для всех материалов с разными оттенками
slope_graphite = plot_with_fit(B2_graphite, dP_graphite, 'Графит', 
                              graphite_color, 'o', point_alpha=0.7, line_alpha=0.9)
slope_tungsten = plot_with_fit(B2_tungsten, dP_tungsten, 'Вольфрам', 
                              tungsten_color, 's', point_alpha=0.7, line_alpha=0.9)
slope_copper = plot_with_fit(B2_copper, dP_copper, 'Медь', 
                            copper_color, '^', point_alpha=0.7, line_alpha=0.9)
slope_aluminum = plot_with_fit(B2_aluminum, dP_aluminum, 'Алюминий', 
                              aluminum_color, 'D', point_alpha=0.7, line_alpha=0.9)

# Настройки графика
plt.xlabel('B², Тл²', fontsize=14)
plt.ylabel('ΔP, Н·10⁻⁶', fontsize=14)
plt.title('Зависимость ΔP от B² для различных материалов', fontsize=16)
plt.grid(True, linestyle='--', alpha=0.7)
plt.legend(fontsize=12, loc='best')

# Установка пределов осей для лучшего отображения
plt.xlim(-0.05, 0.85)
plt.ylim(-50, 1800)

# Добавление сетки
plt.minorticks_on()
plt.grid(True, which='major', linestyle='-', alpha=0.5)
plt.grid(True, which='minor', linestyle=':', alpha=0.3)

plt.tight_layout()
plt.show()

# Вывод угловых коэффициентов
print("Угловые коэффициенты аппроксимирующих прямых:")
print(f"Графит: {slope_graphite[0]:.1f}")
print(f"Вольфрам: {slope_tungsten[0]:.1f}")
print(f"Медь: {slope_copper[0]:.1f}")
print(f"Алюминий: {slope_aluminum[0]:.1f}")