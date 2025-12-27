import matplotlib.pyplot as plt
import numpy as np
from scipy.optimize import curve_fit

# Данные из таблицы
T = np.array([283.5, 288.0, 290.0, 292.0, 294.0, 296.0, 298.0, 300.0, 302.0, 304.0, 306.0, 308.0, 310.0, 312.0, 314.0])
T_errors = np.array([0.2] * 15)

tau2_minus_tau02 = np.array([36.758, 35.022, 33.321, 30.442, 25.207, 18.048, 11.697, 7.680, 5.798, 4.864, 4.306, 3.806, 3.381, 3.086, 2.865])
tau2_errors = np.array([0.022, 0.022, 0.021, 0.021, 0.021, 0.020, 0.019, 0.019, 0.019, 0.019, 0.019, 0.019, 0.018, 0.018, 0.018])

# Для определения точки Кюри используем закон Кюри-Вейсса
# 1/χ ∼ (T - Θ) ∼ 1/(τ² - τ₀²)
# Поэтому строим зависимость 1/(τ² - τ₀²) от T

# Данные для обратной величины (четвертый столбец)
inverse_tau2 = np.array([0.0272, 0.0286, 0.0300, 0.0328, 0.0397, 0.0554, 0.0855, 0.1302, 0.1725, 0.2056, 0.2322, 0.2627, 0.2958, 0.3241, 0.3491])
inverse_errors = np.array([0.00002, 0.00002, 0.00002, 0.00002, 0.00003, 0.00006, 0.00014, 0.00032, 0.00056, 0.00079, 0.00100, 0.00128, 0.00162, 0.00194, 0.00224])

# Линейная аппроксимация для высокотемпературной области (парамагнитная область)
# Выбираем точки, где явно виден линейный рост (T > 294K)
mask = T > 294
T_high = T[mask]
inverse_high = inverse_tau2[mask]
errors_high = inverse_errors[mask]

# Линейная функция для аппроксимации
def linear_func(x, a, b):
    return a * x + b

# Аппроксимация с учетом погрешностей
popt, pcov = curve_fit(linear_func, T_high, inverse_high, sigma=errors_high)
a, b = popt
a_err, b_err = np.sqrt(np.diag(pcov))

# Точка Кюри - где линейная экстраполяция пересекает ось X (1/χ = 0)
curie_point = -b / a
curie_point_err = curie_point * np.sqrt((a_err/a)**2 + (b_err/b)**2)

print(f"Точка Кюри: {curie_point:.1f} ± {curie_point_err:.1f} K")

# Построение графика зависимости τ² - τ₀² от T
plt.figure(figsize=(12, 8))

# Точки с погрешностями
plt.errorbar(T, tau2_minus_tau02, xerr=T_errors, yerr=tau2_errors, 
             fmt='o', markersize=6, capsize=4, capthick=1, 
             label='Экспериментальные точки', color='blue', alpha=0.7)

# Соединение точек плавной кривой
plt.plot(T, tau2_minus_tau02, 'b-', alpha=0.5, linewidth=1.5)

# Вертикальная линия для рассчитанной точки Кюри
plt.axvline(x=curie_point, color='red', linestyle='--', linewidth=2, 
            label=f'Точка Кюри ({curie_point:.1f} ± {curie_point_err:.1f} K)')

# Точка на кривой в месте точки Кюри
idx = np.argmin(np.abs(T - curie_point))
plt.plot(T[idx], tau2_minus_tau02[idx], 'ro', markersize=8)

# Настройки графика
plt.xlabel('Температура T, K', fontsize=14)
plt.ylabel(r'$\tau^2 - \tau_0^2$, мкс$^2$', fontsize=14)
plt.title(r'Зависимость $\tau^2 - \tau_0^2$ от температуры', fontsize=16)
plt.grid(True, alpha=0.3)
plt.legend(fontsize=12)

# Добавляем аннотации
# plt.annotate('Ферромагнитная область', 
#              xy=(285, 30), 
#              xytext=(280, 35),
#              arrowprops=dict(arrowstyle='->', color='red'),
#              fontsize=12, color='red')

# plt.annotate('Парамагнитная область', 
#              xy=(300, 10), 
#              xytext=(305, 15),
#              arrowprops=dict(arrowstyle='->', color='red'),
#              fontsize=12, color='red')

plt.tight_layout()
plt.show()

# Дополнительный график для демонстрации определения точки Кюри
# plt.figure(figsize=(10, 6))
# plt.errorbar(T, inverse_tau2, xerr=T_errors, yerr=inverse_errors, 
#              fmt='o', label='Экспериментальные точки', color='green')

# # Линейная аппроксимация
# T_fit = np.linspace(curie_point, 314, 100)
# plt.plot(T_fit, linear_func(T_fit, a, b), 'r-', 
#          label=f'Линейная аппроксимация: y = {a:.4f}x + {b:.3f}')

# # Точка Кюри
# plt.axvline(x=curie_point, color='red', linestyle='--', 
#             label=f'Точка Кюри: {curie_point:.1f} K')

# plt.xlabel('Температура T, K', fontsize=12)
# plt.ylabel(r'$1/(\tau^2 - \tau_0^2)$, мкс$^{-2}$', fontsize=12)
# plt.title('Определение точки Кюри по закону Кюри-Вейсса', fontsize=14)
# plt.grid(True, alpha=0.3)
# plt.legend()
# plt.tight_layout()
# plt.show()