import numpy as np
import matplotlib.pyplot as plt
from scipy.optimize import curve_fit, fsolve
import warnings

warnings.filterwarnings('ignore')

# Настройка стиля графиков
plt.style.use('seaborn-v0_8-paper')
plt.rcParams['font.family'] = 'serif'
plt.rcParams['font.serif'] = ['Times New Roman', 'DejaVu Serif']
plt.rcParams['axes.unicode_minus'] = False

# Вспомогательная функция для форматирования чисел с запятой
def fmt(val, decimals=4):
    return f"{val:.{decimals}f}".replace('.', ',')

# =============================================================================
# 1. Ввод данных и констант
# =============================================================================
# Расстояния в мм
d1 = 320.0       # от лазера до линзы (32 см)
z_det = 492.0    # от лазера до фотоприёмника (49,2 см)
d2 = z_det - d1  # от линзы до фотоприёмника (17,2 см = 172 мм)

# Данные измерения с линзой
x3 = np.array([0.4, 0.45, 0.5, 0.55, 0.6, 0.65, 0.7, 0.75, 0.8, 0.85, 0.9, 0.95, 1, 1.05, 1.1, 1.15, 1.2, 1.25, 1.3, 1.35, 1.4, 1.45, 1.5, 1.55, 1.6, 1.65, 1.7, 1.75, 1.8, 1.85, 1.9, 1.95, 2, 2.05, 2.1, 2.15, 2.2, 2.25, 2.3, 2.35, 2.4, 2.45, 2.5, 2.55, 2.6, 2.65, 2.7, 2.75, 2.8, 2.85, 2.9, 2.95, 3, 3.05, 3.1, 3.15, 3.2, 3.25, 3.3, 3.35, 3.4, 3.45, 3.5, 3.55, 3.6, 3.65, 3.7, 3.75, 3.8, 3.85, 3.9, 3.95, 4, 4.05, 4.1, 4.15, 4.2, 4.25, 4.3, 4.35, 4.4, 4.45, 4.5])
V3 = np.array([2, 3, 4, 5, 6, 8, 10, 12, 16, 20, 24, 29, 32, 40, 47, 55, 63, 71, 79, 89, 100, 110, 122, 135, 148, 164, 180, 195, 209, 220, 232, 242, 251, 260, 269, 278, 288, 295, 300, 303, 304, 303, 301, 298, 295, 291, 285, 276, 268, 261, 252, 244, 232, 217, 205, 193, 183, 164, 148, 135, 122, 110, 100, 89, 79, 71, 63, 55, 47, 40, 32, 29, 24, 20, 16, 12, 10, 8, 6, 5, 4, 3, 2])

# Погрешности
dx = 0.01      # мм
dV = 5.0       # 5 * 10^(-4) В
dd = 1.0       # погрешность расстояний, мм

# Параметры лазера и перетяжки (ОБНОВЛЕНО на основе точного расчёта!)
lambda_m = 0.6328e-3  # мм
omega_0 = 0.1333      # мм
z_0 = 655.3           # мм (65.53 см * 10)
d_omega_0 = 0.0010    # мм
d_z_0 = 0.7           # мм (0.07 см * 10)

# =============================================================================
# 2. Аппроксимация профиля пучка после линзы
# =============================================================================
def gaussian(x, V0, xc, omega, Vbg):
    return V0 * np.exp(-2 * (x - xc)**2 / omega**2) + Vbg

V0_guess = np.max(V3) - np.min(V3)
xc_guess = x3[np.argmax(V3)]
omega_guess = 1.0 
Vbg_guess = np.min(V3)

p0 = [V0_guess, xc_guess, omega_guess, Vbg_guess]
popt, pcov = curve_fit(gaussian, x3, V3, p0=p0, sigma=np.full_like(V3, dV), absolute_sigma=True)
V0, xc3, omega_3, Vbg3 = popt
d_omega_3 = np.sqrt(np.diag(pcov))[2]

print("--- Результаты для пучка ПОСЛЕ линзы ---")
print(f"Центр пучка xc = {fmt(xc3, 3)} +/- {fmt(np.sqrt(np.diag(pcov))[1], 3)} мм")
print(f"Радиус пучка omega_3 = {fmt(omega_3, 4)} +/- {fmt(d_omega_3, 4)} мм")
print(f"Фоновый сигнал Vbg = {fmt(Vbg3, 1)}\n")

# =============================================================================
# 3. Расчёт фокусного расстояния линзы (закон ABCD)
# =============================================================================
def equation_for_f(f, z_L, z_R, d2, lambda_m, omega_3):
    """
    Возвращает разницу между расчётной и целевой мнимой частью 1/q3
    """
    if abs(f) < 1e-6:
        return 1e6
    
    # q1: параметр пучка непосредственно перед линзой
    q1 = z_L + 1j * z_R
    
    # q2: параметр пучка непосредственно после линзы
    # 1/q2 = 1/q1 - 1/f
    q2 = 1 / (1/q1 - 1/f)
    
    # q3: параметр пучка на детекторе (пропагация на d2)
    q3 = q2 + d2
    
    # Мнимая часть 1/q3 должна быть равна -lambda / (pi * omega_3^2)
    im_inv_q3_calc = - (q3.imag / (abs(q3)**2))
    im_inv_q3_target = - lambda_m / (np.pi * omega_3**2)
    
    return im_inv_q3_calc - im_inv_q3_target

