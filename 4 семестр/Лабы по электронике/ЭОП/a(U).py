import numpy as np
import matplotlib.pyplot as plt
from scipy import stats

# Исходные данные
U = np.array([0.5785, 0.6909, 0.7896, 0.6295, 0.7409, 0.653, 0.75])
ln_alpha = np.array([3.465735903, 5.505034774, 6.589971016,
                      4.162862784, 5.821814578, 4.59887381, 6.024397129])

# Линейная регрессия
slope, intercept, r_value, p_value, std_err = stats.linregress(U, ln_alpha)
r_squared = r_value**2

# Подготовка точек для прямой регрессии
U_fit = np.linspace(min(U), max(U), 100)
ln_alpha_fit = slope * U_fit + intercept

# Построение графика
plt.figure(figsize=(8, 6))
plt.scatter(U, ln_alpha, color='red', label='Экспериментальные точки')
plt.plot(U_fit, ln_alpha_fit, color='blue', 
         label=f'Аппроксимация: ln(α) = {slope:.3f}·U - {-intercept:.3f}')

plt.xlabel(r'$U_{МКП}$, кВ')
plt.ylabel('ln(α)')
# plt.title('Зависимость ln(α) от напряжения U')
plt.grid(True, linestyle='--', alpha=0.7)
plt.legend()
plt.tight_layout()
plt.show()

# Вывод параметров в консоль
print(f'Уравнение регрессии: ln(α) = {slope:.4f} * U + {intercept:.4f}')
print(f'Коэффициент детерминации R² = {r_squared:.6f}')
print(f'Стандартная ошибка наклона: {std_err:.6f}')