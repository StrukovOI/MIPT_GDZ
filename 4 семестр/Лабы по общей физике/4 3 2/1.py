import matplotlib.pyplot as plt

# Данные
m = [-2, -1, 0, 1, 2]
frequencies = [1.044, 1.248, 1.504, 2.014]

# Значения Y для каждой частоты (порядок столбцов)
y1 = [-61, -30, 4, 35, 73]       # для 1.044
y2 = [-72, -33, 4, 47, 92]       # для 1.24837
y3 = [-76, -41, 4, 47, 89]       # для 1.504
y4 = [None, -60, 4, 75, None]    # для 2.014 (неполные данные)

# Построение графиков
plt.figure(figsize=(10, 6))
plt.plot(m, y1, 'o-', label=f'{frequencies[0]} МГц')
plt.plot(m, y2, 'o-', label=f'{frequencies[1]} МГц')
plt.plot(m, y3, 'o-', label=f'{frequencies[2]} МГц')
plt.plot(m, y4, 'o-', label=f'{frequencies[3]} МГц')

# Настройки осей и подписи
plt.xlabel('Номер полосы m')
plt.ylabel('Координата Y')
# plt.title('Зависимость координаты Y от номера дифракционной полосы')
plt.grid(True)
plt.legend()
plt.show()