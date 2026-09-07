import numpy as np
import matplotlib.pyplot as plt
from collections import defaultdict
from scipy.interpolate import make_interp_spline, UnivariateSpline

# 1. Исходные данные
x_raw = [40, 35, 35, 30, 25, 25, 20, 20, 20, 15, 12.5, 10, 10, 10, 9, 7.5, 6, 5, 2.5, 0]
N_raw = [0.100, 0.200, 0.100, 0.098, 0.200, 0.300, 0.129, 0.100, 0.133, 0.467, 0.233, 
         0.433, 0.467, 0.550, 0.433, 4.500, 13.833, 14.850, 18.750, 16.200]

# 2. Усреднение повторяющихся измерений
data = defaultdict(list)
for x, n in zip(x_raw, N_raw):
    data[x].append(n)

# Сортируем по возрастанию расстояния
x_avg = sorted(data.keys())
N_avg = [np.mean(data[x]) for x in x_avg]

x_avg = np.array(x_avg)
N_avg = np.array(N_avg)

# 3. Расчёт погрешностей
dx = 0.5  # Погрешность расстояния, мм
t_meas = 30.0  # Время измерения в секундах (измените на ваше реальное время)
dN = np.sqrt(N_avg / t_meas)

# 4. Создание плотной сетки для сплайнов
x_smooth = np.linspace(x_avg.min(), x_avg.max(), 500)

# ==========================================
# ГРАФИК 1: Полный диапазон (Логарифмическая шкала Y)
# ==========================================
plt.figure(figsize=(10, 7))

# Строим сплайн в логарифмической шкале для лучшей интерполяции малых значений
log_N_avg = np.log10(N_avg)
spline_log = make_interp_spline(x_avg, log_N_avg, k=3)  # k=3 - кубический сплайн
log_N_smooth = spline_log(x_smooth)
N_smooth_log = 10**log_N_smooth

# Основной график
plt.plot(x_smooth, N_smooth_log, 'b-', linewidth=2, label='Аппроксимация')
plt.errorbar(x_avg, N_avg, xerr=dx, yerr=dN, fmt='o', color='red', 
             ecolor='black', capsize=4, markersize=7, label='Экспериментальные точки')

plt.yscale('log')
plt.xlabel('Расстояние $x$, мм', fontsize=12)
plt.ylabel('Скорость счёта $N$, имп/с (лог. шкала)', fontsize=12)
# plt.title('Зависимость скорости счёта от расстояния (полный диапазон)', fontsize=14)
plt.legend(fontsize=11)
plt.grid(True, alpha=0.3)
plt.tight_layout()
plt.savefig('graph_full_log_spline.png', dpi=300)
plt.show()

# ==========================================
# ГРАФИК 2: Область спада (Линейная шкала, зум)
# ==========================================
plt.figure(figsize=(10, 7))

# Для линейного графика используем сглаживающий сплайн (лучше работает с шумом)
# Фильтруем только область спада (x от 4 до 16 мм)
mask = (x_avg >= 4) & (x_avg <= 16)
x_drop = x_avg[mask]
N_drop = N_avg[mask]

x_drop_smooth = np.linspace(x_drop.min(), x_drop.max(), 300)

# UnivariateSpline с параметром s (степень сглаживания)
# Чем больше s, тем более гладкая кривая
spline_drop = UnivariateSpline(x_drop, N_drop, s=0.5)  # s можно регулировать
N_drop_smooth = spline_drop(x_drop_smooth)

# Основной график
plt.plot(x_drop_smooth, N_drop_smooth, 'g-', linewidth=2.5, label='Сглаживающий сплайн')
plt.errorbar(x_drop, N_drop, xerr=dx, yerr=dN[mask], fmt='s', color='darkred', 
             ecolor='black', capsize=4, markersize=7, label='Экспериментальные данные')

plt.xlim(4, 16)
plt.ylim(0, 6)
plt.xlabel('Расстояние $x$, мм', fontsize=12)
plt.ylabel('Скорость счёта $N$, имп/с', fontsize=12)
plt.title('Область спада кривой (для определения пробега)', fontsize=14)
plt.legend(fontsize=11)
plt.grid(True, alpha=0.3)
plt.tight_layout()
plt.savefig('graph_drop_spline.png', dpi=300)
plt.show()

# Вывод усреднённых данных для проверки
print("x (мм)\t N_ср (имп/с)\t dN (имп/с)")
for i in range(len(x_avg)):
    print(f"{x_avg[i]:<6}\t {N_avg[i]:<12.3f}\t {dN[i]:<6.3f}")