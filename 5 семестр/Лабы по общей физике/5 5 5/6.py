import numpy as np
import matplotlib.pyplot as plt

# Данные из таблицы (исключая точки 241Am с минимальной энергией)
# Источник, E_i (МэВ), R_i
data = [
    ("60Co", 1.173, 0.054),
    ("60Co", 1.333, 0.053),
    ("137Cs", 0.662, 0.072),
    ("22Na", 0.511, 0.086),
    ("22Na", 1.274, 0.064),
    ("152Eu", 0.123, 0.100),
    ("152Eu", 0.342, 0.088),
    ("152Eu", 0.784, 0.049),
    ("152Eu", 0.972, 0.046),
    ("152Eu", 1.417, 0.054),
]

sources = []
E_list = []
R_list = []
inv_E = []
R_sq = []

print("Источник | E_i (МэВ) | R_i | 1/E_i (МэВ^-1) | R_i^2")
print("-" * 60)

for source, E, R in data:
    sources.append(source)
    E_list.append(E)
    R_list.append(R)
    inv_E.append(1.0 / E)
    R_sq.append(R**2)
    print(f"{source:8} | {E:7.3f} | {R:.3f} | {1.0/E:12.3f} | {R**2:.5f}")

# Линейная аппроксимация R^2 = k * (1/E) + b
inv_E_arr = np.array(inv_E)
R_sq_arr = np.array(R_sq)
k, b = np.polyfit(inv_E_arr, R_sq_arr, 1)

# Плотная сетка для линии тренда
inv_E_fit = np.linspace(min(inv_E_arr) - 0.5, max(inv_E_arr) + 0.5, 100)
R_sq_fit = k * inv_E_fit + b

# Построение графика
plt.figure(figsize=(10, 7))

# Точки экспериментальных данных
plt.scatter(inv_E_arr, R_sq_arr, color='blue', s=80, zorder=5, label='Экспериментальные данные')

# Подписи к точкам
for i, txt in enumerate(sources):
    plt.annotate(txt, (inv_E_arr[i], R_sq_arr[i]), textcoords="offset points", 
                 xytext=(8, 5), fontsize=9, alpha=0.8)

# Линия тренда
plt.plot(inv_E_fit, R_sq_fit, 'r-', linewidth=2, 
         label=f'Аппроксимация: $R^2 = {k:.4f}/E + {b:.4f}$')

plt.xlabel('Обратная энергия $1/E_i$, МэВ$^{-1}$', fontsize=13)
plt.ylabel('Квадрат разрешения $R_i^2$', fontsize=13)
# plt.title('Проверка зависимости $R_i^2 = f(1/E_i)$', fontsize=14)
plt.legend(fontsize=11)
plt.grid(True, alpha=0.4)
plt.tight_layout()

plt.savefig('R_squared_vs_inv_E.png', dpi=300)
print("\nГрафик сохранён как 'R_squared_vs_inv_E.png'")
plt.show()

print(f"\nКоэффициент наклона k = {k:.4f}")
print(f"Свободный член b = {b:.4f}")

# Проверка качества аппроксимации
R_sq_pred = k * inv_E_arr + b
ss_res = np.sum((R_sq_arr - R_sq_pred)**2)
ss_tot = np.sum((R_sq_arr - np.mean(R_sq_arr))**2)
r_squared = 1 - (ss_res / ss_tot)
print(f"Коэффициент детерминации R² = {r_squared:.4f}")