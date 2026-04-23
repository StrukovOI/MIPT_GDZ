import numpy as np
import matplotlib.pyplot as plt

# Данные: m и x_m (мкм)
m = np.array([-9, -8, -7, -6, -5, -4, -3, -2, -1, 0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10])
x = np.array([-800.0871, -712.9232, -624.4582, -534.6924, -444.9265, -353.8597,
              -267.9967, -179.5317, -92.3678, 0.0000, 91.0668, 179.5317, 269.2976,
              357.7625, 450.1303, 534.6924, 624.4582, 714.2241, 805.2909, 892.4549])

# Погрешность по x_m (вертикальная ось)
y_err = 5.0  # мкм

# Линейная аппроксимация x = k*m + b
coeffs = np.polyfit(m, x, 1)
k, b = coeffs
x_fit = k * m + b

# R^2
ss_res = np.sum((x - x_fit)**2)
ss_tot = np.sum((x - np.mean(x))**2)
r2 = 1 - ss_res / ss_tot

# Построение
plt.figure(figsize=(8, 5))
plt.errorbar(m, x, yerr=y_err, fmt='o', capsize=3, elinewidth=1,
             color='blue', label='Экспериментальные точки')
plt.plot(m, x_fit, 'r--', label=f'Линейная аппроксимация: $x_m = {k:.4f}\,m + {b:.4f}$')
plt.xlabel('m')
plt.ylabel('$x_m$, мкм')
# plt.title('Зависимость координаты полосы от порядка m')
plt.grid(True, linestyle=':', alpha=0.7)
plt.legend()
# plt.text(0.05, 0.95, f'$R^2 = {r2:.6f}$', transform=plt.gca().transAxes,
#          fontsize=12, verticalalignment='top',
#          bbox=dict(boxstyle='round', facecolor='white', alpha=0.8))
plt.tight_layout()
plt.show()

print(f"Уравнение прямой: x_m = {k:.4f} * m + {b:.4f}")
print(f"R^2 = {r2:.6f}")