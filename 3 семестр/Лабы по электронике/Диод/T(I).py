import numpy as np
import matplotlib.pyplot as plt
from scipy.optimize import fsolve

# Исходные данные
I_h = np.array([0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9, 1.0, 1.1, 1.2, 1.3, 1.4, 1.5, 1.6, 1.7, 1.8, 1.9, 2.0, 2.1, 2.2, 2.3, 2.4, 2.5, 2.6, 2.7, 2.8, 2.9])
U_h = np.array([0.022, 0.044, 0.0693, 0.0975, 0.13, 0.17, 0.225, 0.29, 0.381, 0.47, 0.656, 0.76, 0.911, 0.974, 1.101, 1.294, 1.389, 1.6, 2.09, 2.26, 2.5, 2.8, 3.03, 3.24, 3.5, 3.78, 4.14, 4.44, 4.66])

# Геометрические параметры
d_wire = 0.15e-3  # диаметр катода в метрах
l_wire = 45e-3    # длина катода в метрах

# Физические параметры
T0 = 300          # комнатная температура в К
alpha = 2.29e-3   # температурный коэффициент сопротивления вольфрама

# Физические константы
sigma = 5.67e-8   # постоянная Стефана-Больцмана Вт/(м²·К⁴)
epsilon = 0.3     # коэффициент излучения вольфрама

# 1. Расчет температуры по изменению сопротивления
# Сопротивление при комнатной температуре (первое измерение)
R0 = U_h[0] / I_h[0]

# Расчет сопротивления для всех точек
R = U_h / I_h

# Расчет температуры по формуле R = R0(1 + alpha*(T - T0))
T_resistance = T0 + (R/R0 - 1) / alpha

# 2. Расчет температуры по уравнению энергетического баланса
# Площадь поверхности катода (цилиндр)
S_cathode = np.pi * d_wire * l_wire

# Мощность нагрева
P = I_h * U_h

# Решение уравнения P = sigma*epsilon*S*(T^4 - T0^4)
T_energy = np.zeros(len(P))
for i in range(len(P)):
    if P[i] > 0:
        T_energy[i] = (P[i] / (sigma * epsilon * S_cathode) + T0**4)**0.25
    else:
        T_energy[i] = T0

# 3. Данные для метода Ричардсона-Дэшмана (экспериментальные точки)
I_h_richardson = np.array([2.4, 2.5, 2.6, 2.7, 2.8, 2.9])  # токи накала в А
I_a_saturation = np.array([0.192e-3, 0.589e-3, 1.155e-3, 3.41e-3, 8.05e-3, 8.53e-3])  # максимальные анодные токи в А

# Площадь эмитирующей поверхности катода
S_emit = np.pi * d_wire * l_wire

# Функция для решения уравнения Ричардсона-Дэшмана
def richardson_temp(T, I_a, S_emit, phi):
    return 120.14e4 * (1 - 0.07) * S_emit * T**2 * np.exp(-phi * 1.602e-19 / (1.38e-23 * T)) - I_a

# Решение для каждой точки
T_richardson = np.zeros(len(I_h_richardson))
phi = 4.5  # работа выхода вольфрама в эВ

for i in range(len(I_h_richardson)):
    # Начальное приближение из расчета по энергетическому балансу для соответствующего тока
    idx = np.argmin(np.abs(I_h - I_h_richardson[i]))
    T_initial = T_energy[idx]
    
    # Решение уравнения
    solution = fsolve(richardson_temp, T_initial, args=(I_a_saturation[i], S_emit, phi))
    T_richardson[i] = solution[0]

# Построение графика с улучшениями
plt.figure(figsize=(10, 6.5))
plt.style.use('seaborn-v0_8-whitegrid')

# Более яркие и насыщенные цвета
colors = ['#0072BD', '#D95319']  # Яркий синий и оранжевый

# График 1: По сопротивлению - яркий синий
plt.plot(I_h, T_resistance, color=colors[0], linewidth=2, 
         marker='o', markersize=6, markevery=2, 
         label='По изменению сопротивления', alpha=0.9)

# График 2: По энергетическому балансу - яркий оранжевый/красный
plt.plot(I_h, T_energy, color=colors[1], linewidth=2, 
         marker='s', markersize=6, markevery=2, 
         label='По энергетическому балансу', alpha=0.9)

# Соединяем точки Ричардсона линией
plt.plot(I_h_richardson, T_richardson, color='#77AC30', 
         linewidth=2.5, linestyle='-', alpha=0.8,
         label='Метод Ричардсона-Дэшмана')

# Экспериментальные точки Ричардсона (6 точек) - ярко-зеленые
plt.scatter(I_h_richardson, T_richardson, color='#77AC30', 
           s=50, zorder=5, edgecolors='black', linewidth=1.0,
           alpha=0.9)

# Настройка сетки
plt.grid(True, linestyle='--', alpha=0.7, linewidth=0.8)

# Настройка осей
plt.xlabel('Ток накала, А', fontsize=13, fontweight='medium')
plt.ylabel('Температура катода, К', fontsize=13, fontweight='medium')

# Устанавливаем красивые пределы осей
plt.xlim(0, 3.0)
plt.ylim(0, 3200)

# Настройка делений на осях
plt.xticks(np.arange(0, 3.1, 0.5), fontsize=11)
plt.yticks(np.arange(0, 3201, 500), fontsize=11)

# Легенда - компактная и информативная
plt.legend(loc='lower right', fontsize=11, framealpha=0.95, 
           edgecolor='gray', fancybox=True, shadow=True)

# Минималистичный заголовок
# plt.title('Температура катода vs ток накала', fontsize=15, 
#           fontweight='bold', pad=15)

# Тонкая рамка вокруг графика
for spine in plt.gca().spines.values():
    spine.set_linewidth(1.0)
    spine.set_color('gray')

# Добавляем легкую тень под графиком для объема
# plt.gca().patch.set_facecolor('#f8f9fa')

plt.tight_layout()

# Сохранение графика в высоком качестве
# plt.savefig('cathode_temperature_plot_v2.png', dpi=300, bbox_inches='tight')
plt.show()

# Вывод значений точек Ричардсона для проверки
# print("\nТочки Ричардсона-Дэшмана:")
# print(f"{'Ток, А':<10} {'Температура, К':<15}")
# print("-" * 25)
# for i in range(len(I_h_richardson)):
#     print(f"{I_h_richardson[i]:<10.1f} {T_richardson[i]:<15.1f}")