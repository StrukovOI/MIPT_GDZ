import numpy as np
import matplotlib.pyplot as plt

# 1. Исходные данные
theta_deg = np.array([0, 10, 20, 30, 40, 50, 60, 70, 80, 90, 100, 110])
N = np.array([900, 888, 800, 745, 688, 605, 546, 490, 434, 400, 356, 329])

# Погрешности из условия
d_theta_deg = 1.0  # градусы
d_N = 5.0          # каналы

# 2. Перевод угла в радианы для расчётов
theta_rad = np.radians(theta_deg)
d_theta_rad = np.radians(d_theta_deg)

# 3. Расчёт координат для графика
X = 1 - np.cos(theta_rad)
Y = 1 / N

# 4. Расчёт погрешностей координат (через производные)
# dX = |d(1 - cos(theta))/d(theta)| * d_theta = sin(theta) * d_theta_rad
dX = np.sin(theta_rad) * d_theta_rad

# dY = |d(1/N)/dN| * d_N = (1 / N^2) * d_N
dY = d_N / (N**2)

# 5. Линейная аппроксимация (МНК) для проведения прямой
# Y = k * X + b
k, b = np.polyfit(X, Y, 1)
X_fit = np.linspace(0, np.max(X) * 1.05, 100)
Y_fit = k * X_fit + b

# 6. Настройка стиля графиков
plt.rcParams['font.size'] = 12
plt.rcParams['axes.grid'] = True
plt.rcParams['grid.alpha'] = 0.5

# 7. Построение графика
plt.figure(figsize=(9, 6))

# Точки с крестами погрешностей
plt.errorbar(X, Y, xerr=dX, yerr=dY, fmt='o', color='blue', 
             ecolor='black', capsize=4, markersize=6, 
             label='Экспериментальные точки')

# Линия наилучшего приближения
plt.plot(X_fit, Y_fit, '-', color='red', linewidth=2, 
         label=f'Линейная аппроксимация\n(k = {k:.5f})')

# Оформление осей и легенды
plt.xlabel(r'$1 - \cos\theta$', fontsize=14)
plt.ylabel(r'$1 / N(\theta)$', fontsize=14)# plt.title('Проверка формулы Комптона (линеаризованный график)', fontsize=15)
plt.legend(loc='upper left', fontsize=11)

# Сохранение и показ
plt.tight_layout()
plt.savefig('compton_graph.png', dpi=300)
print("График сохранён как 'compton_graph.png'")
plt.show()

# Вывод параметров для отчёта (поможет заполнить пропуски в LaTeX)
print(f"\nПараметры линейной аппроксимации:")
print(f"Наклон (k): {k:.5f}")
print(f"Пересечение с осью Y (1/N_наил(0)): {b:.6f}  =>  N_наил(0) = {1/b:.0f}")
# Для угла 90 градусов X = 1
Y_90_fit = k * 1 + b
print(f"Значение на прямой при X=1 (1/N_наил(90)): {Y_90_fit:.6f}  =>  N_наил(90) = {1/Y_90_fit:.0f}")