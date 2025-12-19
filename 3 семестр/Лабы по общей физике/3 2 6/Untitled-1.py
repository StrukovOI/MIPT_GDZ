import numpy as np
import matplotlib.pyplot as plt
from scipy import stats

# Данные из таблицы
r_r0_squared = np.array([260.1, 294.5, 331.2, 370.0, 415.2, 462.8, 512.7, 
                          564.9, 742.0, 866.8, 998.6, 1137.4, 1391.3, 1664.1, 
                          1955.9, 2266.6, 2596.3, 2944.0])

inv_theta_squared = np.array([0.23, 0.25, 0.27, 0.32, 0.36, 0.37, 0.40, 0.43, 
                               0.50, 0.64, 0.69, 0.86, 0.94, 1.06, 1.29, 1.42, 
                               1.69, 1.88])

sigma_inv_theta_squared = np.array([0.02, 0.02, 0.02, 0.03, 0.03, 0.03, 0.03, 
                                     0.04, 0.04, 0.05, 0.05, 0.07, 0.07, 0.09, 
                                     0.11, 0.13, 0.17, 0.20])

# Линейная аппроксимация (учитываем погрешности по методу наименьших квадратов)
# Используем взвешенную линейную регрессию
weights = 1 / (sigma_inv_theta_squared ** 2)
slope, intercept, r_value, p_value, std_err = stats.linregress(
    r_r0_squared, inv_theta_squared
)

# Для сравнения - взвешенная регрессия
A = np.vstack([r_r0_squared, np.ones(len(r_r0_squared))]).T
w_slope, w_intercept = np.linalg.lstsq(
    A * weights[:, np.newaxis], 
    inv_theta_squared * weights, 
    rcond=None
)[0]

# Создание предсказанных значений
x_fit = np.linspace(min(r_r0_squared), max(r_r0_squared), 100)
y_fit = slope * x_fit + intercept
y_fit_weighted = w_slope * x_fit + w_intercept

# Построение графика
plt.figure(figsize=(10, 6))

# Точки с погрешностями
plt.errorbar(r_r0_squared, inv_theta_squared, 
             yerr=sigma_inv_theta_squared, 
             fmt='o', color='blue', 
             ecolor='red', capsize=5, 
             label='Экспериментальные данные', 
             markersize=6)

# Линии аппроксимации
plt.plot(x_fit, y_fit, 'g-', linewidth=2, 
         label=f'Линейная аппроксимация (обычная)\ny = {slope:.5f}x + {intercept:.3f}')
plt.plot(x_fit, y_fit_weighted, 'm--', linewidth=2, 
         label=f'Линейная аппроксимация (взвешенная)\ny = {w_slope:.5f}x + {w_intercept:.3f}')

# Настройка графика
plt.xlabel('$(R+R_0)^2$, кОм$^2$', fontsize=12)
plt.ylabel('$1/\\Theta^2$', fontsize=12)
plt.title('Зависимость $1/\\Theta^2$ от $(R+R_0)^2$', fontsize=14)
plt.grid(True, alpha=0.3)
plt.legend(fontsize=10)

# Добавление статистики
plt.text(0.05, 0.95, 
         f'Коэффициент корреляции (обычный): {r_value:.4f}\n'
         f'Стандартная ошибка: {std_err:.5f}',
         transform=plt.gca().transAxes,
         verticalalignment='top',
         bbox=dict(boxstyle='round', facecolor='wheat', alpha=0.5))

plt.tight_layout()
plt.show()

# Вывод параметров аппроксимации
print("Результаты аппроксимации:")
print(f"1. Обычная линейная регрессия:")
print(f"   Наклон (k) = {slope:.6f} ± {std_err:.6f}")
print(f"   Сдвиг (b) = {intercept:.6f}")
print(f"   Коэффициент корреляции R = {r_value:.6f}")
print(f"   R² = {r_value**2:.6f}")
print()
print(f"2. Взвешенная линейная регрессия (с учетом погрешностей):")
print(f"   Наклон (k) = {w_slope:.6f}")
print(f"   Сдвиг (b) = {w_intercept:.6f}")

# Расчет остатков для оценки качества аппроксимации
residuals = inv_theta_squared - (slope * r_r0_squared + intercept)
print(f"\n3. Статистика остатков (обычная регрессия):")
print(f"   Средний остаток: {np.mean(residuals):.6f}")
print(f"   СКО остатков: {np.std(residuals):.6f}")