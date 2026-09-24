import numpy as np
import matplotlib.pyplot as plt

# 1. Исходные данные для калибровки
N = np.array([1069.86, 1236.06, 1357.11, 1765.88])
E = np.array([4.784, 5.49, 6.002, 7.687])

# Небольшие разумные погрешности для красивого отображения (можно убрать, если не требуются)
dN = np.array([1.0, 1.0, 1.0, 1.0])      # погрешность канала ~1
dE = np.array([0.01, 0.01, 0.01, 0.01])  # погрешность табличной энергии ~0.01 МэВ

# 2. Линейная аппроксимация (МНК): E = k * N + b
k, b = np.polyfit(N, E, 1)

# Создаём точки для построения гладкой линии тренда
N_fit = np.linspace(min(N) - 50, max(N) + 50, 100)
E_fit = k * N_fit + b

# 3. Построение графика
plt.figure(figsize=(8, 6))

# Точки с погрешностями
plt.errorbar(N, E, xerr=dN, yerr=dE, fmt='o', color='blue', 
             ecolor='black', capsize=4, markersize=6, label='Экспериментальные точки')

# Линия тренда
plt.plot(N_fit, E_fit, '-', color='red', linewidth=2, 
         label=f'Линейная аппроксимация:\nE = {k:.5f}·N + {b:.3f}')

# Оформление
plt.xlabel('Номер канала $N$', fontsize=12)
plt.ylabel('Энергия $E$, МэВ', fontsize=12)
# plt.title('Калибровочная зависимость спектрометра', fontsize=14)
plt.legend(loc='upper left', fontsize=11)
plt.grid(True, alpha=0.4)

plt.tight_layout()
plt.savefig('calibration_graph.png', dpi=300)
print("График сохранён как 'calibration_graph.png'")
plt.show()

# 4. Вывод коэффициентов для вставки в LaTeX
print("\n--- Результаты для вставки в отчёт ---")
print(f"Коэффициент наклона k = {k:.5f} МэВ/канал")
print(f"Свободный член b = {b:.3f} МэВ")
# Проверка качества аппроксимации (R^2)
E_pred = k * N + b
ss_res = np.sum((E - E_pred)**2)
ss_tot = np.sum((E - np.mean(E))**2)
r_squared = 1 - (ss_res / ss_tot)
print(f"Коэффициент детерминации R^2 = {r_squared:.6f} (должен быть близок к 1)")