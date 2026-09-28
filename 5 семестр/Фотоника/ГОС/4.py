import numpy as np
import matplotlib.pyplot as plt
from scipy.optimize import curve_fit
import warnings

warnings.filterwarnings('ignore')

# Настройка стиля графиков
plt.style.use('seaborn-v0_8-paper')
plt.rcParams['font.family'] = 'serif'
plt.rcParams['font.serif'] = ['Times New Roman', 'DejaVu Serif']
plt.rcParams['axes.unicode_minus'] = False

# =============================================================================
# 1. Ввод данных
# =============================================================================
# ВНИМАНИЕ: Если данные перепутаны местами, установите SWAP_DATA = True
SWAP_DATA = True  

z1_raw = 492.0  # 49.2 см
z2_raw = 797.0  # 79.7 см

# Данные набора 1
x_set1 = np.array([0, 0.1, 0.15, 0.2, 0.25, 0.3, 0.35, 0.4, 0.45, 0.46, 0.47, 0.48, 0.49, 0.5, 0.51, 0.52, 0.53, 0.54, 0.55, 0.56, 0.57, 0.58, 0.59, 0.6, 0.61, 0.62, 0.63, 0.64, 0.65, 0.66, 0.67, 0.68, 0.69, 0.7, 0.71, 0.72, 0.73, 0.75, 0.76, 0.77, 0.78, 0.79, 0.8, 0.81, 0.82, 0.83, 0.84, 0.85, 0.86, 0.87, 0.88, 0.89, 0.9, 0.92, 0.94, 0.96, 0.98, 1, 1.05, 1.1, 1.15, 1.2, 1.25, 1.35, 1.4, 1.45])
V_set1 = np.array([0, 1, 3, 5, 8, 15, 30, 62, 138, 160, 185, 222, 264, 315, 356, 419, 489, 545, 625, 701, 760, 833, 936, 1020, 1123, 1250, 1352, 1430, 1530, 1658, 1759, 1874, 1980, 2060, 2170, 2267, 2346, 2468, 2490, 2538, 2559, 2570, 2580, 2570, 2553, 2520, 2468, 2427, 2364, 2245, 2214, 2066, 1951, 1745, 1482, 1241, 988, 783, 408, 180, 75, 32, 13, 7, 4, 2])

# Данные набора 2
x_set2 = np.array([0, 0.05, 0.1, 0.15, 0.2, 0.25, 0.3, 0.35, 0.4, 0.45, 0.48, 0.5, 0.52, 0.54, 0.55, 0.56, 0.57, 0.58, 0.59, 0.6, 0.61, 0.62, 0.63, 0.64, 0.65, 0.66, 0.67, 0.68, 0.69, 0.7, 0.71, 0.72, 0.73, 0.75, 0.77, 0.79, 0.81, 0.83, 0.85, 0.9, 0.95, 1, 1.05, 1.1, 1.15, 1.2, 1.25])
V_set2 = np.array([5, 8, 12, 20, 55, 72, 125, 243, 475, 899, 1241, 1530, 1812, 2102, 2230, 2342, 2428, 2510, 2565, 2627, 2646, 2670, 2680, 2680, 2660, 2641, 2603, 2568, 2482, 2418, 2303, 2203, 2075, 1753, 1552, 1297, 1065, 800, 634, 314, 142, 68, 35, 18, 10, 6, 4])

# Меняем местами, если флаг установлен
if SWAP_DATA:
    z1, z2 = z2_raw, z1_raw
    x1, x2 = x_set2, x_set1
    V1, V2 = V_set2, V_set1
    print("ВНИМАНИЕ: Наборы данных для z1 и z2 поменяны местами для корректного расчёта.\n")
else:
    z1, z2 = z1_raw, z2_raw
    x1, x2 = x_set1, x_set2
    V1, V2 = V_set1, V_set2

# Погрешности
dz = 1.0      # 0,1 см = 1 мм
dx = 0.01     # мм
dV = 5.0      # 5 * 10^(-4) В

# Длина волны He-Ne лазера в мм
lambda_m = 0.6328e-3 

# Вспомогательная функция для форматирования чисел с запятой
def fmt(val, decimals=4):
    return f"{val:.{decimals}f}".replace('.', ',')

