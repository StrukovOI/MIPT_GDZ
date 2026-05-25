import numpy as np
import matplotlib.pyplot as plt

# Параметры уравнения Ван-дер-Ваальса для CO2
a = 0.3653  # Па·м⁶/моль² (параметр притяжения)
b = 4.28e-5 # м³/моль (параметр объема)
R = 8.314   # Дж/(моль·К) (универсальная газовая постоянная)

# Критические параметры (рассчитываются из a и b)
T_crit = 8*a/(27*R*b)      # Критическая температура
P_crit = a/(27*b**2)       # Критическое давление
V_crit = 3*b                # Критический объем

print(f"Критическая температура: {T_crit:.2f} K")
print(f"Критическое давление: {P_crit/1e6:.2f} МПа")
print(f"Критический объем: {V_crit*1000:.4f} л/моль")

# Создаем диапазон объемов (исключаем V = b)
V = np.linspace(b*1.05, 10*b, 500)  # от 1.05b до 10b

# Функция для расчета давления по уравнению Ван-дер-Ваальса
def van_der_waals(V, T):
    return R*T/(V - b) - a/V**2

# Создаем график
plt.figure(figsize=(10, 7))
plt.title("Изотермы уравнения Ван-дер-Ваальса для CO₂", fontsize=14)
plt.xlabel("Объем V, м³/моль", fontsize=12)
plt.ylabel("Давление P, МПа", fontsize=12)
plt.grid(True, linestyle='--', alpha=0.7)

# Рассчитываем и строим изотермы для разных температур
temperatures = [0.85*T_crit, T_crit, 1.2*T_crit, 1.5*T_crit]
colors = ['blue', 'red', 'green', 'purple']
labels = [
    f'T = {0.8*T_crit:.1f} K',
    f'T = {T_crit:.1f} K',
    f'T = {1.2*T_crit:.1f} K',
    f'T = {1.5*T_crit:.1f} K'
]

for T, color, label in zip(temperatures, colors, labels):
    P = van_der_waals(V, T)
    plt.plot(V, P/1e6, color=color, linewidth=2, label=label)  # Переводим в МПа

# Добавляем критические точки
plt.scatter([V_crit], [P_crit/1e6], color='black', s=80, zorder=5, 
           label=f'Критическая точка') #({V_crit:.5f} м³/моль, {P_crit/1e6:.2f} МПа)

# Добавляем асимптоту для идеального газа при критической температуре
P_ideal = R*T_crit/V
plt.plot(V, P_ideal/1e6, 'r--', linewidth=1, label=r'Идеальный газ (при T$_{\text{крит}}$)')

# Настраиваем легенду и отображение
plt.legend(fontsize=10)
plt.xlim(V[0], V[-1])
plt.ylim(0, 25)
plt.tight_layout()

# Показать график
plt.show()