import numpy as np
import matplotlib.pyplot as plt

# Настройка шрифтов для корректного отображения русского текста и минуса
plt.rcParams['font.family'] = 'serif'
plt.rcParams['font.serif'] = ['Times New Roman', 'DejaVu Serif']
plt.rcParams['axes.unicode_minus'] = False

# Данные: (показание барабана N, длина волны lambda)
data = [
    (2459, 5852.49), (2474, 5881.89), (2504, 5944.83), (2519, 5975.53),
    (2543, 6030.00), (2564, 6074.34), (2573, 6096.14), (2594, 6143.06),
    (2602, 6163.59), (2626, 6217.28), (2646, 6266.49), (2662, 6304.79),
    (2672, 6334.42), (2692, 6382.99), (2698, 6402.24), (2736, 6506.53),
    (2745, 6532.88), (2768, 6598.95), (2796, 6678.28), (2808, 6717.04)
]

N = np.array([d[0] for d in data])
lam = np.array([d[1] for d in data])

# Аппроксимация квадратичным многочленом (степень 2)
coeffs = np.polyfit(N, lam, 2)
poly = np.poly1d(coeffs)

# Расчет R^2
y_fit = poly(N)
ss_res = np.sum((lam - y_fit)**2)
ss_tot = np.sum((lam - np.mean(lam))**2)
r2 = 1 - (ss_res / ss_tot)

# Формирование строки с уравнением для легенды
# Используем форматирование для красивого вывода коэффициентов
a, b, c = coeffs
sign_b = '+' if b >= 0 else '-'
sign_c = '+' if c >= 0 else '-'
eq_str = f"λ(N) = {a:.4e}·N² {sign_b} {abs(b):.4f}·N {sign_c} {abs(c):.2f}"
legend_str = f"Аппроксимация: \n{eq_str}"

# Построение графика
plt.figure(figsize=(10, 6))

# Точки с погрешностью по оси X: +- 2 деления
plt.errorbar(N, lam, xerr=2, fmt='o', color='black', 
             label='Экспериментальные точки', capsize=4, markersize=5, elinewidth=1)

# Линия аппроксимации (расширенный диапазон: min-60 до max+60)
N_fit = np.linspace(min(N) - 60, max(N) + 60, 500)
plt.plot(N_fit, poly(N_fit), 'r-', linewidth=2, label=legend_str)

# Оформление
plt.xlabel('Показания барабана монохроматора, дел.', fontsize=12)
plt.ylabel('Длина волны, Å', fontsize=12)
# plt.title('Градуировочная кривая монохроматора УМ-2', fontsize=14, fontweight='bold')
plt.grid(True, which='major', linestyle='-', alpha=0.7)
plt.grid(True, which='minor', linestyle='--', alpha=0.4)

# Размещаем легенду так, чтобы она не перекрывала данные
plt.legend(fontsize=10, loc='upper left', framealpha=0.9)

# Расширенные пределы осей для демонстрации поведения кривой
plt.xlim(min(N) - 60, max(N) + 60)
plt.ylim(5800, 6750)

plt.tight_layout()
plt.show() # Только отображение, без автоматического сохранения