import numpy as np
import matplotlib.pyplot as plt

# Универсальная газовая постоянная
R = 8.314  # Дж/(моль·К)

# Вириальные коэффициенты для CO₂ (примерные значения)
# B(T) в м³/моль, C(T) в м⁶/моль²
def B(T):
    """Второй вириальный коэффициент для CO₂"""
    return (0.042 - 150/T - 4.2e4/T**3) * 0.001  # Переводим из л/моль в м³/моль

def C(T):
    """Третий вириальный коэффициент для CO₂"""
    return (3000/T**2) * 1e-6  # Переводим из л²/моль² в м⁶/моль²

# Критические параметры CO₂ (для справки)
T_crit = 304.13  # K
P_crit = 7.377e6  # Па
V_crit = 94e-6    # м³/моль (0.094 л/моль)

# Функция давления по уравнению Камерлинга-Оннеса
def virial_pressure(V, T):
    """Давление по вириальному уравнению до третьего коэффициента"""
    return (R * T / V) * (1 + B(T)/V + C(T)/V**2)

# Создаем диапазон объемов
V_min = 0.0001  # м³/моль (0.1 л/моль)
V_max = 0.01    # м³/моль (10 л/моль)
V = np.linspace(V_min, V_max, 1000)

# Создаем график
plt.figure(figsize=(10, 7))
plt.title("Изотермы уравнения Камерлинга-Оннеса для CO₂", fontsize=14)
plt.xlabel("Объем V, м³/моль", fontsize=12)
plt.ylabel("Давление P, МПа", fontsize=12)
plt.grid(True, linestyle='--', alpha=0.7)

# Температуры для изотерм
temperatures = [280, T_crit, 320, 350]  # K
colors = ['blue', 'red', 'green', 'purple']
labels = [
    f'T = 280 K',
    f'T = {T_crit} K',
    f'T = 320 K',
    f'T = 350 K'
]

# Строим изотермы
for T, color, label in zip(temperatures, colors, labels):
    P = virial_pressure(V, T)
    plt.plot(V, P/1e6, color=color, linewidth=2, label=label)  # Давление в МПа

# Добавляем изотерму идеального газа для сравнения
P_ideal = R * T_crit / V
plt.plot(V, P_ideal/1e6, 'r--', linewidth=1, label=f'Идеальный газ (при {T_crit} K)')

# # Добавляем критическую точку
# plt.scatter([V_crit], [P_crit/1e6], color='black', s=80, zorder=5, 
#            label=f'Критическая точка CO₂ ({V_crit:.5f} м³/моль, {P_crit/1e6:.2f} МПа)')

# Настраиваем легенду и отображение
plt.legend(fontsize=10, loc='upper right')
plt.xlim(V_min, V_max)
plt.ylim(0, 15)  # Ограничение по давлению
plt.tight_layout()

# Показать график
plt.savefig('virial_isotherms.png', dpi=300)
plt.show()

# Выводим значения вириальных коэффициентов
print("Вириальные коэффициенты для разных температур:")
for T in temperatures:
    print(f"T = {T} K: B = {B(T):.6f} м³/моль, C = {C(T):.9f} м⁶/моль²")