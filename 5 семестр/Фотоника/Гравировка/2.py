import numpy as np
import scipy.stats as stats
import matplotlib.pyplot as plt

# Настройка шрифтов для корректного отображения кириллицы и знака минуса
plt.rcParams['font.sans-serif'] = ['Arial', 'DejaVu Sans', 'Helvetica']
plt.rcParams['axes.unicode_minus'] = False

# Исходные данные
I = np.array([14.1, 14.4, 14.7, 15.0, 15.3, 15.6, 15.9, 16.2, 16.5, 16.8, 17.1, 17.4])
P = np.array([40, 102, 182, 264, 352, 460, 570, 680, 820, 922, 1015, 1082])

# Выбор линейного участка (от 14.7 А до 16.8 А, где нет насыщения)
mask = (I >= 14.7) & (I <= 16.8)
I_lin, P_lin = I[mask], P[mask]

# Линейная регрессия
slope, intercept, r_value, p_value, std_err = stats.linregress(I_lin, P_lin)
I_th = -intercept / slope

# Погрешности
yerr = 15.0   # +- 10 мВт для мощности
xerr = 0.1    # +- 0.1 А для тока
n = len(I_lin)
Delta = n * np.sum(I_lin**2) - np.sum(I_lin)**2
sigma_k = yerr * np.sqrt(n / Delta)
sigma_b = yerr * np.sqrt(np.sum(I_lin**2) / Delta)
sigma_Ith = np.sqrt((sigma_b / slope)**2 + (sigma_k * intercept / slope**2)**2)

print(f"Результаты аппроксимации:")
print(f"Наклон (КПД): k = {slope:.1f} +/- {sigma_k:.1f} мВт/А")
print(f"Пороговый ток: I_th = {I_th:.2f} +/- {sigma_Ith:.2f} А")
print(f"R^2 = {r_value**2:.4f}")

# Построение графика
plt.figure(figsize=(8, 6))

# Все экспериментальные точки с погрешностями
plt.errorbar(I, P, xerr=xerr, yerr=yerr, fmt='o', color='blue', alpha=0.7, 
             ecolor='black', capsize=3, label='Экспериментальные точки')

# Линия аппроксимации
I_fit = np.linspace(14.0, 17.6, 100)
P_fit = slope * I_fit + intercept
plt.plot(I_fit, P_fit, 'r-', linewidth=2, label=f'Аппроксимация: $P = {slope:.1f} \\cdot I {intercept:.1f}$')

# Вертикальная линия порогового тока
plt.axvline(I_th, color='green', linestyle='--', linewidth=2, 
            label=f'Пороговый ток $I_{{пор}}$ = {I_th:.2f} А')

# Оформление
plt.xlabel('Ток накачки, А', fontsize=12)
plt.ylabel('Мощность излучения, мВт', fontsize=12)
# plt.title('Зависимость мощности излучения от тока накачки\n(режим модуляции добротности)', fontsize=14)
plt.legend(fontsize=11)
plt.grid(True, linestyle=':', alpha=0.8)
plt.tight_layout()

# Сохранение и отображение
# plt.savefig('q_switched_plot.png', dpi=300)
# print("\nГрафик успешно сохранен как 'q_switched_plot.png'")
plt.show()