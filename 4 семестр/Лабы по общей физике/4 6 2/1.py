import numpy as np
import matplotlib.pyplot as plt
from scipy.interpolate import CubicSpline

# Первая зависимость (x1, y1)
x1 = np.array([0, 0.13, 0.26, 0.35, 0.5, 0.59, 0.75, 0.92, 1.07, 1.27, 1.46, 1.79, 2.74, 3.38, 4.46])
y1 = np.array([1, 0.977011494, 0.954022989, 0.91954023, 0.862068966, 0.793103448, 0.747126437, 0.67816092,
               0.632183908, 0.574712644, 0.528735632, 0.471264368, 0.310344828, 0.218390805, 0.137931034])

# Вторая зависимость (x2, y2)
x2 = np.array([0, 0.46, 0.65, 0.92, 1.14, 1.39, 1.61, 1.92, 2.09, 2.2, 2.57, 2.96, 3.41, 3.67, 4.47, 4.76])
y2 = np.array([0.040229885, 0.126436782, 0.189655172, 0.247126437, 0.33908046, 0.402298851, 0.471264368,
               0.563218391, 0.632183908, 0.689655172, 0.770114943, 0.850574713, 0.902298851, 0.942528736,
               0.977011494, 0.994252874])

# Создание кубических сплайнов (естественные граничные условия)
cs1 = CubicSpline(x1, y1, bc_type='natural')
cs2 = CubicSpline(x2, y2, bc_type='natural')

# Точки для плавного построения каждой кривой
x1_smooth = np.linspace(x1.min(), x1.max(), 300)
y1_smooth = cs1(x1_smooth)

x2_smooth = np.linspace(x2.min(), x2.max(), 300)
y2_smooth = cs2(x2_smooth)

# Общий диапазон для суммы (ограничен максимальным x первой зависимости)
x_common = np.linspace(0, x1.max(), 300)  # от 0 до 4.46
y_sum = cs1(x_common) + cs2(x_common)

# Построение графика
plt.figure(figsize=(10, 6))

# Первая зависимость (точки и сплайн)
plt.scatter(x1, y1, color='blue', s=40, zorder=3)
plt.plot(x1_smooth, y1_smooth, color='blue', linewidth=2, label='T')

# Вторая зависимость (точки и сплайн)
plt.scatter(x2, y2, color='green', s=40, zorder=3)
plt.plot(x2_smooth, y2_smooth, color='green', linewidth=2, label='R')

# Сумма сплайнов
plt.plot(x_common, y_sum, color='red', linestyle='--', linewidth=2, label='T + R')

# Оформление
plt.xlabel(r'$\ell$, мм', fontsize=12)
plt.ylabel('R, T', fontsize=12)
# plt.title('Аппроксимация кубическими сплайнами и их сумма', fontsize=14)
plt.grid(True, linestyle=':', alpha=0.7)
plt.legend(fontsize=10)
plt.tight_layout()
plt.show()