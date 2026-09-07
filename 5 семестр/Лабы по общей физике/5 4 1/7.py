import numpy as np
import matplotlib.pyplot as plt
from collections import defaultdict

# 1. Исходные данные
x_raw = [40, 35, 35, 30, 25, 25, 20, 20, 20, 15, 12.5, 10, 10, 10, 9, 7.5, 6, 5, 2.5, 0]
N_raw = [0.100, 0.200, 0.100, 0.098, 0.200, 0.300, 0.129, 0.100, 0.133, 0.467, 0.233,
         0.433, 0.467, 0.550, 0.433, 4.500, 13.833, 14.850, 18.750, 16.200]

# 2. Усреднение повторяющихся измерений
data = defaultdict(list)
for x, n in zip(x_raw, N_raw):
    data[x].append(n)

x_avg = sorted(data.keys())
N_avg = [np.mean(data[x]) for x in x_avg]

x_avg = np.array(x_avg)
N_avg = np.array(N_avg)

# 3. Расчёт погрешностей
dx = 0.5          # погрешность расстояния, мм
t_meas = 30.0     # время измерения, с
dN = np.sqrt(N_avg / t_meas)

# 4. Построение графика в обычном (линейном) масштабе
plt.figure(figsize=(10, 7))
plt.errorbar(x_avg, N_avg, xerr=dx, yerr=dN, fmt='o', color='red',
             ecolor='black', capsize=4, markersize=7, label='Экспериментальные точки')
plt.xlabel('Расстояние $x$, мм', fontsize=12)
plt.ylabel('Скорость счёта $N$, имп/с', fontsize=12)
# plt.title('Зависимость скорости счёта от расстояния (линейный масштаб)', fontsize=14)
plt.legend(fontsize=11)
plt.grid(True, alpha=0.3)
plt.tight_layout()
plt.show()