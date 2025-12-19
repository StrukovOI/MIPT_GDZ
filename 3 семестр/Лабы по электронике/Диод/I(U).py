# import numpy as np
# import matplotlib.pyplot as plt

# # Данные из таблицы (I в A, U в B)
# I = np.array([0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9, 1.0, 1.1, 1.2, 1.3, 1.4, 1.5, 1.6, 1.7, 1.8, 1.9, 2.0, 2.1, 2.2, 2.3, 2.4, 2.5, 2.6, 2.7, 2.8, 2.9])
# U = np.array([0.022, 0.044, 0.0693, 0.0975, 0.13, 0.17, 0.225, 0.29, 0.381, 0.47, 0.656, 0.76, 0.911, 0.974, 1.101, 1.294, 1.389, 1.6, 2.09, 2.26, 2.5, 2.8, 3.03, 3.24, 3.5, 3.78, 4.14, 4.44, 4.66])

# # Создание графика
# plt.figure(figsize=(10, 6))
# plt.plot(U, I, 'bo-', linewidth=1, markersize=4, label='Экспериментальные точки')

# # Настройка графика
# # plt.title('Зависимость тока накала от напряжения накала', fontsize=14, fontweight='bold')
# plt.xlabel('Напряжение накала, В', fontsize=12)
# plt.ylabel('Ток накала, А', fontsize=12)
# plt.grid(True, alpha=0.3)

# # Добавление сетки
# plt.minorticks_on()
# plt.grid(which='major', linestyle='-', linewidth='0.5')
# plt.grid(which='minor', linestyle=':', linewidth='0.5')

# # Добавление легенды
# plt.legend(fontsize=10)

# # Автоматическая настройка пределов осей
# plt.xlim(left=0)
# plt.ylim(bottom=0)

# plt.tight_layout()
# plt.show()







import numpy as np
import matplotlib.pyplot as plt

# Данные: мощность P в Вт, сопротивление R в Ом
P = np.array([0.0022, 0.0088, 0.02079, 0.039, 0.065, 0.102, 0.1575, 0.232, 0.3429, 
              0.47, 0.7216, 0.912, 1.1843, 1.3636, 1.6515, 2.0704, 2.3613, 2.88, 
              3.971, 4.52, 5.25, 6.16, 6.969, 7.776, 8.75, 9.828, 11.178, 12.432, 13.514])

R = np.array([0.22, 0.22, 0.231, 0.24375, 0.26, 0.283333333, 0.321428571, 0.3625, 
              0.423333333, 0.47, 0.596363636, 0.633333333, 0.700769231, 0.695714286, 
              0.734, 0.80875, 0.817058824, 0.888888889, 1.1, 1.13, 1.19047619, 
              1.272727273, 1.317391304, 1.35, 1.4, 1.453846154, 1.533333333, 
              1.585714286, 1.606896552])

# Создание графика
plt.figure(figsize=(10, 6))
plt.plot(P, R, 'bo-', linewidth=1, markersize=4, label='Экспериментальные данные')

# Настройка графика
# plt.title('Зависимость сопротивления катода от приложенной мощности', fontsize=14, fontweight='bold')
plt.xlabel('Мощность, Вт', fontsize=12)
plt.ylabel('Сопротивление катода, Ом', fontsize=12)
plt.grid(True, alpha=0.3)

# Добавление сетки
plt.minorticks_on()
plt.grid(which='major', linestyle='-', linewidth='0.5')
plt.grid(which='minor', linestyle=':', linewidth='0.5')

# Добавление легенды
plt.legend(fontsize=10, loc='lower right')

# Автоматическая настройка пределов осей
plt.xlim(left=0)
plt.ylim(bottom=0.2, top=1.7)

# Форматирование осей для лучшей читаемости
plt.xticks(np.arange(0, 15, 1))
plt.yticks(np.arange(0.2, 1.7, 0.1))

plt.tight_layout()
plt.show()

# Дополнительно: график в логарифмическом масштабе по оси X
# plt.figure(figsize=(10, 6))
# plt.plot(P, R, 'bo-', linewidth=2, markersize=6, label='Экспериментальные данные')
# plt.title('Зависимость сопротивления катода от приложенной мощности\n(логарифмический масштаб по оси X)', fontsize=14, fontweight='bold')
# plt.xlabel('Мощность, Вт (логарифмическая шкала)', fontsize=12)
# plt.ylabel('Сопротивление катода, Ом', fontsize=12)
# plt.grid(True, alpha=0.3, which='both')
# plt.xscale('log')
# plt.legend(fontsize=10, loc='lower right')
# plt.tight_layout()
# plt.show()