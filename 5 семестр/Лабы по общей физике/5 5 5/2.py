import numpy as np
import matplotlib.pyplot as plt

# Данные для калибровки (фотопики с известными энергиями)
E_cal = np.array([0.511, 0.6617, 1.1732, 1.274, 1.3325])  # МэВ
N_cal = np.array([747.769, 950.315, 1637.490, 1761.878, 1849.134])  # каналы
dN_cal = np.array([58.799, 63.549, 85.430, 108.979, 93.856])  # погрешность N

# Линейная аппроксимация N = a*E + b
a, b = np.polyfit(E_cal, N_cal, 1)

# Плотная сетка для графика
E_fit = np.linspace(0, 1.5, 100)
N_fit = a * E_fit + b

# Построение графика
plt.figure(figsize=(10, 7))

# Экспериментальные точки с погрешностями
plt.errorbar(E_cal, N_cal, xerr=0, yerr=dN_cal, fmt='o', color='blue', 
             ecolor='gray', capsize=4, markersize=6, label='Калибровочные точки')

# Линия аппроксимации
plt.plot(E_fit, N_fit, '-', color='red', linewidth=2, 
         label=f'Аппроксимация: N = {a:.2f}·E + {b:.2f}')

plt.xlabel('Энергия $E$, МэВ', fontsize=13)
plt.ylabel('Номер канала $N$', fontsize=13)
# plt.title('Калибровочный график гамма-спектрометра', fontsize=14)
plt.legend(fontsize=11)
plt.grid(True, alpha=0.4)
plt.tight_layout()
plt.savefig('calibration_gamma.png', dpi=300)
print("График сохранён как 'calibration_gamma.png'")
plt.show()

# Вывод результатов
print(f"\n=== РЕЗУЛЬТАТЫ КАЛИБРОВКИ ===")
print(f"Коэффициент a = {a:.2f} каналов/МэВ")
print(f"Коэффициент b = {b:.2f} каналов")
print(f"Уравнение: N = {a:.2f}·E + {b:.2f}")

# Проверка качества аппроксимации (R²)
N_pred = a * E_cal + b
ss_res = np.sum((N_cal - N_pred)**2)
ss_tot = np.sum((N_cal - np.mean(N_cal))**2)
r_squared = 1 - (ss_res / ss_tot)
print(f"Коэффициент детерминации R² = {r_squared:.6f}")