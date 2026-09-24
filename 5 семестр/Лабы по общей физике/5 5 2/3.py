import numpy as np
import matplotlib.pyplot as plt

# Данные для 226Ra и его дочерних ядер
# (из рис. 3 методички)
isotopes = ['$^{226}$Ra', '$^{222}$Rn', '$^{218}$Po', '$^{214}$Po']
E_alpha = np.array([4.784, 5.490, 6.002, 7.687])  # МэВ
T_half_s = np.array([
    1617 * 365.25 * 24 * 3600,      # 1617 лет -> секунды
    3.82 * 24 * 3600,                # 3.82 дня -> секунды
    3.10 * 60,                       # 3.10 мин -> секунды
    1.64e-4                          # 164 мкс -> секунды
])

# Вычисляем координаты для графика
x = 1 / np.sqrt(E_alpha)
y = np.log10(T_half_s)

# Линейная аппроксимация (МНК)
k, b = np.polyfit(x, y, 1)
x_fit = np.linspace(min(x) - 0.02, max(x) + 0.02, 100)
y_fit = k * x_fit + b

# Построение графика
plt.figure(figsize=(9, 6))
plt.plot(x_fit, y_fit, '-', color='red', linewidth=2, 
         label=f'Аппроксимация: lg T = {k:.2f}/√E + {b:.2f}')
plt.scatter(x, y, color='blue', s=80, zorder=5, label='Экспериментальные точки')

# Подписи точек
for i, iso in enumerate(isotopes):
    plt.annotate(iso, (x[i], y[i]), textcoords="offset points", 
                 xytext=(10, 5), fontsize=10, color='darkblue')

plt.xlabel(r'$1/\sqrt{E_\alpha}$, МэВ$^{-1/2}$', fontsize=13)
plt.ylabel(r'$\lg T_{1/2}$, $T_{1/2}$ в секундах', fontsize=13)
# plt.title('Проверка закона Гейгера–Неттола для семейства $^{226}$Ra', fontsize=14)
plt.legend(loc='upper right', fontsize=11)
plt.grid(True, alpha=0.4)

plt.tight_layout()
plt.savefig('geiger_nuttall.png', dpi=300)
print("График сохранён как 'geiger_nuttall.png'")
plt.show()

# Вывод коэффициентов
print(f"\nКоэффициенты закона Гейгера–Неттола:")
print(f"a = {k:.2f}")
print(f"b = {b:.2f}")
print(f"Коэффициент детерминации R² = {1 - np.sum((y - (k*x + b))**2) / np.sum((y - np.mean(y))**2):.4f}")