import numpy as np
import matplotlib.pyplot as plt

# Нормализованные параметры для уравнения Клаузиуса
a = 1.0       # Сила притяжения
b = 0.1       # Собственный объем молекул
c = 0.05      # Дополнительный параметр объема
R = 1.0       # Газовая постоянная (нормализована)

# Уравнение Клаузиуса
def pressure(V, T):
    return (R * T / (V - b)) - (a / (T * (V + c)**2))

# Диапазон объемов (исключая V <= b)
V_min = b + 0.01*b  # Начало диапазона
V_max = 10*b         # Конец диапазона
V = np.linspace(V_min, V_max, 1000)

# Температуры для изотерм (без привязки к критическим)
temperatures = [1.2, 1.3, 1.5, 2.0]  # Нормализованные значения
colors = ['#1f77b4', '#ff7f0e', '#2ca02c', '#d62728']
labels = [f'T = {T:.2f}' for T in temperatures]

# Построение графика
plt.figure(figsize=(12, 8))
plt.title("Изотермы уравнения Клаузиуса", fontsize=16)
plt.xlabel("Молярный объем $V$", fontsize=14)
plt.ylabel("Давление $P$", fontsize=14)

# Расчёт и отрисовка изотерм
for T, color, label in zip(temperatures, colors, labels):
    P = pressure(V, T)
    plt.plot(V, P, color=color, linewidth=2, label=label)

# Добавление идеального газа для сравнения
P_ideal = R * temperatures[1] / V  # Идеальный газ при T=1
plt.plot(V, P_ideal, 'k--', linewidth=1, label='Идеальный газ (T = 1)')

# Вертикальная линия V = b
# plt.axvline(b, color='red', linestyle='--', linewidth=1, label='V = b')

# Настройки графика
plt.legend(fontsize=12, loc='upper right')
plt.grid(True, linestyle='--', alpha=0.7)
plt.xlim(V_min, V_max)
plt.ylim(-0.5, 5)  # Ограничение по давлению для лучшей визуализации
plt.tight_layout()

# Сохранение и отображение
plt.savefig('clausius_isotherms_no_critical.png', dpi=300, bbox_inches='tight')
plt.show()