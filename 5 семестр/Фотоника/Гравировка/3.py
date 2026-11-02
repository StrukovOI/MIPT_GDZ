import numpy as np
import matplotlib.pyplot as plt
from scipy.optimize import curve_fit

# Настройка шрифтов
plt.rcParams['font.sans-serif'] = ['Arial', 'DejaVu Sans', 'Helvetica']
plt.rcParams['axes.unicode_minus'] = False

# Данные (без первой точки 13.5 А)
I = np.array([13.8, 14.1, 14.4, 14.7, 15.0, 15.3, 15.6, 15.9, 16.2, 16.5, 16.8, 17.1, 17.4])
P_out = np.array([2, 40, 102, 182, 264, 352, 460, 570, 680, 820, 922, 1015, 1082])
FWHM = np.array([0.45, 0.43, 0.43, 0.4225, 0.375, 0.34, 0.3275, 0.315, 0.2825, 0.2725, 0.2825, 0.261, 0.265])

# Мощность накачки (напряжение ~168 В)
V_pump = 168.0
P_pump = I * V_pump

# Линеаризация: 1/Δτ vs P_нак
inv_FWHM = 1.0 / FWHM

# Линейная аппроксимация: 1/Δτ = a * P_нак + b
a, b = np.polyfit(P_pump, inv_FWHM, 1)
print(f"Линеаризация: 1/Δτ = {a:.6f} * P_нак + {b:.4f}")
print(f"Коэффициент корреляции: {np.corrcoef(P_pump, inv_FWHM)[0,1]:.4f}")

# Обратное преобразование для построения кривой
P_smooth = np.linspace(min(P_pump), max(P_pump), 200)
FWHM_fit = 1.0 / (a * P_smooth + b)

# Построение графика
plt.figure(figsize=(10, 7))

# Экспериментальные точки (маленькие, чёрные)
plt.errorbar(P_pump, FWHM, yerr=0.02, fmt='o', color='blue', 
             ecolor='gray', capsize=2, markersize=5, label='Экспериментальные данные')

# Аппроксимация через линеаризацию
plt.plot(P_smooth, FWHM_fit, 'r-', linewidth=2, label='Аппроксимация: $\\Delta\\tau = 1/(aP + b)$')

plt.xlabel('Мощность накачки $P_{\\text{нак}}$, Вт', fontsize=13)
plt.ylabel('Длительность импульса $\\tau$, мкс', fontsize=13)
# plt.title('Зависимость длительности импульса от мощности накачки\n(режим модуляции добротности)', fontsize=14)
plt.legend(fontsize=11)
plt.grid(True, linestyle=':', alpha=0.8)
plt.tight_layout()

# plt.savefig('pulse_duration_linearized.png', dpi=300)
# print("\nГрафик сохранен как 'pulse_duration_linearized.png'")
plt.show()

# Вывод параметров
P_th_approx = -b/a  # где 1/Δτ = 0 (формальный порог)
print(f"\nФормальный порог (где 1/Δτ → 0): P_пор ≈ {P_th_approx:.0f} Вт (ток ≈ {P_th_approx/V_pump:.2f} А)")
print(f"При P_нак → ∞: Δτ → 1/b ≈ {1/b:.3f} мкс")