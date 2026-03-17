import numpy as np
import matplotlib.pyplot as plt
from scipy import stats

# Данные первого набора (7 точек)
U1 = np.array([0.5785, 0.6909, 0.7896, 0.6295, 0.7409, 0.653, 0.75])
lnI1 = np.array([-3.036554268, -1.087909766, 0.264431357,
                 -2.092567309, -0.270575888, -1.677609693, -0.146194084])

# Данные второго набора (10 точек)
U2 = np.array([0.7484, 0.7914, 0.8624, 0.8915, 0.924, 0.9567,
               0.9955, 0.9227, 0.8557])
lnI2 = np.array([-2.95401468, -2.325649033, -1.33279151, -0.967373522,
                 -0.583862375, -0.224106515, 0.142662081, -0.493952119,
                 -1.363906842])

# Данные третьего набора (11 точек)
U3 = np.array([1.0395, 1.0939, 1.1282, 1.1524, 1.1735, 1.2119,
               1.2314, 1.2651, 1.2719, 1.285])
lnI3 = np.array([-2.679025522, -2.180544467, -1.919706484, -1.735908576,
                 -1.564942673, -1.327874521, -1.189576924, -0.997202567,
                 -0.93450562, -0.83149013])

# Функция для выполнения регрессии и возврата параметров
def regression(x, y):
    slope, intercept, r_value, p_value, std_err = stats.linregress(x, y)
    r2 = r_value**2
    return slope, intercept, r2

# Расчёт для каждого набора
slope1, intercept1, r2_1 = regression(U1, lnI1)
slope2, intercept2, r2_2 = regression(U2, lnI2)
slope3, intercept3, r2_3 = regression(U3, lnI3)

# Подготовка точек для прямых
U_fit = np.linspace(min(U1.min(), U2.min(), U3.min()),
                    max(U1.max(), U2.max(), U3.max()), 200)
fit1 = slope1 * U_fit + intercept1
fit2 = slope2 * U_fit + intercept2
fit3 = slope3 * U_fit + intercept3

# Построение графика
plt.figure(figsize=(10, 7))
plt.plot(U_fit, fit1, zorder=1, color='lightcoral')
plt.scatter(U1, lnI1, color='red', marker='o', zorder=2, label='Без фильтров')


plt.plot(U_fit, fit2, zorder=1, color='deepskyblue')
plt.scatter(U2, lnI2, color='blue', marker='o', zorder=2, label='1 фильтр')


plt.plot(U_fit, fit3, zorder=1, color='lime')
plt.scatter(U3, lnI3, color='green', marker='o', zorder=2, label='2 фильтра')


plt.xlabel(r'$U_{МКП}$, кВ')
plt.ylabel('ln(I)')
# plt.title('Зависимость ln(I) от напряжения U для трёх наборов данных')
plt.grid(True, linestyle=':', alpha=0.7)
plt.legend(loc='best', fontsize=9)
plt.tight_layout()
plt.show()

# Вывод параметров в консоль
# print("Результаты линейной регрессии:")
# print(f"Набор 1: ln(I) = {slope1:.4f} * U + {intercept1:.4f}, R² = {r2_1:.6f}")
# print(f"Набор 2: ln(I) = {slope2:.4f} * U + {intercept2:.4f}, R² = {r2_2:.6f}")
# print(f"Набор 3: ln(I) = {slope3:.4f} * U + {intercept3:.4f}, R² = {r2_3:.6f}")