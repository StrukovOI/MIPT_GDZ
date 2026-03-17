import numpy as np
import matplotlib.pyplot as plt
from scipy.interpolate import Akima1DInterpolator

# Исходные данные (давление в торр, напряжение в единицах 10^-2 кВ)
p = np.array([2000, 1750, 1000, 229, 148, 125, 103, 90, 78, 65])
U = np.array([90, 80, 70, 61, 68, 74, 85, 96, 108, 127])

# Перевод напряжения в вольты
U_V = U * 10

# Погрешности: половина последнего разряда
dp = np.full_like(p, 1, dtype=int)                 # для давления, торр
dU = np.full_like(U, 1 * 10, dtype=int)            # для напряжения, В (0.5 * 10 = 5 В)

# Сортировка по возрастанию давления (для интерполяции)
idx = np.argsort(p)
p_sorted = p[idx]
U_sorted = U_V[idx]
dp_sorted = dp[idx]
dU_sorted = dU[idx]

# Интерполяция Акима
akima = Akima1DInterpolator(p_sorted, U_sorted)

# Плотная сетка для гладкой кривой
p_dense = np.linspace(p_sorted.min(), p_sorted.max(), 500)
U_dense = akima(p_dense)

# Построение графика
plt.figure(figsize=(10, 6))

# Интерполяционная кривая
plt.plot(p_dense, U_dense, 'b-', linewidth=2, label='Интерполяционная кривая')

# Экспериментальные точки с погрешностями
plt.errorbar(p_sorted, U_sorted, 
             xerr=dp_sorted, yerr=dU_sorted, 
             fmt='ro', markersize=8, capsize=3,
             label='Экспериментальные точки')

# Подписи и сетка
plt.xlabel('Давление p (торр)')
plt.ylabel('Напряжение U (В)')
plt.grid(True, linestyle='--', alpha=0.6)
plt.legend()
plt.tight_layout()
plt.show()