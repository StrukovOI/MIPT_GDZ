import matplotlib.pyplot as plt
import numpy as np

# Новые данные
x = np.array([2.857142857, 2.5, 2.222222222, 2, 1.666666667, 1.428571429, 1.25, 1.111111111])  # 1/d, 1/мм
y = np.array([1.164262295, 1.109344262, 0.95557377, 0.835852459, 0.812786885, 0.648032787, 0.443737705, 0.490967213])  # ρ, мм

# Линейная аппроксимация
coefficients = np.polyfit(x, y, 1)
k = coefficients[0]
b = coefficients[1]
y_fit = k * x + b

# Ручной расчёт R^2
ss_res = np.sum((y - y_fit) ** 2)
ss_tot = np.sum((y - np.mean(y)) ** 2)
r2 = 1 - (ss_res / ss_tot)

# Построение графика
plt.figure(figsize=(8, 5))
plt.scatter(x, y, color='blue', label='Экспериментальные точки')
plt.plot(x, y_fit, color='red', linestyle='-', label=f'Линейная аппроксимация: ρ = {k:.3f}·(1/d) + {b:.3f}')

plt.xlabel('1/d, 1/мм')
plt.ylabel('ρ, мм')
# plt.title('Зависимость ρ от 1/d с линейной аппроксимацией (новые данные)')
plt.grid(True)
plt.legend()

# plt.text(0.05, 0.95, f'$R^2 = {r2:.4f}$', transform=plt.gca().transAxes,
#          fontsize=12, verticalalignment='top', bbox=dict(boxstyle='round', facecolor='white', alpha=0.8))

plt.tight_layout()
plt.show()

print(f"Уравнение прямой: ρ = {k:.4f} * (1/d) + {b:.4f}")
print(f"Коэффициент детерминации R^2 = {r2:.4f}")