# =============================================================================
# 2. Функции для аппроксимации и расчёта
# =============================================================================
def gaussian(x, V0, xc, omega, Vbg):
    return V0 * np.exp(-2 * (x - xc)**2 / omega**2) + Vbg

def find_beam_params(x, V, z, label):
    V0_guess = np.max(V) - np.min(V)
    xc_guess = x[np.argmax(V)]
    omega_guess = 0.3
    Vbg_guess = np.min(V)
    
    p0 = [V0_guess, xc_guess, omega_guess, Vbg_guess]
    popt, pcov = curve_fit(gaussian, x, V, p0=p0, sigma=np.full_like(V, dV), absolute_sigma=True)
    V0, xc, omega, Vbg = popt
    
    perr = np.sqrt(np.diag(pcov))
    d_omega = perr[2]
    
    print(f"--- Результаты для {label} (z = {fmt(z/10, 1)} см) ---")
    print(f"Центр пучка xc = {fmt(xc, 3)} +/- {fmt(perr[1], 3)} мм")
    print(f"Радиус пучка omega = {fmt(omega, 4)} +/- {fmt(d_omega, 4)} мм")
    print(f"Фоновый сигнал Vbg = {fmt(Vbg, 1)}")
    
    mask = V > Vbg + 10
    x_shifted = x[mask] - xc
    y_lin = np.log(V[mask] - Vbg)
    x_lin = x_shifted**2
    
    B, A = np.polyfit(x_lin, y_lin, 1)
    omega_lin = np.sqrt(-2 / B)
    
    print(f"Проверка линеаризацией: omega_lin = {fmt(omega_lin, 4)} мм\n")
    
    return omega, d_omega, xc, Vbg, x_lin, y_lin, B, A, popt

# =============================================================================
# 3. Обработка данных
# =============================================================================
omega1, d_omega1, xc1, Vbg1, x_lin1, y_lin1, B1, A1, popt1 = find_beam_params(x1, V1, z1, "z1")
omega2, d_omega2, xc2, Vbg2, x_lin2, y_lin2, B2, A2, popt2 = find_beam_params(x2, V2, z2, "z2")

# =============================================================================
# 4. Расчёт перетяжки
# =============================================================================
def solve_waist(z1, z2, w1, w2, lam):
    from scipy.optimize import fsolve
    
    def equations(u):
        if u <= 0 or u >= min(w1**2, w2**2):
            return 1e6
        term1 = (np.pi * np.sqrt(u) / lam) * np.sqrt(w2**2 - u)
        term2 = (np.pi * np.sqrt(u) / lam) * np.sqrt(w1**2 - u)
        return term1 - term2 - (z2 - z1)
    
    u_guess = min(w1**2, w2**2) * 0.8
    u_sol = fsolve(equations, u_guess)[0]
    omega_0 = np.sqrt(u_sol)
    z_0 = z1 - (np.pi * omega_0 / lam) * np.sqrt(w1**2 - omega_0**2)
    
    return omega_0, z_0

if omega2 > omega1:
    omega_0, z_0 = solve_waist(z1, z2, omega1, omega2, lambda_m)
    
    N_mc = 10000
    omega0_samples, z0_samples = [], []
    
    for _ in range(N_mc):
        z1_mc = np.random.normal(z1, dz)
        z2_mc = np.random.normal(z2, dz)
        w1_mc = np.random.normal(omega1, d_omega1)
        w2_mc = np.random.normal(omega2, d_omega2)
        try:
            w0_mc, z0_mc = solve_waist(z1_mc, z2_mc, w1_mc, w2_mc, lambda_m)
            if 0 < w0_mc < min(w1_mc, w2_mc):
                omega0_samples.append(w0_mc)
                z0_samples.append(z0_mc)
        except:
            continue
    
    d_omega0 = np.std(omega0_samples)
    d_z0 = np.std(z0_samples)
    
    print("=== ИТОГОВЫЕ ПАРАМЕТРЫ ПЕРЕТЯЖКИ ===")
    print(f"omega_0 = {fmt(omega_0, 4)} +/- {fmt(d_omega0, 4)} мм")
    print(f"z_0     = {fmt(z_0/10, 2)} +/- {fmt(d_z0/10, 2)} см (от выходного окна лазера)")
