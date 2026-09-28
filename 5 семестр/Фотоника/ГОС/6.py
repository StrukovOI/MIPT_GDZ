import numpy as np
import matplotlib.pyplot as plt
from scipy.optimize import fsolve, curve_fit
import warnings

warnings.filterwarnings('ignore')

# Настройка стиля
plt.style.use('seaborn-v0_8-paper')
plt.rcParams['font.family'] = 'serif'
plt.rcParams['font.serif'] = ['Times New Roman', 'DejaVu Serif']
plt.rcParams['axes.unicode_minus'] = False

def fmt(val, decimals=4):
    return f"{val:.{decimals}f}".replace('.', ',')

# =============================================================================
# 1. Ввод данных
# =============================================================================
z1 = 797.0  # 79,7 см (ближе к перетяжке, пучок уже)
z2 = 492.0  # 49,2 см (дальше от перетяжки, пучок шире)

x1 = np.array([0, 0.05, 0.1, 0.15, 0.2, 0.25, 0.3, 0.35, 0.4, 0.45, 0.48, 0.5, 0.52, 0.54, 0.55, 0.56, 0.57, 0.58, 0.59, 0.6, 0.61, 0.62, 0.63, 0.64, 0.65, 0.66, 0.67, 0.68, 0.69, 0.7, 0.71, 0.72, 0.73, 0.75, 0.77, 0.79, 0.81, 0.83, 0.85, 0.9, 0.95, 1, 1.05, 1.1, 1.15, 1.2, 1.25])
V1 = np.array([5, 8, 12, 20, 55, 72, 125, 243, 475, 899, 1241, 1530, 1812, 2102, 2230, 2342, 2428, 2510, 2565, 2627, 2646, 2670, 2680, 2680, 2660, 2641, 2603, 2568, 2482, 2418, 2303, 2203, 2075, 1753, 1552, 1297, 1065, 800, 634, 314, 142, 68, 35, 18, 10, 6, 4])

x2 = np.array([0, 0.1, 0.15, 0.2, 0.25, 0.3, 0.35, 0.4, 0.45, 0.46, 0.47, 0.48, 0.49, 0.5, 0.51, 0.52, 0.53, 0.54, 0.55, 0.56, 0.57, 0.58, 0.59, 0.6, 0.61, 0.62, 0.63, 0.64, 0.65, 0.66, 0.67, 0.68, 0.69, 0.7, 0.71, 0.72, 0.73, 0.75, 0.76, 0.77, 0.78, 0.79, 0.8, 0.81, 0.82, 0.83, 0.84, 0.85, 0.86, 0.87, 0.88, 0.89, 0.9, 0.92, 0.94, 0.96, 0.98, 1, 1.05, 1.1, 1.15, 1.2, 1.25, 1.35, 1.4, 1.45])
V2 = np.array([0, 1, 3, 5, 8, 15, 30, 62, 138, 160, 185, 222, 264, 315, 356, 419, 489, 545, 625, 701, 760, 833, 936, 1020, 1123, 1250, 1352, 1430, 1530, 1658, 1759, 1874, 1980, 2060, 2170, 2267, 2346, 2468, 2490, 2538, 2559, 2570, 2580, 2570, 2553, 2520, 2468, 2427, 2364, 2245, 2214, 2066, 1951, 1745, 1482, 1241, 988, 783, 408, 180, 75, 32, 13, 7, 4, 2])

dV = 5.0
lambda_m = 0.6328e-3 

# =============================================================================
# 2. Аппроксимация профилей
# =============================================================================
def gaussian(x, V0, xc, omega, Vbg):
    return V0 * np.exp(-2 * (x - xc)**2 / omega**2) + Vbg

def get_omega(x, V):
    p0 = [np.max(V) - np.min(V), x[np.argmax(V)], 0.3, np.min(V)]
    popt, pcov = curve_fit(gaussian, x, V, p0=p0, sigma=np.full_like(V, dV), absolute_sigma=True)
    return popt[2], np.sqrt(np.diag(pcov))[2]

omega_1, d_omega_1 = get_omega(x1, V1)
omega_2, d_omega_2 = get_omega(x2, V2)

print(f"Эксперимент 1 (z={z1/10} см): omega_1 = {fmt(omega_1, 4)} мм")
print(f"Эксперимент 2 (z={z2/10} см): omega_2 = {fmt(omega_2, 4)} мм")

# =============================================================================
# 3. ПРАВИЛЬНОЕ численное решение (перетяжка МЕЖДУ точками)
# =============================================================================
def equation(u):
    # u = omega_0^2. Перетяжка между z1 и z2, поэтому расстояния СКЛАДЫВАЮТСЯ
    if u <= 0 or u >= min(omega_1**2, omega_2**2):
        return 1e6
    term = (np.pi * np.sqrt(u) / lambda_m) * (np.sqrt(omega_1**2 - u) + np.sqrt(omega_2**2 - u))
    return term - (z1 - z2)

u_sol = fsolve(equation, 0.015)[0] # 0.015 ~ (0.12)^2
omega_0 = np.sqrt(u_sol)

