import matplotlib.pyplot as plt
import numpy as np

# Данные: D в мм, d в мкм
D = [5.36, 1.9]
d = [24.85, 49.37]

# Вычисляем 1/D (в 1/мм)
inv_D = [1 / val for val in D]

# Построение графика
plt.figure(figsize=(8, 6))
plt.plot(inv_D, d, 'ro', markersize=8, label='Экспериментальные точки')

# Аппроксимация прямой, проходящей через обе точки (линейная интерполяция)
# Используем polyfit для получения коэффициентов прямой y = a*x + b
coeffs = np.polyfit(inv_D, d, 1)  # степень 1
a, b = coeffs
print(f"Уравнение прямой: d = {a:.2f}*(1/D) + {b:.2f}")

# Генерируем точки для прямой в диапазоне от 0 до max(inv_D) с запасом
x_line = np.linspace(0, max(inv_D)*1.2, 100)
y_line = a * x_line + b
plt.plot(x_line, y_line, 'b-', label=f'Аппроксимация: d = {a:.2f}·(1/D) + {b:.2f}')

# Оформление
plt.xlabel('1/D, 1/мм')
plt.ylabel('d, мкм')
# plt.title('Зависимость периода решётки от обратной ширины щели')
plt.grid(True)
plt.legend()
plt.xlim(0, max(inv_D)*1.2)
plt.ylim(0, max(d)*1.2)

# Подписи точек
for i, (x, y) in enumerate(zip(inv_D, d)):
    plt.text(x, y, f'  D={D[i]} мм', verticalalignment='bottom')

plt.show()