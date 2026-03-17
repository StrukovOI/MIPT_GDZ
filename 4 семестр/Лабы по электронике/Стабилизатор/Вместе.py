import numpy as np
import matplotlib.pyplot as plt
from scipy.interpolate import Akima1DInterpolator

# Данные первого набора (p в 10⁻³ торр, U в 10⁻² кВ)
p1 = np.array([2000, 1750, 1000, 229, 148, 125, 103, 90, 78, 65])
U1 = np.array([90, 80, 70, 61, 68, 74, 85, 96, 108, 127])

# Данные второго набора
p2 = np.array([2420, 1410, 220, 196, 178, 128, 91, 58])
U2 = np.array([50, 45, 40, 40, 40, 41, 41, 93])

# Погрешности (половина последнего разряда) – явно int
dp1 = np.full_like(p1, 1, dtype=int)
dU1 = np.full_like(U1, 1, dtype=int)
dp2 = np.full_like(p2, 1, dtype=int)
dU2 = np.full_like(U2, 1, dtype=int)

# Сортировка по возрастанию давления (необходимо для интерполяции)
idx1 = np.argsort(p1)
p1_sorted = p1[idx1]
U1_sorted = U1[idx1]
dp1_sorted = dp1[idx1]
dU1_sorted = dU1[idx1]

idx2 = np.argsort(p2)
p2_sorted = p2[idx2]
U2_sorted = U2[idx2]
dp2_sorted = dp2[idx2]
dU2_sorted = dU2[idx2]

# Интерполяция Акима для каждого набора
akima1 = Akima1DInterpolator(p1_sorted, U1_sorted)
akima2 = Akima1DInterpolator(p2_sorted, U2_sorted)

# Плотные сетки для гладких кривых
p1_dense = np.linspace(p1_sorted.min(), p1_sorted.max(), 500)
U1_dense = akima1(p1_dense)
p2_dense = np.linspace(p2_sorted.min(), p2_sorted.max(), 500)
U2_dense = akima2(p2_dense)

# Построение графика
plt.figure(figsize=(10, 6))

# Первый набор – синий цвет, маркеры круги
plt.errorbar(p1_sorted, U1_sorted, xerr=dp1_sorted, yerr=dU1_sorted,
             fmt='o', color='red', markersize=6, capsize=3,
             ecolor='red', elinewidth=1, label=None)  # точки без легенды
plt.plot(p1_dense, U1_dense, 'b-', linewidth=2, label='Воздух')

# Второй набор – красный цвет, маркеры квадраты
plt.errorbar(p2_sorted, U2_sorted, xerr=dp2_sorted, yerr=dU2_sorted,
             fmt='o', color='lime', markersize=6, capsize=3,
             ecolor='lime', elinewidth=1, label=None)
plt.plot(p2_dense, U2_dense, 'm-', linewidth=2, label='Аргон')

plt.xlabel('Давление p (10⁻³ торр)')
plt.ylabel('Напряжение U (10⁻² кВ)')
plt.grid(True, linestyle='--', alpha=0.6)
plt.legend()
plt.tight_layout()

# Если хотите логарифмическую шкалу по оси давления (обычно для кривой Пашена), раскомментируйте следующую строку:
# plt.xscale('log')

plt.show()