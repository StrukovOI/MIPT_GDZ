import matplotlib.pyplot as plt
import numpy as np
from scipy.optimize import curve_fit

# Данные из таблицы
T = np.array([283.5, 288.0, 290.0, 292.0, 294.0, 296.0, 298.0, 300.0, 302.0, 304.0, 306.0, 308.0, 310.0, 312.0, 314.0])
T_errors = np.array([0.2] * 15)

inverse_tau2 = np.array([0.0272, 0.0286, 0.0300, 0.0328, 0.0397, 0.0554, 0.0855, 0.1302, 0.1725, 0.2056, 0.2322, 0.2627, 0.2958, 0.3241, 0.3491])
inverse_errors = np.array([0.00002, 0.00002, 0.00002, 0.00002, 0.00003, 0.00006, 0.00014, 0.00032, 0.00056, 0.00079, 0.00100, 0.00128, 0.00162, 0.00194, 0.00224])

# Линейная функция для аппроксимации
def linear_func(x, a, b):
    return a * x + b

# Аппроксимация линейной части (парамагнитная область)
# Выбираем точки выше предполагаемой точки Кюри (например, T > 295K)
mask = T > 295
T_fit = T[mask]
inverse_fit = inverse_tau2[mask]
errors_fit = inverse_errors[mask]

# Аппроксимация с учетом погрешностей
popt, pcov = curve_fit(linear_func, T_fit, inverse_fit, sigma=errors_fit)
a, b = popt
a_err, b_err = np.sqrt(np.diag(pcov))

# Точка Кюри - где линейная экстраполяция пересекает ось X (1/χ = 0)
curie_point = -b / a
curie_point_err = curie_point * np.sqrt((a_err/a)**2 + (b_err/b)**2)

print(f"Точка Кюри: {curie_point:.1f} ± {curie_point_err:.1f} K")

# Построение графика
plt.figure(figsize=(12, 8))

# Точки с погрешностями
plt.errorbar(T, inverse_tau2, xerr=T_errors, yerr=inverse_errors, 
             fmt='o', markersize=6, capsize=4, capthick=1, 
             label='Экспериментальные точки', color='blue', alpha=0.7)

# Соединение точек плавной кривой
plt.plot(T, inverse_tau2, 'b-', alpha=0.5, linewidth=1.5, label='Экспериментальная зависимость')

# Линейная экстраполяция для определения точки Кюри
T_extrap = np.linspace(curie_point, max(T), 100)
plt.plot(T_extrap, linear_func(T_extrap, a, b), 'r--', 
         label=f'Линейная аппроксимация: y = {a:.5f}x - {-b:.3f}')

# Вертикальная линия для точки Кюри
plt.axvline(x=curie_point, color='red', linestyle='--', linewidth=2, 
            label=f'Парамагнитная точка Кюри ({curie_point:.1f} ± {curie_point_err:.1f} K)')

# Точка пересечения с осью X (точка Кюри)
plt.plot(curie_point, 0, 'ro', markersize=8)

# Настройки графика
plt.xlabel('Температура T, K', fontsize=14)
plt.ylabel(r'$\dfrac{1}{\tau^2 - \tau_0^2}$, мкс$^{-2}$', fontsize=14)
plt.title('Зависимость $1/(\\tau^2 - \\tau_0^2)$ от температуры', fontsize=16)
plt.grid(True, alpha=0.3)
plt.legend(fontsize=12)

# Добавляем аннотации
# plt.annotate('Ферромагнитная область', 
#              xy=(285, 0.03), 
#              xytext=(280, 0.05),
#              arrowprops=dict(arrowstyle='->', color='red'),
#              fontsize=12, color='red')

# plt.annotate('Парамагнитная область', 
#              xy=(305, 0.2), 
#              xytext=(305, 0.25),
#              arrowprops=dict(arrowstyle='->', color='red'),
#              fontsize=12, color='red')

plt.tight_layout()
plt.show()