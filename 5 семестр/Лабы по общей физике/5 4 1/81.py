import numpy as np
import matplotlib.pyplot as plt
from scipy.interpolate import make_interp_spline

# 1. Исходные данные
t = 10.0  # Время измерения, с
P_raw = np.array([21, 58, 93, 121, 143, 195, 243, 293, 343, 393, 443, 543, 593, 693, 743])
N_count_raw = np.array([3244, 2548, 1896, 1356, 959, 326, 92, 31, 3, 3, 4, 6, 4, 2, 1])

# 2. Расчет скорости счета и погрешностей
N = N_count_raw / t
dN = np.sqrt(N_count_raw) / t  # Погрешность по Пуассону
dP = 1.0  # Погрешность манометра, мм рт. ст.

# Сортировка данных по давлению
sort_idx = np.argsort(P_raw)
P = P_raw[sort_idx]
N = N[sort_idx]
dN = dN[sort_idx]

# Настройка стиля графиков
plt.rcParams['font.size'] = 12
plt.rcParams['axes.grid'] = True
plt.rcParams['grid.alpha'] = 0.6

# ==========================================
# ГРАФИК: Полный диапазон (ЛИНЕЙНАЯ шкала, гладкая кривая)
# ==========================================
# Для построения гладкой кривой используем интерполяцию по log10(N),
# чтобы избежать осцилляций при большом динамическом диапазоне,
# и затем возвращаемся к линейным значениям.
log_N = np.log10(N)
P_smooth = np.linspace(P.min(), P.max(), 500)
spline_log = make_interp_spline(P, log_N, k=3)
log_N_smooth = spline_log(P_smooth)
N_smooth = 10**log_N_smooth

plt.figure(figsize=(10, 6))
# Кривая аппроксимации
plt.plot(P_smooth, N_smooth, '-', color='blue', linewidth=2, label='Аппроксимация')
# Экспериментальные точки с погрешностями
plt.errorbar(P, N, xerr=dP, yerr=dN, fmt='o', color='red', 
             ecolor='black', capsize=4, markersize=6, label='Экспериментальные точки')

# Линейная шкала по оси Y (убрана логарифмическая)
plt.xlabel('Давление $P$, мм рт. ст.', fontsize=13)
plt.ylabel('Скорость счёта $N$, имп/с', fontsize=13)
plt.title('Зависимость скорости счёта от давления (линейный масштаб)', fontsize=14)
plt.legend()
plt.tight_layout()
# plt.savefig('scint_linear_full_smooth.png', dpi=300)  # при необходимости
plt.show()