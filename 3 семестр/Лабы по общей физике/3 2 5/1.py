import numpy as np
import matplotlib.pyplot as plt
from scipy.optimize import curve_fit

# Данные из таблицы
C = np.array([0.0012, 0.0022, 0.0032, 0.0042, 0.0052, 0.0062, 0.0072, 0.0082, 0.0092, 0.0102])  # мкФ
T_meas = np.array([68, 94, 112, 128, 142, 158, 166, 178, 192, 200])  # мкс
T_teor = np.array([67.99, 92.58, 111.88, 128.32, 142.87, 156.08, 168.25, 179.60, 190.27, 200.38])  # мкс

# Функция для аппроксимации T = a * sqrt(C)
def fit_func(C, a):
    return a * np.sqrt(C)

# Аппроксимация данных
popt_meas, _ = curve_fit(fit_func, C, T_meas)
popt_teor, _ = curve_fit(fit_func, C, T_teor)

# Создание гладкой кривой для графика
C_smooth = np.linspace(C.min(), C.max(), 500)
T_meas_smooth = fit_func(C_smooth, *popt_meas)
T_teor_smooth = fit_func(C_smooth, *popt_teor)

# Построение графика
plt.figure(figsize=(10, 6))
plt.plot(C_smooth, T_meas_smooth, 'r-', label=f'Измеренный период')
plt.plot(C_smooth, T_teor_smooth, 'b--', label=f'Теоретический период')
plt.plot(C, T_meas, 'ro')
plt.plot(C, T_teor, 'b^')

# Настройка внешнего вида
plt.xlabel('C, мкФ', fontsize=12)
plt.ylabel('T, мкс', fontsize=12)
# plt.title('Зависимость периода колебаний от ёмкости', fontsize=14)
plt.legend(fontsize=10)
plt.grid(True, linestyle='--', alpha=0.7)

# Дополнительные настройки
plt.xlim(0.001, 0.011)
plt.xticks(np.arange(0.001, 0.011, 0.001))
plt.tight_layout()
plt.show()

# Вывод параметров аппроксимации
print(f"Параметр аппроксимации для измеренных данных: a = {popt_meas[0]:.2f}")
print(f"Параметр аппроксимации для теоретических данных: a = {popt_teor[0]:.2f}")