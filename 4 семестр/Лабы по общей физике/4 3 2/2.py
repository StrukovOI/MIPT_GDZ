import numpy as np
import matplotlib.pyplot as plt

# Данные: 1/ν (1/МГц) и Λ (мм)
x = np.array([0.878024795, 0.695913595, 0.677314043, 0.613869774, 0.590489575, 0.562673374, 0.479717542])
y = np.array([1.378205128, 1.217948718, 1.185897436, 1.068376068, 1.025641026, 0.961538462, 0.820512821])

# Расчёт коэффициентов линейной регрессии y = a*x + b
a, b = np.polyfit(x, y, 1)  # a — искомый наклон
print(f"Коэффициент наклона a = {a:.6f} мм·МГц")

# Построение графика
plt.figure(figsize=(8, 6))
plt.scatter(x, y, color='red', label='Экспериментальные точки')
plt.plot(x, a*x + b, color='blue', label=f'Аппроксимация: y = {a:.3f}x + {b:.3f}')
plt.xlabel('1/ν, 1/МГц')
plt.ylabel('Λ, мм')
# plt.title('Зависимость Λ от обратной частоты')
plt.grid(True)
plt.legend()
plt.show()