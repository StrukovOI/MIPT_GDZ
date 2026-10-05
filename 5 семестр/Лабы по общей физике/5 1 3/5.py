import numpy as np
import matplotlib.pyplot as plt
from scipy.interpolate import UnivariateSpline

# === ДАННЫЕ ИЗМЕРЕНИЙ ===
# Накал 2.755 В
V1 = np.array([-0.035, 0.059, 0.314, 1.125, 1.963, 2.19, 2.299, 2.407, 2.491, 2.608, 2.655, 2.766, 2.837, 2.863, 2.995, 3.117, 3.167, 3.243, 3.363, 3.417, 3.56, 3.712, 3.831, 3.902, 4.086, 4.229, 4.426, 4.739, 5.328, 5.532, 5.844, 6.172, 6.429, 6.724, 6.988, 7.53, 7.904, 8.332, 8.637, 9.109, 9.402, 9.837, 10.071, 10.451, 11.084, 11.438, 11.977, 11.979])
V_anode1_mV = np.array([-0.11, -0.11, -0.11, -0.11, -0.09, 0.04, 0.32, 1.18, 2.81, 7.49, 10.39, 18.54, 24.54, 26.95, 37.45, 43.21, 44.61, 45.85, 47.08, 47.59, 48.09, 47.45, 47.89, 47.89, 47.66, 48.15, 49.51, 48.78, 43.8, 41.48, 39.6, 36.85, 35.61, 35.45, 35.25, 30.55, 28.17, 25.79, 24.13, 22.39, 21.42, 20.56, 20.07, 19.98, 20.55, 21.25, 22.11, 22.52])

# Накал 2.925 В
V2 = np.array([-0.055, 1.277, 2.053, 2.388, 2.654, 3.084, 3.315, 3.689, 4.049, 4.448, 5.031, 5.543, 5.868, 6.445, 6.83, 7.14, 7.358, 7.75, 8.259, 9.042, 9.472, 10.188, 10.919, 11.523])
V_anode2_mV = np.array([-0.11, -0.11, -0.07, 1.25, 14.53, 46.35, 52.82, 58.96, 62.85, 65.67, 67.18, 66.76, 65.75, 63.34, 60.28, 57.59, 55.83, 52.11, 49.33, 43.72, 41.36, 39.47, 40.25, 42.29])

# Перевод в ток (мкА)
I1 = V_anode1_mV / 100.0
I2 = V_anode2_mV / 100.0

# Погрешности (обновлено: анод ±1 мВ)
dV = 0.002
dV_anode = 1.0  # мВ
dI = dV_anode / 100.0  # 0.01 мкА

# === ГЛОБАЛЬНАЯ СГЛАЖИВАЮЩАЯ АППРОКСИМАЦИЯ ===
# Один сплайн на весь диапазон — как в Excel
# Параметр s подбирается так, чтобы кривая была плавной, но следовала за данными

# Для первого набора: убираем шум в начале (V < 2), там ток ~0
mask1 = V1 >= 2.0
spline1 = UnivariateSpline(V1[mask1], I1[mask1], k=3, s=0.05)

mask2 = V2 >= 2.0
spline2 = UnivariateSpline(V2[mask2], I2[mask2], k=3, s=0.05)

# Плотная сетка для гладких кривых
V_dense = np.linspace(2.0, 12.0, 1000)
I1_smooth = spline1(V_dense)
I2_smooth = spline2(V_dense)

# === РАСЧЁТ РАЗМЕРА ЭЛЕКТРОННОЙ ОБОЛОЧКИ ===
V_max1, V_min1 = 3.7, 10.5
V_max2, V_min2 = 5.0, 10.2
V_max_avg = (V_max1 + V_max2) / 2.0

h = 6.626e-34
m_e = 9.109e-31
e_charge = 1.602e-19
U0 = 2.5

E_max_J = (V_max_avg + U0) * e_charge
l_meters = h / (2 * np.sqrt(2 * m_e * E_max_J))
l_angstrom = l_meters * 1e10

print("=== РЕЗУЛЬТАТЫ ДЛЯ ОТЧЁТА ===")
print(f"Среднее напряжение максимума: {V_max_avg:.2f} В")
print(f"Расчетный размер электронной оболочки l = {l_angstrom:.2f} Å")

# === ПОСТРОЕНИЕ ГРАФИКА ===
plt.figure(figsize=(12, 7))

# Экспериментальные точки с обновлёнными крестами погрешностей (±1 мВ)
plt.errorbar(V1, I1, xerr=dV, yerr=dI, fmt='o', color='blue', 
             ecolor='gray', capsize=3, markersize=4, alpha=0.7, label='Эксп. (2.755 В)')
plt.errorbar(V2, I2, xerr=dV, yerr=dI, fmt='s', color='red', 
             ecolor='gray', capsize=3, markersize=4, alpha=0.7, label='Эксп. (2.925 В)')

# Гладкие сплайны (как в Excel)
plt.plot(V_dense, I1_smooth, '-', color='blue', linewidth=2, alpha=0.9)
plt.plot(V_dense, I2_smooth, '-', color='red', linewidth=2, alpha=0.9)

# Отметка экстремумов
# plt.axvline(V_max1, color='blue', linestyle='--', alpha=0.6, linewidth=1.5)
# plt.axvline(V_min1, color='blue', linestyle=':', alpha=0.6, linewidth=1.5)
# plt.text(V_max1 + 0.2, 0.45, f'Макс: {V_max1:.1f} В', color='blue', fontsize=11, fontweight='bold')
# plt.text(V_min1 + 0.2, 0.25, f'Мин: {V_min1:.1f} В', color='blue', fontsize=11, fontweight='bold')

plt.xlabel('Напряжение катод-сетка $V$, В', fontsize=13)
plt.ylabel('Анодный ток $I_a$, мкА', fontsize=13)
# plt.title('Вольт-амперная характеристика тиратрона (статический режим)', fontsize=15)
plt.legend(loc='upper right', fontsize=11)
plt.grid(True, alpha=0.4)
plt.xlim(-0.5, 12.5)
plt.ylim(-0.05, 0.75)
plt.tight_layout()
plt.savefig('vax_static_smooth.png', dpi=300)
print("График сохранён как 'vax_static_smooth.png'")
plt.show()