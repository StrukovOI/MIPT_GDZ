import numpy as np
import matplotlib.pyplot as plt
from scipy.interpolate import CubicSpline

# Исходные данные
U = np.array([2, 5, 10, 15, 20, 30, 40, 50, 100, 150])
I = np.array([-4, -1.1, 2.5, 6.3, 10.1, 16, 22.5, 27, 49.6, 67])

# Создание кубического сплайна (естественные граничные условия)
cs = CubicSpline(U, I, bc_type='natural')

# Гладкая сетка для отображения
U_smooth = np.linspace(U.min(), U.max(), 200)
I_smooth = cs(U_smooth)

# Построение графика
plt.figure(figsize=(8, 5))
plt.plot(U, I, 'o', label='Экспериментальные точки', markersize=8)
plt.plot(U_smooth, I_smooth, '-', label='Кубический сплайн', linewidth=2)
plt.xlabel('U, мВ')
plt.ylabel('I, мкА')
# plt.title('Интерполяция кубическими сплайнами')
plt.grid(True, linestyle='--', alpha=0.7)
# plt.legend()
plt.tight_layout()
plt.show()