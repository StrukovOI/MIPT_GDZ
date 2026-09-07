import numpy as np
import matplotlib.pyplot as plt
from scipy.interpolate import make_interp_spline, UnivariateSpline

# 1. Исходные данные
t = 10.0  # Время измерения, с
P_raw = np.array([21, 58, 93, 121, 143, 195, 243, 293, 343, 393, 443, 543, 593, 693, 743])
N_count_raw = np.array([3244, 2548, 1896, 1356, 959, 326, 92, 31, 3, 3, 4, 6, 4, 2, 1])

# 2. Расчет скорости счета и погрешностей
N = N_count_raw / t
dN = np.sqrt(N_count_raw) / t  # Погрешность по Пуассону
dP = 1.0  # Погрешность манометра, мм рт. ст.

# Сортировка данных по давлению (на случай, если они были перепутаны)
sort_idx = np.argsort(P_raw)
P = P_raw[sort_idx]
N = N[sort_idx]
dN = dN[sort_idx]

# Настройка стиля графиков
plt.rcParams['font.size'] = 12
plt.rcParams['axes.grid'] = True
plt.rcParams['grid.alpha'] = 0.6

# ==========================================
# ГРАФИК 1: Полный диапазон (Логарифмическая шкала Y, гладкая кривая)
# ==========================================
# Для логарифмического графика интерполируем log10(N), чтобы избежать отрицательных значений и осцилляций
log_N = np.log10(N)
# Создаем плотную сетку для гладкой кривой
P_smooth_full = np.linspace(P.min(), P.max(), 500)
# Кубический сплайн (k=3)
spline_log = make_interp_spline(P, log_N, k=3)
log_N_smooth = spline_log(P_smooth_full)
N_smooth_full = 10**log_N_smooth

plt.figure(figsize=(10, 6))
plt.plot(P_smooth_full, N_smooth_full, '-', color='blue', linewidth=2, label='Аппроксимация')
plt.errorbar(P, N, xerr=dP, yerr=dN, fmt='o', color='red', ecolor='black', capsize=4, markersize=6, label='Экспериментальные точки')

plt.yscale('log')
plt.xlabel('Давление $P$, мм рт. ст.', fontsize=13)
plt.ylabel('Скорость счёта $N$, имп/с (лог. шкала)', fontsize=13)
# plt.title('Зависимость скорости счёта от давления (полный диапазон)', fontsize=14)
plt.legend()
plt.tight_layout()
plt.savefig('scint_log_smooth.png', dpi=300)
plt.show()

# ==========================================
# ГРАФИК 2: Область спада (Линейная шкала, гладкая кривая + экстраполяция)
# ==========================================
# Оценим уровень фона по последним точкам (P > 300)
N_bg = np.mean(N[P > 300]) 

# Берем только область спада для построения касательной (исключаем плато и чистый фон)
# Например, точки, где N находится между фоном + 1 и 80% от максимума
N_max = np.max(N)
mask_drop = (N > N_bg + 0.5) & (N < N_max * 0.8)
P_drop = P[mask_drop]
N_drop = N[mask_drop]

# Линейная аппроксимация (касательная) на самом крутом участке спада
k, b = np.polyfit(P_drop, N_drop, 1)
P_extrap = (N_bg - b) / k  # Точка пересечения касательной с уровнем фона

# Создаем гладкую кривую для всей области спада с помощью сглаживающего сплайна
P_smooth_drop = np.linspace(P.min(), P.max(), 500)
# Параметр s отвечает за степень сглаживания. Чем больше s, тем глаже кривая.
# Для этих данных s=2.0 хорошо убирает шум на хвосте, сохраняя форму спада.
spline_drop = UnivariateSpline(P, N, s=2.0)
N_smooth_drop = spline_drop(P_smooth_drop)

plt.figure(figsize=(10, 6))
plt.plot(P_smooth_drop, N_smooth_drop, '-', color='green', linewidth=2.5, label='Сглаживающая кривая')
plt.errorbar(P, N, xerr=dP, yerr=dN, fmt='s', color='darkred', ecolor='black', capsize=4, markersize=6, label='Экспериментальные точки')

# Рисуем касательную для экстраполяции
P_line = np.linspace(min(P_drop)-20, max(P_drop)+40, 100)
N_line = k * P_line + b
plt.plot(P_line, N_line, '--', color='blue', linewidth=2, label=f'Касательная к участку спада')

# Горизонтальная линия фона
plt.axhline(N_bg, color='black', linestyle=':', linewidth=1.5, label=f'Уровень фона $N_{{bg}} \\approx {N_bg:.2f}$')

# Вертикальная линия экстраполированного давления
plt.axvline(P_extrap, color='blue', linestyle='-.', linewidth=1.5, alpha=0.7)
plt.text(P_extrap + 10, N_bg + 2, f'$P_{{э}} \\approx {P_extrap:.1f}$ мм рт. ст.', color='blue', fontsize=12, fontweight='bold')

# Настройки осей для зума на область спада
plt.xlim(0, 350)
plt.ylim(-1, max(N_drop) + 10)

plt.xlabel('Давление $P$, мм рт. ст.', fontsize=13)
plt.ylabel('Скорость счёта $N$, имп/с', fontsize=13)
plt.title('Определение экстраполированного давления $P_{э}$', fontsize=14)
plt.legend()
plt.tight_layout()
plt.savefig('scint_linear_drop_smooth.png', dpi=300)
plt.show()

print(f"Уровень фона N_bg: {N_bg:.2f} имп/с")
print(f"Экстраполированное давление P_э: {P_extrap:.1f} мм рт. ст.")