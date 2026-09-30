import numpy as np
import matplotlib.pyplot as plt
from scipy.interpolate import UnivariateSpline
from scipy.optimize import curve_fit
import matplotlib.ticker as mticker

# Исходные данные
U_kV = np.array([30, 25, 20, 17, 15, 12, 10, 5, 2, 1.5, 1, 0.5])
sigma = np.array([0.2211, 0.2388, 0.2228, 0.2261, 0.2270, 0.2234, 0.2161, 0.2033, 0.1519, 0.1319, 0.1024, 0.0500])
d_sigma = np.array([0.0022, 0.0027, 0.0032, 0.0037, 0.0034, 0.0034, 0.0041, 0.0043, 0.0038, 0.0041, 0.0040, 0.0049])

# Сортировка по возрастанию напряжения
sorted_indices = np.argsort(U_kV)
U_sorted = U_kV[sorted_indices]
sigma_sorted = sigma[sorted_indices]
d_sigma_sorted = d_sigma[sorted_indices]

# Функция для аппроксимации (физически обоснованная форма)
# sigma = a * (1 - exp(-b*U)) * exp(-c*U) + d
# или более простая: логарифмическая с насыщением
def physical_model(U, a, b, c, d):
    """
    Физическая модель: рост с насыщением и возможным спадом
    a - максимальное значение sigma
    b - скорость роста
    c - коэффициент спада на высоких напряжениях
    d - смещение
    """
    return a * (1 - np.exp(-b * U)) * np.exp(-c * U) + d

# Подбор параметров модели
try:
    popt, pcov = curve_fit(physical_model, U_sorted, sigma_sorted, 
                           p0=[0.24, 0.5, 0.01, 0.0], 
                           sigma=d_sigma_sorted,
                           absolute_sigma=True,
                           maxfev=10000)
    
    # Создание плавной кривой
    U_smooth = np.linspace(0.5, 30, 300)
    sigma_smooth = physical_model(U_smooth, *popt)
    
except RuntimeError:
    # Если не сходится, используем сглаживание сплайнами
    print("Используем сплайн-аппроксимацию")
    spline = UnivariateSpline(U_sorted, sigma_sorted, s=0.001, k=3)
    U_smooth = np.linspace(0.5, 30, 300)
    sigma_smooth = spline(U_smooth)

# Построение графика
fig, ax = plt.subplots(figsize=(10, 7))

# Экспериментальные точки с погрешностями
ax.errorbar(U_sorted, sigma_sorted, yerr=d_sigma_sorted, 
            fmt='o', color='blue', markersize=6, 
            ecolor='red', elinewidth=1.5, capsize=4, 
            label='Экспериментальные данные', zorder=3)

# Аппроксимирующая кривая
ax.plot(U_smooth, sigma_smooth, 'g-', linewidth=2.5, 
        label='Аппроксимация', zorder=2)

# Настройка осей
ax.set_xlabel('Ускоряющее напряжение $U$, кВ', fontsize=12, fontweight='bold')
ax.set_ylabel('Коэффициент вторичной эмиссии $\sigma$', fontsize=12, fontweight='bold')
# ax.set_title('Зависимость коэффициента вторичной эмиссии\nот ускоряющего напряжения', 
#              fontsize=14, fontweight='bold', pad=20)

# Сетка
ax.grid(True, linestyle='--', alpha=0.7, zorder=0)

# Легенда
ax.legend(loc='lower right', fontsize=10, framealpha=0.9)

# Форматирование чисел с запятой
def comma_formatter(x, pos):
    return f"{x:g}".replace('.', ',')

ax.xaxis.set_major_formatter(mticker.FuncFormatter(comma_formatter))
ax.yaxis.set_major_formatter(mticker.FuncFormatter(comma_formatter))

# Установка пределов
ax.set_xlim(0, 32)
ax.set_ylim(0, 0.28)

# Добавление аннотаций для ключевых областей
# ax.axvspan(0, 3, alpha=0.1, color='yellow', label='Область роста')
# ax.axvspan(5, 25, alpha=0.1, color='green', label='Плато (насыщение)')

plt.tight_layout()
plt.savefig('fig_sigma_plot.png', dpi=300, bbox_inches='tight')
plt.show()

# Вывод параметров аппроксимации
if 'popt' in locals():
    print("\nПараметры аппроксимации:")
    print(f"a (макс. значение) = {popt[0]:.4f}")
    print(f"b (скорость роста) = {popt[1]:.4f}")
    print(f"c (коэфф. спада) = {popt[4]:.4f}")
    print(f"d (смещение) = {popt[3]:.4f}")