# Расстояние от перетяжки до линзы (линза стоит ДО перетяжки, поэтому z_L < 0)
z_L = d1 - z_0
# Рэлеевская длина
z_R = np.pi * omega_0**2 / lambda_m

# Решаем уравнение для f. 
f_sol = fsolve(equation_for_f, x0=100.0, args=(z_L, z_R, d2, lambda_m, omega_3))[0]

print("--- Расчёт параметров линзы ---")
print(f"Расстояние от перетяжки до линзы z_L = {fmt(z_L, 2)} мм")
print(f"Рэлеевская длина z_R = {fmt(z_R, 4)} мм")
print(f"Найденное фокусное расстояние f = {fmt(f_sol, 2)} мм\n")

# =============================================================================
# 4. Оценка погрешности f методом Монте-Карло
# =============================================================================
N_mc = 5000
f_samples = []

for _ in range(N_mc):
    # Генерируем случайные значения в пределах погрешностей
    d1_mc = np.random.normal(d1, dd)
    z_det_mc = np.random.normal(z_det, dd)
    d2_mc = z_det_mc - d1_mc
    
    omega_0_mc = np.random.normal(omega_0, d_omega_0)
    z_0_mc = np.random.normal(z_0, d_z_0)
    omega_3_mc = np.random.normal(omega_3, d_omega_3)
    
    z_L_mc = d1_mc - z_0_mc
    z_R_mc = np.pi * omega_0_mc**2 / lambda_m
    
    try:
        # Ищем корень, начиная с предыдущего решения
        f_mc = fsolve(equation_for_f, x0=f_sol, args=(z_L_mc, z_R_mc, d2_mc, lambda_m, omega_3_mc))[0]
        # Фильтруем физически осмысленные положительные значения (для собирающей линзы)
        if 10 < f_mc < 1000: 
            f_samples.append(f_mc)
    except:
        continue

d_f = np.std(f_samples)
print(f"Погрешность фокусного расстояния (Монте-Карло): df = {fmt(d_f, 2)} мм")
print(f"Итоговое f = {fmt(f_sol, 2)} +/- {fmt(d_f, 2)} мм\n")

# =============================================================================
# 5. Построение графиков
# =============================================================================
fig, axs = plt.subplots(1, 2, figsize=(12, 5))

# График 1: Исходные данные + аппроксимация
x_fit3 = np.linspace(min(x3), max(x3), 300)
axs[0].errorbar(x3, V3, yerr=dV, fmt='o', label='Эксперимент', markersize=4, alpha=0.7)
axs[0].plot(x_fit3, gaussian(x_fit3, *popt), 'r-', label=f'Аппроксимация\n$\\omega_3$ = {fmt(omega_3, 3)} мм')
axs[0].axvline(xc3, color='g', linestyle='--', label=f'$x_c$ = {fmt(xc3, 2)} мм')
axs[0].axhline(Vbg3, color='k', linestyle=':', label=f'$V_{{bg}}$ = {fmt(Vbg3, 1)}')
axs[0].set_title('Профиль пучка после линзы')
axs[0].set_xlabel('x, мм')
axs[0].set_ylabel('U, 10$^{-4}$ В')
axs[0].legend()
axs[0].grid(True, alpha=0.5)

# График 2: Линеаризация
mask3 = V3 > Vbg3 + 5
x_shifted3 = x3[mask3] - xc3
y_lin3 = np.log(V3[mask3] - Vbg3)
x_lin3 = x_shifted3**2

B3, A3 = np.polyfit(x_lin3, y_lin3, 1)
omega_3_lin = np.sqrt(-2 / B3)

axs[1].plot(x_lin3, y_lin3, 'bo', markersize=4, label='Экспериментальные точки')
axs[1].plot(x_lin3, A3 + B3 * x_lin3, 'r-', label=f'Линейная аппроксимация\nk = {fmt(B3, 2)}\n$\\omega_{{lin}}$ = {fmt(omega_3_lin, 3)} мм')
axs[1].set_title('Линеаризация зависимости для пучка после линзы')
axs[1].set_xlabel('$(x - x_c)^2$, мм$^2$')
axs[1].set_ylabel(r'$\ln(U - U_{bg})$')
axs[1].legend()
axs[1].grid(True, alpha=0.5)

plt.tight_layout()
plt.savefig('lens_beam_profile.png', dpi=300)
print("График сохранён в файл 'lens_beam_profile.png'")

plt.show()