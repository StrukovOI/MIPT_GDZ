import matplotlib.pyplot as plt
import numpy as np

# Данные из таблицы
I_p = [5.167, 3.048, 1.672]  # мА
n_e = [16.3, 9.89, 5.85]     # ×10¹⁵ м⁻³
delta_n_e = [0.8, 0.35, 0.12] # ×10¹⁵ м⁻³

# Погрешности
delta_I = 0.005  # мА

# Построение графика
plt.figure(figsize=(10, 6))
plt.errorbar(I_p, n_e, xerr=delta_I, yerr=delta_n_e, 
             fmt='s', markersize=8, capsize=5, capthick=2,
             label='Экспериментальные точки', color='red')

# Настройки графика
plt.xlabel('$I_p$, мА', fontsize=12)
plt.ylabel('$n_e$, $10^{15}$ м$^{-3}$', fontsize=12)
# plt.title('Зависимость концентрации электронов от тока разряда', fontsize=14)
plt.grid(True, linestyle='--', alpha=0.7)
# plt.legend(fontsize=11)

# Добавляем аннотации с дополнительными параметрами
# additional_params = [
#     f'$ω_p$={7.14}×10⁹ рад/с\n$r_D$={9.4}×10⁻⁶ м\n$N_D$={57}',
#     f'$ω_p$={5.57}×10⁹ рад/с\n$r_D$={12.0}×10⁻⁶ м\n$N_D$={78}',
#     f'$ω_p$={4.28}×10⁹ рад/с\n$r_D$={15.6}×10⁻⁶ м\n$N_D$={93}'
# ]

# for i, (x, y, params) in enumerate(zip(I_p, n_e, additional_params)):
#     plt.annotate(params, (x, y), 
#                 xytext=(15, 15), textcoords='offset points',
#                 fontsize=9, bbox=dict(boxstyle="round,pad=0.3", fc="white", alpha=0.7))

plt.tight_layout()
plt.show()