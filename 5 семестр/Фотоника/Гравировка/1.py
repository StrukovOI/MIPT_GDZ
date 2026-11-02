import numpy as np
import matplotlib.pyplot as plt
import scipy.stats as stats

# Исходные данные
I = np.array([0, 7.9, 10.2, 13.1, 14.1, 14.4, 14.7, 15.0, 15.3, 15.6, 15.9, 16.2, 16.5, 16.8, 17.1, 17.4])
P = np.array([0, 0, 1, 2, 22, 85, 150, 220, 320, 440, 570, 700, 820, 950, 1080, 1190])

# Выбор линейного участка (I >= 15.0 A)
mask = I >= 15.0
I_lin, P_lin = I[mask], P[mask]

# Линейная регрессия
slope, intercept, r_value, p_value, std_err = stats.linregress(I_lin, P_lin)
I_th = -intercept / slope

# Погрешности
yerr = 20   # +- 10 мВт для мощности
xerr = 0.1  # +- 0.1 А для тока (предполагаем, что +-1 в условии была опечаткой)

# Построение графика
plt.figure(figsize=(8, 6))
plt.errorbar(I, P, xerr=xerr, yerr=yerr, fmt='o', color='blue', alpha=0.7, label='Экспериментальные точки')

I_fit = np.linspace(14.5, 17.6, 100)
P_fit = slope * I_fit + intercept
plt.plot(I_fit, P_fit, 'r-', label=f'Аппроксимация: P = {slope:.1f}·I {intercept:.1f}')

plt.axvline(I_th, color='green', linestyle='--', label=f'Пороговый ток $I_{{пор}}$ = {I_th:.2f} А')

plt.xlabel('Ток накачки, А')
plt.ylabel('Мощность излучения, мВт')
# plt.title('Зависимость мощности излучения от тока накачки (свободная генерация)')
plt.legend()
plt.grid(True)
plt.tight_layout()
# plt.savefig('free_generation_plot.png', dpi=300)
plt.show()