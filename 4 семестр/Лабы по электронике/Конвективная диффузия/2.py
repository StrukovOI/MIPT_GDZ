import numpy as np
import matplotlib.pyplot as plt
from scipy.interpolate import Akima1DInterpolator

# Исходные данные
freq = np.array([0.1, 0.2, 0.5, 1, 2, 5, 10, 20])
U_ratio = np.array([3.15, 3.905, 5.065, 3.125, 3.375, 1.83, 0.81, 0.275])

# Создание интерполятора Акима
akima_interp = Akima1DInterpolator(freq, U_ratio)

# Гладкая сетка частот (логарифмическая для равномерного отображения на таком диапазоне)
freq_smooth = np.logspace(np.log10(freq.min()), np.log10(freq.max()), 500)
U_smooth = akima_interp(freq_smooth)

# Построение графика
plt.figure(figsize=(8, 5))
plt.semilogx(freq, U_ratio, 'o', label='Экспериментальные точки', markersize=8)
plt.semilogx(freq_smooth, U_smooth, '-', label='Интерполяция Акима', linewidth=2)
plt.xlabel('Частота, Гц')
plt.ylabel('$U_{вых}/U_{вх}$')
# plt.title('Интерполяция Акима частотной характеристики')
plt.grid(True, linestyle='--', alpha=0.7)
# plt.legend()
plt.tight_layout()
plt.show()