else:
    print("ОШИБКА: Размер пучка на большем расстоянии меньше. Проверьте исходные данные!")

# =============================================================================
# 5. Построение графиков
# =============================================================================
fig, axs = plt.subplots(2, 2, figsize=(12, 10))

# График 1: z1, исходные данные + фит
x_fit1 = np.linspace(min(x1), max(x1), 200)
axs[0, 0].errorbar(x1, V1, yerr=dV, fmt='o', label='Эксперимент', markersize=4, alpha=0.7)
axs[0, 0].plot(x_fit1, gaussian(x_fit1, *popt1), 'r-', label=f'Аппроксимация\n$\\omega$ = {fmt(omega1, 3)} мм')
axs[0, 0].axvline(xc1, color='g', linestyle='--', label=f'$x_c$ = {fmt(xc1, 2)} мм')
axs[0, 0].axhline(Vbg1, color='k', linestyle=':', label=f'$V_{{bg}}$ = {fmt(Vbg1, 1)}')
axs[0, 0].set_title(f'Профиль пучка при z = {fmt(z1/10, 1)} см')
axs[0, 0].set_xlabel('x, мм')
axs[0, 0].set_ylabel('U, 10$^{-4}$ В')
axs[0, 0].legend()
axs[0, 0].grid(True, alpha=0.5)

# График 2: z2, исходные данные + фит
x_fit2 = np.linspace(min(x2), max(x2), 200)
axs[0, 1].errorbar(x2, V2, yerr=dV, fmt='o', label='Эксперимент', markersize=4, alpha=0.7)
axs[0, 1].plot(x_fit2, gaussian(x_fit2, *popt2), 'r-', label=f'Аппроксимация\n$\\omega$ = {fmt(omega2, 3)} мм')
axs[0, 1].axvline(xc2, color='g', linestyle='--', label=f'$x_c$ = {fmt(xc2, 2)} мм')
axs[0, 1].axhline(Vbg2, color='k', linestyle=':', label=f'$V_{{bg}}$ = {fmt(Vbg2, 1)}')
axs[0, 1].set_title(f'Профиль пучка при z = {fmt(z2/10, 1)} см')
axs[0, 1].set_xlabel('x, мм')
axs[0, 1].set_ylabel('U, 10$^{-4}$ В')
axs[0, 1].legend()
axs[0, 1].grid(True, alpha=0.5)

# График 3: z1, линеаризация (с префиксом r для корректного LaTeX)
axs[1, 0].plot(x_lin1, y_lin1, 'bo', markersize=4, label='Экспериментальные точки')
axs[1, 0].plot(x_lin1, A1 + B1 * x_lin1, 'r-', label=f'Линейная аппроксимация\nk = {fmt(B1, 2)}')
axs[1, 0].set_title(f'Линеаризация зависимости для z = {fmt(z1/10, 1)} см')
axs[1, 0].set_xlabel('$(x - x_c)^2$, мм$^2$')
axs[1, 0].set_ylabel(r'$\ln(U - U_{bg})$')
axs[1, 0].legend()
axs[1, 0].grid(True, alpha=0.5)

# График 4: z2, линеаризация
axs[1, 1].plot(x_lin2, y_lin2, 'bo', markersize=4, label='Экспериментальные точки')
axs[1, 1].plot(x_lin2, A2 + B2 * x_lin2, 'r-', label=f'Линейная аппроксимация\nk = {fmt(B2, 2)}')
axs[1, 1].set_title(f'Линеаризация зависимости для z = {fmt(z2/10, 1)} см')
axs[1, 1].set_xlabel('$(x - x_c)^2$, мм$^2$')
axs[1, 1].set_ylabel(r'$\ln(U - U_{bg})$')
axs[1, 1].legend()
axs[1, 1].grid(True, alpha=0.5)

plt.tight_layout()
plt.savefig('beam_profiles.png', dpi=300)
print("\nГрафики сохранены в файл 'beam_profiles.png'")

# ОТКРЫТИЕ ОКНА С ГРАФИКАМИ
plt.show()