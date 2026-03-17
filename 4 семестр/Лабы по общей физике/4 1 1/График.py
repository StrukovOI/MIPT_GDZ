import numpy as np
import matplotlib.pyplot as plt
from scipy.optimize import curve_fit

# Исходные данные: L (см), l (см)
L_data = np.array([76.8, 88.8, 68.7, 60.3, 55.0, 50.0])
l_data = np.array([52.6, 65.2, 43.7, 34.9, 28.93, 22.6])

# Погрешность измерения расстояний (1 мм = 0.1 см)
sigma_L = 0.1
sigma_l = 0.1

# Вычисляем Y = L^2 - l^2 и её погрешность
Y = L_data**2 - l_data**2
sigma_Y = 2 * np.sqrt((L_data * sigma_L)**2 + (l_data * sigma_l)**2)

# Определяем модель: Y = k * L - b  (линейная функция)
def linear(L, k, b):
    return k * L - b

# Выполняем взвешенную подгонку
popt, pcov = curve_fit(linear, L_data, Y, sigma=sigma_Y, absolute_sigma=True)
k, b = popt
sigma_k, sigma_b = np.sqrt(np.diag(pcov))
cov_kb = pcov[0, 1]  # ковариация между k и b

# Вывод результатов подгонки
print("Результаты линейной аппроксимации Y = k·L - b:")
print(f"k = {k:.2f} ± {sigma_k:.2f} см")
print(f"b = {b:.1f} ± {sigma_b:.1f} см²")

# Вычисляем D = k^2 - 4b, проверяем знак
D = k**2 - 4*b
if D <= 0:
    print("Ошибка: D ≤ 0, невозможно вычислить f и delta.")
else:
    sqrtD = np.sqrt(D)
    # Фокусное расстояние f и оптический интервал delta
    f = sqrtD / 4
    delta = (k - sqrtD) / 2

    # Частные производные для погрешностей
    df_dk = k / (4 * sqrtD)
    df_db = -1 / (2 * sqrtD)
    ddelta_dk = 0.5 * (1 - k / sqrtD)
    ddelta_db = 1 / sqrtD

    # Погрешности методом распространения ошибок
    sigma_f = np.sqrt((df_dk * sigma_k)**2 + (df_db * sigma_b)**2 +
                      2 * df_dk * df_db * cov_kb)
    sigma_delta = np.sqrt((ddelta_dk * sigma_k)**2 + (ddelta_db * sigma_b)**2 +
                          2 * ddelta_dk * ddelta_db * cov_kb)

    print(f"\nФокусное расстояние системы f = {f:.2f} ± {sigma_f:.2f} см")
    print(f"Оптический интервал δ = {delta:.2f} ± {sigma_delta:.2f} см")

# Построение графика
plt.figure(figsize=(8, 6))
# Экспериментальные точки с погрешностями
plt.errorbar(L_data, Y, yerr=sigma_Y, fmt='o', capsize=5, label='Экспериментальные точки')
# Аппроксимирующая прямая
L_fit = np.linspace(min(L_data)-2, max(L_data)+2, 100)
Y_fit = linear(L_fit, k, b)
plt.plot(L_fit, Y_fit, 'r-', label=f'Аппроксимация: A = {k:.1f}·L – {b:.0f}')
plt.xlabel('L, см')
plt.ylabel('A = L² – l², см²')
# plt.title('Определение параметров составной системы по методу Бесселя')
plt.legend()
plt.grid(True)
plt.show()