import numpy as np
import matplotlib.pyplot as plt
from scipy.interpolate import CubicSpline

# Исходные данные в заданном порядке
U = np.array([122, 120, 117, 118, 124, 125, 122, 120, 118, 115])
I = np.array([19, 17, 15, 13, 11, 9, 7, 5, 3, 1])

# Погрешности
dU = np.full_like(U, 1, dtype=int)
dI = np.full_like(I, 1, dtype=int)

# Параметр t (индексы точек)
t = np.arange(len(U))

# Кубические сплайны для U(t) и I(t)
cs_U = CubicSpline(t, U, bc_type='natural')   # естественные граничные условия
cs_I = CubicSpline(t, I, bc_type='natural')

# Плотная сетка по параметру для гладкой кривой
t_dense = np.linspace(t.min(), t.max(), 500)
U_dense = cs_U(t_dense)
I_dense = cs_I(t_dense)

# Построение графика
plt.figure(figsize=(10, 6))
plt.errorbar(U, I, xerr=dU, yerr=dI, 
             fmt='ro', markersize=8, capsize=3, 
             ecolor='red', elinewidth=1,
             label='Экспериментальные точки')
plt.plot(U_dense, I_dense, 'b-', linewidth=2, 
         label='Интерполяционная кривая')

plt.xlabel('Напряжение U (10⁻² кВ)')
plt.ylabel('Ток I (10⁻⁴ А)')
plt.grid(True, linestyle='--', alpha=0.6)
plt.legend()
plt.tight_layout()
plt.show()