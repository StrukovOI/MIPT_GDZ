import numpy as np
import matplotlib.pyplot as plt
from scipy.optimize import curve_fit

# Данные
m = np.array([1, 2, 3, 4, 5, 6, 7, 8])
r2 = np.array([1024.00, 1806.25, 2550.25, 3249.00, 4000.56, 4692.25, 5402.25, 6201.56])
r2_err = np.array([32.0, 42.5, 50.5, 57.0, 63.3, 68.5, 73.5, 78.8])  # погрешности r^2

# Линейная аппроксимация с учётом погрешностей (взвешенный МНК)
def linear_func(x, a, b):
    return a * x + b

# Взвешенный fit: веса = 1/ошибка^2
weights = 1 / r2_err**2
popt, pcov = curve_fit(linear_func, m, r2, sigma=r2_err, absolute_sigma=True)
a, b = popt
a_err, b_err = np.sqrt(np.diag(pcov))

# Гладкие точки для прямой
m_fit = np.linspace(min(m)-0.5, max(m)+0.5, 100)
r2_fit = linear_func(m_fit, a, b)

# Построение
plt.figure(figsize=(8, 5))
plt.errorbar(m, r2, yerr=r2_err, fmt='o', capsize=4, capthick=1, elinewidth=1,
             label='Экспериментальные точки', color='blue', markersize=6)
plt.plot(m_fit, r2_fit, 'r-', label=f'Аппроксимация: $r^2 = ({a:.2f} \\pm {a_err:.2f}) m + ({b:.1f} \\pm {b_err:.1f})$')
plt.xlabel('m')
plt.ylabel('$r^2$, мм$^2$')
# plt.title('Зависимость $r^2$ от $m$')
plt.grid(True, linestyle='--', alpha=0.7)
plt.legend()
plt.tight_layout()
plt.show()

# Вывод коэффициентов
print(f"Коэффициент наклона a = {a:.2f} ± {a_err:.2f}")
print(f"Свободный член b = {b:.1f} ± {b_err:.1f}")