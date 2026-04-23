import numpy as np
import matplotlib.pyplot as plt

# Исходные данные: (n+1) и z (см)
n1 = np.array([2, 3, 4, 5, 6, 7])
z = np.array([6.9, 4.0, 2.9, 2.3, 1.9, 1.65])

# Погрешность по z (постоянная, ±0.1 см)
z_err = 0.2

# Преобразование: x = 1/(n+1)
x = 1 / n1

# Линейная аппроксимация (полином 1-й степени)
coeffs = np.polyfit(x, z, 1)
k, b = coeffs
z_fit = k * x + b

# Расчёт коэффициента детерминации R^2
ss_res = np.sum((z - z_fit)**2)
ss_tot = np.sum((z - np.mean(z))**2)
r2 = 1 - ss_res / ss_tot

# Построение графика
plt.figure(figsize=(8, 5))

# Отображаем точки с погрешностями (error bars)
plt.errorbar(x, z, yerr=z_err, fmt='o', color='blue', capsize=3,
             label='Экспериментальные точки')

# Линия аппроксимации
plt.plot(x, z_fit, color='red', linestyle='--', 
         label=f'Аппроксимация: z = {k:.3f}·x - {-b:.3f}')

plt.xlabel('1/(n+1)')
plt.ylabel('z, см')
plt.grid(True, linestyle=':', alpha=0.7)
plt.legend()
plt.tight_layout()
plt.show()

print(f"Уравнение прямой: z = {k:.4f} * (1/(n+1)) + {b:.4f}")
print(f"Коэффициент детерминации R^2 = {r2:.4f}")