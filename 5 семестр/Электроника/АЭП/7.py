import numpy as np
from scipy.optimize import fsolve

# Твои данные из консоли
slopes = {'F0001': -24.58, 'F0002': -16.20, 'F0003': -27.11, 'F0004': -15.67}
phi = 4.7  # эВ
R_m = 1e-3 # 1 мм
k_geom = 0.5

def fmt(val, dec=2):
    return f"{val:.{dec}f}".replace('.', ',')

results_beta = []
results_r = []

print("\\begin{tabular}{|l|c|c|}")
print("\\hline")
print("№ ВАХ & $\\\\tan \\\\alpha$, кВ & $\\\\beta$, $10^6$ м$^{-1}$ \\\\")
print("\\hline")

for name, slope in slopes.items():
    # Расчет beta (в 10^6 м^-1)
    beta = -6.83 * (phi**1.5) / slope
    beta_m = beta * 1e6
    
    # Численное решение для r
    def eq_r(r_m):
        return beta_m - 1.0 / (k_geom * r_m * np.log(R_m / r_m))
    
    r_m = fsolve(eq_r, 50e-9)[0]
    r_nm = r_m * 1e9
    
    results_beta.append((name, slope, beta))
    results_r.append((name, r_nm))
    
    # Строка для первой таблицы
    name_ru = "Ручн." if "manual" in name.lower() else f"Авто {name[-1]}"
    # Для простоты назовем их Авто 1, Авто 2 и т.д.
    auto_num = name[-1]
    print(f"Авто {auto_num} & {fmt(slope, 2)} & {fmt(beta, 2)} \\\\")

print("\\hline")
print("\\end{tabular}")

print("\n" + "="*50 + "\n")

print("\\begin{tabular}{|l|c|}")
print("\\hline")
print("№ ВАХ & Характерный радиус $r$, нм \\\\")
print("\\hline")
for name, r_nm in results_r:
    auto_num = name[-1]
    print(f"Авто {auto_num} & {fmt(r_nm, 1)} \\\\")
print("\\hline")
print("\\end{tabular}")