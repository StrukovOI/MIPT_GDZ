import numpy as np
import matplotlib.pyplot as plt
import math

# Параметры уравнения Дитеричи для CO₂
a = 0.45  # Параметр притяжения (Па·м⁶·К/моль²)
b = 3.2e-5  # Параметр объема (м³/моль)
R = 8.314  # Универсальная газовая постоянная (Дж/(моль·К))

# Расчет критических параметров для уравнения Дитеричи
V_crit = 2 * b  # Критический объем
T_crit = a / (4 * R * b)  # Критическая температура
P_crit = (a / (4 * math.exp(2) * b**2))  # Критическое давление

print(f"Критическая температура: {T_crit:.2f} K")
print(f"Критическое давление: {P_crit/1e6:.2f} МПа")
print(f"Критический объем: {V_crit*1000:.4f} л/моль")

# Функция для расчета давления по уравнению Дитеричи
def dieterici_pressure(V, T):
    return (R * T / (V - b)) * np.exp(-a / (R * T * V))

# Создаем диапазон объемов (исключаем V = b)
V = np.linspace(b * 1.05, 10 * b, 500)  # от 1.05b до 10b

# Создаем график
plt.figure(figsize=(10, 7))
plt.title("Изотермы уравнения Дитеричи для CO₂", fontsize=14)
plt.xlabel("Объем V, м³/моль", fontsize=12)
plt.ylabel("Давление P, МПа", fontsize=12)
plt.grid(True, linestyle='--', alpha=0.7)

# Рассчитываем и строим изотермы для разных температур
temperatures = [0.8 * T_crit, T_crit, 1.2 * T_crit, 1.5 * T_crit]
colors = ['blue', 'red', 'green', 'purple']
labels = [
    f'T = {0.8*T_crit:.1f} K',
    f'T = {T_crit:.1f} K',
    f'T = {1.2*T_crit:.1f} K',
    f'T = {1.5*T_crit:.1f} K'
]

for T, color, label in zip(temperatures, colors, labels):
    P = dieterici_pressure(V, T)
    plt.plot(V, P/1e6, color=color, linewidth=2, label=label)  # Переводим в МПа

# Добавляем критические точки
plt.scatter([V_crit], [P_crit/1e6], color='black', s=80, zorder=5, 
           label=f'Критическая точка')#({V_crit:.5f} м³/моль, {P_crit/1e6:.2f} МПа)

# Добавляем асимптоту для идеального газа при критической температуре
P_ideal = R * T_crit / V
plt.plot(V, P_ideal/1e6, 'r--', linewidth=1, label=r'Идеальный газ (при T$_{\text{крит}}$)')

# Настраиваем легенду и отображение
plt.legend(fontsize=10)
plt.xlim(V[0], V[-1])
plt.ylim(0, 20)  # Ограничение по давлению для лучшей визуализации
plt.tight_layout()

# Показать график
plt.show()