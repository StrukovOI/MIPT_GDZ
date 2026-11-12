import numpy as np
import matplotlib.pyplot as plt

plt.rcParams['font.family'] = 'serif'
plt.rcParams['font.serif'] = ['Times New Roman', 'DejaVu Serif']
plt.rcParams['axes.unicode_minus'] = False

# Данные (omega в 10^14 рад/с, V0_phys - перевёрнутый знак для физической корректности)
data = {
    2200: {'omega': 34.476, 'V0_meas': -0.534, 'dV0': 0.029},
    2300: {'omega': 33.697, 'V0_meas': -0.543, 'dV0': 0.016},
    2460: {'omega': 32.164, 'V0_meas': -0.435, 'dV0': 0.042},
    2550: {'omega': 31.177, 'V0_meas': -0.422, 'dV0': 0.026},
    2830: {'omega': 27.772, 'V0_meas': -0.305, 'dV0': 0.027},
}

omegas = np.array([data[N]['omega'] for N in sorted(data.keys())])
V0_phys = np.array([-data[N]['V0_meas'] for N in sorted(data.keys())])
dV0 = np.array([data[N]['dV0'] for N in sorted(data.keys())])

# Линейная регрессия: V0 = m * omega + b
m, b = np.polyfit(omegas, V0_phys, 1)

# Пересчёт в СИ и СГС
m_SI = m * 1e-14  # В * с / рад
e = 1.602176634e-19 # Кл
h_calc_J = 2 * np.pi * e * m_SI
h_calc_CGS = h_calc_J * 1e7  # 1 Дж = 10^7 эрг
h_tab_CGS = 6.62607015e-27

# Погрешность наклона
n = len(omegas)
residuals = V0_phys - (m * omegas + b)
s2 = np.sum(residuals**2) / (n - 2)
X = np.vstack([omegas, np.ones(n)]).T
cov = s2 * np.linalg.inv(X.T @ X)
dm = np.sqrt(cov[0, 0])
dh_CGS = 2 * np.pi * e * dm * 1e-14 * 1e7

# Красная граница и работа выхода
omega_cr_14 = -b / m
omega_cr_SI = omega_cr_14 * 1e14
c_angstrom = 2.99792458e18
lambda_cr = 2 * np.pi * c_angstrom / omega_cr_SI
W_eV = -b
dW_eV = np.sqrt(cov[1, 1])

# ===== Построение графика =====
fig, ax = plt.subplots(figsize=(9, 6))

ax.errorbar(omegas, V0_phys, yerr=dV0, fmt='o', ms=7, capsize=4, 
            color='black', label='Экспериментальные точки', zorder=5)

omega_line = np.linspace(omegas.min() - 10, omegas.max() + 10, 100)
V0_line = m * omega_line + b

# Формируем строку с уравнением для легенды
# Используем {b:+.4f}, чтобы знак плюс или минус подставился автоматически
eq_str = f"$V_0 = {m:.4f} \\cdot (\\omega / 10^{{14}}) {b:+.4f}$"
legend_str = f"Линейная аппроксимация:\n{eq_str}"

ax.plot(omega_line, V0_line, 'r-', linewidth=2, label=legend_str)

ax.axvline(omega_cr_14, color='green', linestyle='--', linewidth=1.5, 
           label=f'Красная граница: $\\lambda_{{кр}} = {lambda_cr:.0f}$ Å')
ax.plot(omega_cr_14, 0, 'go', ms=8, zorder=6)

for i, N in enumerate(sorted(data.keys())):
    ax.annotate(f'{N}', (omegas[i], V0_phys[i]), 
                textcoords='offset points', xytext=(6, 4), fontsize=10)

ax.set_xlabel('$\\omega$, $10^{14}$ рад/с', fontsize=12)
ax.set_ylabel('Запирающий потенциал $V_0$, В', fontsize=12)
# ax.set_title('Зависимость запирающего потенциала от циклической частоты', 
#              fontsize=13, fontweight='bold')
ax.grid(True, linestyle='--', alpha=0.6)
ax.legend(fontsize=10, loc='upper left')

# Блок с результатами на графике
# textstr = (f'$h = {h_calc_CGS:.3e}$ эрг·с\n'
#            f'$\\Delta h = {dh_CGS:.3e}$ эрг·с\n'
#            f'$W = {W_eV:.3f}$ эВ\n'
#            f'$\\lambda_{{кр}} = {lambda_cr:.0f}$ Å')
# props = dict(boxstyle='round', facecolor='wheat', alpha=0.9)
# ax.text(0.98, 0.02, textstr, transform=ax.transAxes, fontsize=10,
#         verticalalignment='bottom', horizontalalignment='right', bbox=props)

plt.tight_layout()
plt.show()