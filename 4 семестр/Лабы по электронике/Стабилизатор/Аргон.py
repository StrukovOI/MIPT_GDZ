import numpy as np
import matplotlib.pyplot as plt
from scipy.interpolate import Akima1DInterpolator

# Данные: давление в 10⁻³ торр, напряжение в 10⁻² кВ
p = np.array([2420, 1410, 220, 196, 178, 128, 91, 58])
U = np.array([50, 45, 40, 40, 40, 41, 41, 93])

# Погрешности (половина последнего разряда)
dp = np.full_like(p, 1, dtype=int)
dU = np.full_like(U, 1, dtype=int)

# Сортировка по возрастанию давления (для кривой Пашена)
idx = np.argsort(p)
p_sorted = p[idx]
U_sorted = U[idx]
dp_sorted = dp[idx]
dU_sorted = dU[idx]

# Интерполяция Акима
akima = Akima1DInterpolator(p_sorted, U_sorted)

# Плотная сетка для гладкой кривой
p_dense = np.linspace(p_sorted.min(), p_sorted.max(), 500)
U_dense = akima(p_dense)

# Построение графика
plt.figure(figsize=(10, 6))
plt.errorbar(p_sorted, U_sorted, xerr=dp_sorted, yerr=dU_sorted,
             fmt='ro', markersize=8, capsize=3, ecolor='red', elinewidth=1,
             label='Экспериментальные точки')
plt.plot(p_dense, U_dense, 'b-', linewidth=2, label='Интерполяционная кривая')
plt.xlabel('Давление p (10⁻³ торр)')
plt.ylabel('Напряжение U (10⁻² кВ)')
plt.grid(True, linestyle='--', alpha=0.6)
plt.legend()
plt.tight_layout()
plt.show()