# Находим z_0. Расстояние от z1 до перетяжки:
dist_1 = (np.pi * omega_0 / lambda_m) * np.sqrt(omega_1**2 - omega_0**2)
z_0 = z1 - dist_1

print(f"\nНайденная перетяжка: omega_0 = {fmt(omega_0, 4)} мм, z_0 = {fmt(z_0/10, 2)} см")

# Проверка попадания в точки
def omega_sq(z, w0, z0, lam):
    return w0**2 + (lam**2 / (np.pi**2 * w0**2)) * (z - z0)**2

check_1 = np.sqrt(omega_sq(z1, omega_0, z_0, lambda_m))
check_2 = np.sqrt(omega_sq(z2, omega_0, z_0, lambda_m))
print(f"ПРОВЕРКА: парабола даёт omega(z1) = {fmt(check_1, 4)} мм (совпадает с {fmt(omega_1, 4)})")
print(f"ПРОВЕРКА: парабола даёт omega(z2) = {fmt(check_2, 4)} мм (совпадает с {fmt(omega_2, 4)})")

# =============================================================================
# 4. Оценка погрешностей (Монте-Карло)
# =============================================================================
N_mc = 10000
w0_samples, z0_samples = [], []
for _ in range(N_mc):
    z1_mc = np.random.normal(z1, 1.0)
    z2_mc = np.random.normal(z2, 1.0)
    w1_mc = np.random.normal(omega_1, d_omega_1)
    w2_mc = np.random.normal(omega_2, d_omega_2)
    
    def eq_mc(u):
        if u <= 0 or u >= min(w1_mc**2, w2_mc**2): return 1e6
        return (np.pi * np.sqrt(u) / lambda_m) * (np.sqrt(w1_mc**2 - u) + np.sqrt(w2_mc**2 - u)) - (z1_mc - z2_mc)
    
    try:
        u_mc = fsolve(eq_mc, 0.015)[0]
        if 0 < u_mc < min(w1_mc**2, w2_mc**2):
            w0_mc = np.sqrt(u_mc)
            dist_mc = (np.pi * w0_mc / lambda_m) * np.sqrt(w1_mc**2 - u_mc)
            z0_samples.append(z1_mc - dist_mc)
            w0_samples.append(w0_mc)
    except:
        pass

d_omega_0 = np.std(w0_samples)
d_z_0 = np.std(z0_samples)
print(f"Погрешности: omega_0 = {fmt(omega_0, 4)} +/- {fmt(d_omega_0, 4)} мм, z_0 = {fmt(z_0/10, 2)} +/- {fmt(d_z_0/10, 2)} см")

# =============================================================================
# 5. Построение графика
# =============================================================================
fig, ax = plt.subplots(figsize=(9, 6))

z_theory = np.linspace(0, 900, 500)
omega2_theory = omega_sq(z_theory, omega_0, z_0, lambda_m)

# Асимптоты
# theta = lambda_m / (np.pi * omega_0)
# omega2_asym = (theta**2) * (z_theory - z_0)**2

# ax.plot(z_theory/10, omega2_asym, 'k--', linewidth=1.5, alpha=0.5, label='Асимптоты (расходимость)')
ax.plot(z_theory/10, omega2_theory, 'r-', linewidth=2.5, label='Теоретическая парабола $\omega^2(z)$')

ax.errorbar([z1/10, z2/10], [omega_1**2, omega_2**2], 
            yerr=[2*omega_1*d_omega_1, 2*omega_2*d_omega_2], 
            fmt='bo', markersize=10, capsize=6, capthick=2, 
            label='Экспериментальные точки')

# Указатели на перетяжку
ax.plot([z_0/10, z_0/10], [0, omega_0**2], 'g-', linewidth=2, alpha=0.8)
ax.plot([0, z_0/10], [omega_0**2, omega_0**2], 'g-', linewidth=2, alpha=0.8)
ax.plot(z_0/10, omega_0**2, 'go', markersize=10)

ax.text(z_0/10 + 2, omega_0**2 + 0.005, 
        f'Перетяжка:\n$z_0 = {fmt(z_0/10, 1)}$ см\n$\omega_0 = {fmt(omega_0, 3)}$ мм', 
        verticalalignment='bottom', fontsize=11, 
        bbox=dict(facecolor='white', alpha=0.9, edgecolor='green', boxstyle='round,pad=0.3'))

ax.set_xlabel(r'Расстояние от лазера $z$, см', fontsize=12)
ax.set_ylabel(r'Квадрат радиуса пучка $\omega^2$, мм$^2$', fontsize=12)
# ax.set_title('Графическое определение перетяжки (парабола проходит через обе точки)', fontsize=13)
ax.legend(fontsize=10, loc='upper left')
ax.grid(True, alpha=0.4)
ax.set_xlim(0, 90)
ax.set_ylim(0, max(omega_1**2, omega_2**2) * 1.3)

plt.tight_layout()
plt.savefig('waist_overlay_graph.png', dpi=300)
print("\nГрафик сохранён в файл 'waist_overlay_graph.png'")
plt.show()