import numpy as np
import matplotlib.pyplot as plt

# Исходные данные
I_raw = np.array([4, 5, 23, 36, 90, 90, 120, 148, 168, 206, 265, 295, 321, 390, 455, 497, 580, 640, 640, 640, 632, 625, 620])
P_raw = np.array([8, 8, 28, 38, 90, 91, 118, 143, 168, 193, 243, 268, 293, 343, 388, 421, 478, 543, 543, 593, 638, 688, 743])

# Вычитаем нулевое показание
I_zero = 2  # пА
I_corrected = I_raw - I_zero

# Усредняем повторяющиеся измерения
data = {}
for p, i in zip(P_raw, I_corrected):
    if p not in data:
        data[p] = []
    data[p].append(i)

P_avg = sorted(data.keys())
I_avg = [np.mean(data[p]) for p in P_avg]

P_avg = np.array(P_avg)
I_avg = np.array(I_avg)

# Находим горизонтальный участок (плато) - последние точки
plateau_mask = P_avg > 500
I_plateau = np.mean(I_avg[plateau_mask])

# Находим наклонный участок для экстраполяции
# Берем точки в области роста (примерно от 100 до 450 мм рт. ст.)
slope_mask = (P_avg > 100) & (P_avg < 450)
P_slope = P_avg[slope_mask]
I_slope = I_avg[slope_mask]

# Линейная аппроксимация наклонного участка
k, b = np.polyfit(P_slope, I_slope, 1)

# Точка пересечения наклонной прямой с уровнем плато
P_extrap = (I_plateau - b) / k

# Построение графика
plt.figure(figsize=(10, 6))

# ЗАМЕНА: используем errorbar вместо plot для добавления крестов погрешностей
plt.errorbar(P_avg, I_avg, xerr=2.5, yerr=1.0, fmt='o-', color='blue', ecolor='black', capsize=4, markersize=5, label='Экспериментальные точки')

# Рисуем наклонную прямую
P_line = np.linspace(0, P_extrap + 50, 100)
I_line = k * P_line + b
plt.plot(P_line, I_line, '--', color='red', linewidth=2, label='Аппроксимация наклонного участка')

# Рисуем горизонтальную линию плато
# plt.axhline(I_plateau, color='green', linestyle='--', linewidth=2, label=f'Уровень плато ({I_plateau:.1f} пА)')

# Отмечаем точку пересечения
# plt.axvline(P_extrap, color='purple', linestyle='-.', linewidth=2, alpha=0.7)
# plt.text(P_extrap + 20, I_plateau - 50, f'P_э ≈ {P_extrap:.0f} мм рт. ст.', color='purple', fontsize=12, fontweight='bold')

plt.xlabel('Давление P, мм рт. ст.', fontsize=12)
plt.ylabel('Ток I, пА', fontsize=12)
# plt.title('Зависимость тока ионизационной камеры от давления', fontsize=14)
plt.legend()
plt.grid(True, alpha=0.3)
plt.tight_layout()
plt.savefig('ion_chamber_graph.png', dpi=300)
plt.show()

print(f"Уровень плато: {I_plateau:.1f} пА")
print(f"Экстраполированное давление: {P_extrap:.0f} мм рт. ст.")