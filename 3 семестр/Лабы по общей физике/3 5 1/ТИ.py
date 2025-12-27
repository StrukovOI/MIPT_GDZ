import matplotlib.pyplot as plt
import numpy as np

# Данные из таблицы
I_p = [5.167, 3.048, 1.672]  # мА
kT_e = [2.48, 2.77, 2.83]    # эВ
T_e = [28.78, 32.14, 32.84]  # ×10³ К

# Погрешности
delta_I = 0.005  # мА
delta_T_e = [1.28, 0.93, 0.58]  # ×10³ К

# Построение графика
plt.figure(figsize=(10, 6))
plt.errorbar(I_p, T_e, xerr=delta_I, yerr=delta_T_e, 
             fmt='o', markersize=8, capsize=5, capthick=2,
             label='Экспериментальные точки')

# Настройки графика
plt.xlabel('$I_p$, мА', fontsize=12)
plt.ylabel('$T_e$, $10^3$ К', fontsize=12)
# plt.title('Зависимость температуры электронов от тока разряда', fontsize=14)
plt.grid(True, linestyle='--', alpha=0.7)
# plt.legend(fontsize=11)

# Добавляем аннотации с значениями
# for i, (x, y, kt) in enumerate(zip(I_p, T_e, kT_e)):
#     plt.annotate(f'$kT_e$ = {kt} эВ', (x, y), 
#                 xytext=(10, 5), textcoords='offset points',
#                 fontsize=10, bbox=dict(boxstyle="round,pad=0.3", fc="white", alpha=0.7))

plt.tight_layout()
plt.show()