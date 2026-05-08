import numpy as np
import matplotlib.pyplot as plt
from scipy import stats

# Данные
wavelength = np.array([404.7, 435.8, 491.6, 546.1, 577.0, 579.1])  # нм
sin_phi_minus1 = np.array([0.2005, 0.2193, 0.2594, 0.2662, 0.2844, 0.2834])
sin_phi_plus1 = np.array([0.2013, 0.2196, 0.2593, 0.2655, 0.2834, 0.2824])

# Индексы точек для аппроксимации (без 491.6 нм - это индекс 2)
indices_approx = [0, 1, 3, 4, 5]
indices_outlier = [2]  # точка 491.6 нм

# Создаем фигуру с двумя графиками рядом
fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(14, 5))

# ===== График для -1 порядка =====
# Аппроксимация без точки 491.6 нм
slope_minus1, intercept_minus1, r_value_minus1, p_value_minus1, std_err_minus1 = \
    stats.linregress(wavelength[indices_approx], sin_phi_minus1[indices_approx])

# Создаем линию аппроксимации
x_line = np.array([400, 590])
y_line_minus1 = slope_minus1 * x_line + intercept_minus1

# Формируем уравнение прямой для легенды
eq_minus1 = f'y = {slope_minus1:.6f}x + {intercept_minus1:.4f}'

# Строим все точки
ax1.scatter(wavelength, sin_phi_minus1, color='blue', label='Экспериментальные точки', s=50)
# Выделяем точку 491.6 нм красным цветом
ax1.scatter(wavelength[indices_outlier], sin_phi_minus1[indices_outlier], 
            color='red', s=80, marker='x', zorder=5)
# Строим линию аппроксимации
ax1.plot(x_line, y_line_minus1, 'g-', label=f'{eq_minus1}')

ax1.set_xlabel('Длина волны λ, нм')
ax1.set_ylabel('sin φ')
ax1.set_title('Порядок m = -1')
ax1.legend(fontsize=9)
ax1.grid(True, alpha=0.3)

# ===== График для +1 порядка =====
# Аппроксимация без точки 491.6 нм
slope_plus1, intercept_plus1, r_value_plus1, p_value_plus1, std_err_plus1 = \
    stats.linregress(wavelength[indices_approx], sin_phi_plus1[indices_approx])

# Создаем линию аппроксимации
y_line_plus1 = slope_plus1 * x_line + intercept_plus1

# Формируем уравнение прямой для легенды
eq_plus1 = f'y = {slope_plus1:.6f}x + {intercept_plus1:.4f}'

# Строим все точки
ax2.scatter(wavelength, sin_phi_plus1, color='blue', label='Экспериментальные точки', s=50)
# Выделяем точку 491.6 нм красным цветом
ax2.scatter(wavelength[indices_outlier], sin_phi_plus1[indices_outlier], 
            color='red', s=80, marker='x', zorder=5)
# Строим линию аппроксимации
ax2.plot(x_line, y_line_plus1, 'g-', label=f'{eq_plus1}')

ax2.set_xlabel('Длина волны λ, нм')
ax2.set_ylabel('sin φ')
ax2.set_title('Порядок m = +1')
ax2.legend(fontsize=9)
ax2.grid(True, alpha=0.3)

plt.tight_layout()
plt.show()

# Вывод параметров аппроксимации
print("Параметры аппроксимации:")
print(f"\nПорядок m = -1:")
print(f"  Уравнение: sin(φ) = {slope_minus1:.6f}·λ {intercept_minus1:+.6f}")
print(f"  Угловой коэффициент: {slope_minus1:.6f} нм⁻¹")
print(f"  Свободный член: {intercept_minus1:.6f}")
print(f"  R² = {r_value_minus1**2:.6f}")
print(f"  Период решётки d = 1/slope = {1/slope_minus1:.2f} нм = {1/slope_minus1*1e-3:.2f} мкм")

print(f"\nПорядок m = +1:")
print(f"  Уравнение: sin(φ) = {slope_plus1:.6f}·λ {intercept_plus1:+.6f}")
print(f"  Угловой коэффициент: {slope_plus1:.6f} нм⁻¹")
print(f"  Свободный член: {intercept_plus1:.6f}")
print(f"  R² = {r_value_plus1**2:.6f}")
print(f"  Период решётки d = 1/slope = {1/slope_plus1:.2f} нм = {1/slope_plus1*1e-3:.2f} мкм")

print(f"\nСредний период решётки: {(1/slope_minus1 + 1/slope_plus1)/2:.2f} нм = {(1/slope_minus1 + 1/slope_plus1)/2*1e-3:.2f} мкм")