import numpy as np
import matplotlib.pyplot as plt

# Данные для построения графика
I_h = np.array([2.4, 2.5, 2.6, 2.7, 2.8, 2.9])  # ток накала в А

# Анодные токи для разных напряжений на аноде (в мкА)
I_a_10V = np.array([0.162, 0.478, 0.91, 1.67, 2.06, 2.8]) * 1e-6
I_a_30V = np.array([0.171, 0.51, 0.995, 2.85, 6.2, 6.45]) * 1e-6
I_a_50V = np.array([0.176, 0.53, 1.04, 3.05, 6.75, 7.0]) * 1e-6
I_a_70V = np.array([0.181, 0.547, 1.07, 3.17, 7.13, 7.36]) * 1e-6
I_a_140V = np.array([0.192, 0.589, 1.155, 3.41, 8.05, 8.53]) * 1e-6

# Подготовка данных
voltages = ['10 В', '30 В', '50 В', '70 В', '140 В']
I_a_data = [I_a_10V, I_a_30V, I_a_50V, I_a_70V, I_a_140V]

# Создание фигуры
plt.figure(figsize=(10, 7))

# Используем градиент цветов плазмы для лучшего визуального разделения
for i, (I_a, voltage) in enumerate(zip(I_a_data, voltages)):
    # Цвет становится темнее с увеличением напряжения
    color_intensity = 0.2 + 0.6 * i/len(I_a_data)
    color = plt.cm.plasma(color_intensity)
    
    # Используем semilogy для логарифмической шкалы по Y
    plt.semilogy(I_h, I_a * 1e6, 'o-', color=color, linewidth=3, 
                 markersize=10, markeredgecolor='white', markeredgewidth=2,
                 label=voltage, alpha=0.9)

# Настройка осей
plt.xlabel('Ток накала, А', fontsize=13)
plt.ylabel('Анодный ток, мкА', fontsize=13)

# Настройка сетки (для логарифмической шкалы используем which='both')
plt.grid(True, which='both', alpha=0.4, linestyle='-')

# Настройка легенды
plt.legend(loc='upper left', fontsize=11, frameon=True, shadow=True)

# Установка пределов осей
plt.xlim(2.35, 2.95)
plt.ylim(0.15, 10)  # Для логарифмической шкалы

# Настройка меток осей
plt.xticks(np.arange(2.4, 3.0, 0.1))

# Для логарифмической шкалы задаем удобные метки
plt.yticks([0.2, 0.5, 1, 2, 5, 10], 
           ['0.2', '0.5', '1', '2', '5', '10'])

# Добавление подписей к некоторым точкам для наглядности
# (раскомментируйте при необходимости)
# for i, I_a in enumerate(I_a_data):
#     # Подписываем только первую и последнюю кривую
#     if i == 0 or i == len(I_a_data)-1:
#         for j, (x, y) in enumerate(zip(I_h, I_a * 1e6)):
#             if j % 2 == 0:  # Подписываем только каждую вторую точку
#                 plt.annotate(f'{y:.2f}', (x, y), 
#                             xytext=(0, 10), textcoords='offset points',
#                             ha='center', va='bottom', fontsize=8, alpha=0.7)

plt.tight_layout()

# Сохранение графика
plt.savefig('anode_current_log_beautiful.png', dpi=300, bbox_inches='tight', 
            facecolor='white', edgecolor='none')

plt.show()