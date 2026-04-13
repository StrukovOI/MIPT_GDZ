import numpy as np
import matplotlib.pyplot as plt

# Данные
x = np.array([6.99, 7.12, 7.25, 7.34, 7.49, 7.58, 7.74, 7.91, 8.06, 8.26, 8.45, 8.78, 9.73, 10.37, 11.45])
y = np.array([4.465908119, 4.442651256, 4.418840608, 4.382026635, 4.317488114, 4.234106505, 4.17438727, 
              4.077537444, 4.007333185, 3.912023005, 3.828641396, 3.713572067, 3.295836866, 2.944438979, 2.48490665])

# Погрешности
x_err = 0.05
y_err = 0.04   # если нужна другая погрешность по y — измените здесь

# Линейная аппроксимация
coeffs = np.polyfit(x, y, 1)
k, b = coeffs
y_fit = k * x + b

# Расчёт R^2
ss_res = np.sum((y - y_fit)**2)
ss_tot = np.sum((y - np.mean(y))**2)
r2 = 1 - ss_res / ss_tot

# Построение графика
plt.figure(figsize=(8, 5))
# Отображение точек с крестами погрешностей
plt.errorbar(x, y, xerr=x_err, yerr=y_err, fmt='o', capsize=3, elinewidth=1, 
             markeredgewidth=1, color='blue', label='Исходные точки')
plt.plot(x, y_fit, label=f'Линейная аппроксимация: y = {k:.4f}x + {b:.4f}', color='red', linestyle='--')
plt.xlabel('z, мм')
plt.ylabel('T')
plt.grid(True, linestyle=':', alpha=0.7)
plt.legend()
plt.tight_layout()
plt.show()

print(f"Уравнение прямой: y = {k:.6f} * x + {b:.6f}")
print(f"Коэффициент детерминации R^2 = {r2:.6f}")