import numpy as np
import matplotlib.pyplot as plt
from scipy.interpolate import Akima1DInterpolator

# Данные
x = np.array([50.21, 50.66, 50.73, 50.96, 51.14, 51.61, 53.82, 54.27, 54.61, 55.19, 57.35, 59.67])
y = np.array([8, 6.2, 4.2, 2.6, 1.2, 0, 1.7, 3.95, 6.3, 7.75, 0.05, 7.75])

# Погрешности
x_err = 0.05
y_err = 0.05

# Сортировка данных по x (Akima требует монотонного x)
sort_idx = np.argsort(x)
x_sorted = x[sort_idx]
y_sorted = y[sort_idx]

# Интерполятор Акима
akima = Akima1DInterpolator(x_sorted, y_sorted)

# Гладкая сетка для отображения кривой
x_smooth = np.linspace(x_sorted.min(), x_sorted.max(), 300)
y_smooth = akima(x_smooth)

# Построение графика
plt.figure(figsize=(8, 5))
# Точки с погрешностями
plt.errorbar(x_sorted, y_sorted, xerr=x_err, yerr=y_err, fmt='o', capsize=3,
             elinewidth=1, markeredgewidth=1, color='blue', label='Экспериментальные точки')
# Кривая интерполяции Акима
plt.plot(x_smooth, y_smooth, 'r-', linewidth=2, label='Интерполяция Акима')
plt.xlabel('x, мм')
plt.ylabel('I, мкА')
# plt.title('Интерполяция Акима с погрешностями')
plt.grid(True, linestyle=':', alpha=0.7)
# plt.legend()
plt.tight_layout()
plt.show()