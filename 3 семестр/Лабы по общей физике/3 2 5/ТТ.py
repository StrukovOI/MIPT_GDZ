import numpy as np
import matplotlib.pyplot as plt
from scipy import stats

# Данные из таблицы
T_teor = np.array([67.99, 92.58, 111.88, 128.32, 142.87, 156.08, 168.25, 179.60, 190.27, 200.38])  # мкс
T_meas = np.array([68, 94, 112, 128, 142, 158, 166, 178, 192, 200])  # мкс

# Погрешности измерений ±2 мкс
error = np.array([2, 2, 2, 2, 2, 2, 2, 2, 2, 2])  # мкс

# Линейная регрессия (МНК) с учётом погрешностей через веса
# Веса обратно пропорциональны квадрату погрешности
weights = 1 / error**2
slope, intercept, r_value, p_value, std_err = stats.linregress(T_teor, T_meas)
# Альтернатива с весами (закомментировано, т.к. scipy.stats.linregress не поддерживает веса)
# Используем numpy.polyfit с весами
coefficients = np.polyfit(T_teor, T_meas, 1, w=weights)
slope_weighted, intercept_weighted = coefficients

# Создание точек для аппроксимирующей прямой
T_teor_line = np.linspace(T_teor.min(), T_teor.max(), 100)
T_meas_line = slope * T_teor_line + intercept
T_meas_line_weighted = slope_weighted * T_teor_line + intercept_weighted

# Построение графика
plt.figure(figsize=(8, 6))

# Точки с погрешностями
plt.errorbar(T_teor, T_meas, yerr=error, fmt='ro', markersize=6, capsize=4, 
             label='Экспериментальные точки с погрешностью')

# Аппроксимирующая прямая
plt.plot(T_teor_line, T_meas_line, 'b-', linewidth=2, 
         label=f'Аппроксимация: T_эксп = {slope:.4f}·T_теор + {intercept:.2f}')

# Идеальная прямая T_эксп = T_теор
# plt.plot([T_teor.min(), T_teor.max()], [T_teor.min(), T_teor.max()], 'g--', 
#          alpha=0.7, label='Идеальная зависимость T_эксп = T_теор')

# Настройка графика
plt.xlabel(r'Теоретический период $T_{теор}$, мкс', fontsize=12)
plt.ylabel('Измеренный период T, мкс', fontsize=12)
# plt.title('Сравнение экспериментального и теоретического периодов', fontsize=14)
# plt.legend(fontsize=10)
plt.grid(True, linestyle='--', alpha=0.7)

# Установка равных масштабов по осям
plt.axis('equal')
plt.tight_layout()

# Вывод параметров аппроксимации
print(f"Коэффициент наклона: {slope:.4f}")
print(f"Свободный член: {intercept:.2f}")
print(f"Коэффициент детерминации R²: {r_value**2:.4f}")
print(f"Коэффициент наклона (с учётом весов): {slope_weighted:.4f}")
print(f"Свободный член (с учётом весов): {intercept_weighted:.2f}")

plt.show()