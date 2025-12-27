import numpy as np
import matplotlib.pyplot as plt
from scipy.interpolate import CubicSpline

# Данные

# U = [24.729, 21.779, 18.643, 15.934, 12.684, 9.742, 7.643, 5.752, 3.7703, 1.7381, 
#      0.137, -0.845, -2.411, -4.398, -6.32, -8.283, -10.831, -13.312, -16.283, -19.586, -22.467, -25.494]
# I = [24.03, 23.11, 22.09, 21.19, 20.05, 18.93, 17.95, 16.68, 14.15, 8.22, 
#      0.64, -4.42, -11.51, -16.91, -19.29, -20.57, -21.73, -22.77, -23.91, -25.06, -25.93, -26.83]

# U = [24.663, 21.686, 18.705, 15.702, 12.72, 9.706, 7.786, 5.665, 3.752, 1.728, 
#      0.222, -0.865, -2.39, -4.439, -6.617, -8.431, -10.635, -13.661, -16.248, -19.462, -22.264, -25.508]
# I = [15.2, 14.74, 14.11, 13.45, 12.745, 11.95, 11.31, 10.26, 8.29, 4.49, 
#      0.51, -2.59, -6.54, -10.21, -12.18, -13.04, -13.78, -14.59, -15.27, -16.02, -16.61, -17.15]

U = [24.809, 21.869, 18.747, 15.725, 12.884, 9.767, 7.603, 5.725, 3.675, 1.722, 
     0.158, -0.849, -2.389, -4.389, -6.482, -8.365, -10.243, -13.371, -16.364, -19.441, -22.437, -25.143]

I = [9.42, 9.08, 8.67, 8.23, 7.78, 7.27, 6.77, 6.08, 4.69, 2.46, 
     0.12, -1.47, -3.73, -5.89, -7.21, -7.84, -8.28, -8.86, -9.36, -9.84, -10.24, -10.62]

# Погрешности
delta_U = 0.005  # В
delta_I = 0.01   # мкА

# Сортируем данные по напряжению
sorted_data = sorted(zip(U, I))
U_sorted, I_sorted = zip(*sorted_data)

# Строим кубический сплайн для всей ВАХ
cs = CubicSpline(U_sorted, I_sorted)

# Генерируем точки для плавной кривой
U_smooth = np.linspace(min(U_sorted), max(U_sorted), 500)
I_smooth = cs(U_smooth)

# Находим ток насыщения I_н
# Используем точки с наибольшими напряжениями для определения асимптоты
n_points = 5
U_fit = U_sorted[-n_points:]
I_fit = I_sorted[-n_points:]

# Линейная аппроксимация этих точек
A = np.vstack([U_fit, np.ones(len(U_fit))]).T
slope, intercept = np.linalg.lstsq(A, I_fit, rcond=None)[0]

# Ток насыщения - значение при U=0
I_nas = intercept

print(f"Наклон асимптоты: {slope:.3f} мкА/В")
print(f"Ток насыщения I_н = {I_nas:.2f} мкА")

# Построение единого графика
plt.figure(figsize=(12, 8))

# Экспериментальные точки с погрешностями и сплайн
plt.errorbar(U, I, xerr=delta_U, yerr=delta_I, fmt='bo', markersize=6, 
             capsize=3, capthick=1, label='Экспериментальные точки')
plt.plot(U_smooth, I_smooth, 'r-', linewidth=2, label='ВАХ')

# Асимптота
# Продлеваем асимптоту до U=0 и немного в отрицательную область для наглядности
U_asymptote = np.linspace(-10, max(U_sorted), 100)
I_asymptote = slope * U_asymptote + intercept
plt.plot(U_asymptote, I_asymptote, 'g--', linewidth=2, 
         label=f'Асимптота: $I$ = {slope:.3f} $U$ + {intercept:.2f}')

# Точка пересечения с осью тока (ток насыщения)
plt.axvline(x=0, color='gray', linestyle=':', alpha=0.7)
plt.axhline(y=I_nas, color='gray', linestyle=':', alpha=0.7)
plt.plot(0, I_nas, 'ro', markersize=7, markeredgecolor='black', 
         label=f'Ток насыщения $I_н$ = {I_nas:.2f} мкА')

# Подписи и оформление
plt.xlabel('U, В', fontsize=12)
plt.ylabel('I, мкА', fontsize=12)
plt.title('Вольт-амперная характеристика двойного зонда', fontsize=14)
plt.legend(fontsize=11)
plt.grid(True, linestyle='--', alpha=0.7)

plt.tight_layout()
plt.show()

# Оценка погрешности методом бутстрэпа
n_bootstrap = 1000
I_nas_bootstrap = []

for _ in range(n_bootstrap):
    indices = np.random.choice(range(len(U_fit)), size=len(U_fit), replace=True)
    U_bs = [U_fit[i] for i in indices]
    I_bs = [I_fit[i] for i in indices]
    
    A_bs = np.vstack([U_bs, np.ones(len(U_bs))]).T
    slope_bs, intercept_bs = np.linalg.lstsq(A_bs, I_bs, rcond=None)[0]
    I_nas_bootstrap.append(intercept_bs)

I_nas_std = np.std(I_nas_bootstrap)
print(f"\nОценка погрешности тока насыщения:")
print(f"I_н = {I_nas:.2f} ± {I_nas_std:.2f} мкА")
print(f"Относительная погрешность: {I_nas_std/I_nas*100:.1f}%")