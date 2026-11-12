import numpy as np
import matplotlib.pyplot as plt

plt.rcParams['font.family'] = 'serif'
plt.rcParams['font.serif'] = ['Times New Roman', 'DejaVu Serif']
plt.rcParams['axes.unicode_minus'] = False

def get_lambda(N):
    return 1.5734e-3 * N**2 - 5.8206 * N + 10653.67

c = 2.99792458e18  # скорость света, Å/с

# Наборы данных: N -> (V, V(I))
raw = {
    2830: ([1.998,1.874,1.756,1.651,1.55,1.436,1.368,1.234,1.144,1.073,
            0.973,0.854,0.761,0.605,0.467,0.326],
           [0.284,0.263,0.244,0.222,0.205,0.183,0.167,0.139,0.124,0.112,
            0.096,0.078,0.065,0.046,0.032,0.02]),
    2460: ([2.156,2.026,1.927,1.823,1.682,1.563,1.488,1.395,1.258,1.132,0.999,
            0.674],
           [0.182,0.168,0.158,0.145,0.129,0.118,0.106,0.099,0.084,0.071,0.059,
            0.033]),
    2200: ([2.329,2.111,1.965,1.854,1.744,1.647,1.552,1.405,1.248,1.108,0.966,
            0.807,0.621,0.435],
           [0.129,0.11,0.1,0.092,0.084,0.078,0.072,0.061,0.052,0.044,0.038,
            0.03,0.021,0.013]),
    2300: ([2.373,2.127,1.973,1.851,1.75,1.648,1.526,1.404,1.251,1.104,0.959,
            0.802,0.62,0.416],
           [0.166,0.139,0.126,0.113,0.104,0.095,0.086,0.075,0.064,0.055,0.046,
            0.036,0.026,0.017]),
    2550: ([2.374,2.128,1.972,1.855,1.743,1.608,1.409,1.207,1.014,0.811,0.604,
            0.407],
           [0.269,0.23,0.205,0.189,0.171,0.151,0.122,0.097,0.075,0.055,0.037,
            0.022]),
}



key = 2460
delta = -0.002  # на сколько прибавляем

first, second = raw[key]
raw[key] = (first, [x + delta for x in second])


# Диапазон V для линейной экстраполяции (область запирания)
V_lo, V_hi = 0.0030, 2.60

results = {}
for N, (V, VI) in raw.items():
    V, VI = np.array(V), np.array(VI)
    lam = get_lambda(N)
    nu = c / lam
    # берём только положительные токи и линейный участок
    m = (VI > 0) & (V >= V_lo) & (V <= V_hi)
    xv, yv = V[m], np.sqrt(VI[m])
    k, b = np.polyfit(xv, yv, 1)
    # ошибка через ковариацию (остаточная дисперсия)
    r = yv - (k*xv + b)
    n = len(xv)
    s2 = np.sum(r**2)/(n-2)
    X = np.vstack([xv, np.ones(n)]).T
    cov = s2 * np.linalg.inv(X.T @ X)
    # V0 = -b/k ; распространение ошибки
    V0 = -b/k
    dV0 = np.sqrt((cov[1,1]/k**2) + (b**2*cov[0,0]/k**4) - 2*b*cov[0,1]/k**3)
    r2 = 1 - np.sum(r**2)/np.sum((yv-yv.mean())**2)
    results[N] = dict(lam=lam, nu=nu, V0=V0, dV0=dV0, k=k, b=b, r2=r2,
                      xv=xv, yv=yv, V=V, VI=VI)
    print(f"N={N}  λ={lam:7.1f} Å  ν={nu/1e14:5.3f}·10¹⁴ Гц  "
          f"V0={V0:+.3f}±{dV0:.3f}  (R²={r2:.4f})")

# ===== График 1: серия √I = f(V) =====
fig, ax = plt.subplots(figsize=(10, 6.5))
colors = {2200:'tab:blue', 2300:'tab:cyan', 2460:'tab:green',
          2550:'tab:orange', 2830:'tab:red'}
for N, d in results.items():
    V, VI = d['V'], d['VI']
    pos = VI > 0
    ax.plot(V[pos], np.sqrt(VI[pos]), 'o', ms=4, color=colors[N], alpha=0.7)
    # линия экстраполяции
    xl = np.linspace(-1.1, 2.7, 50)
    ax.plot(xl, d['k']*xl + d['b'], '-', color=colors[N], lw=1.5)
    ax.axvline(d['V0'], color=colors[N], ls=':', lw=1)
    ax.plot(d['V0'], 0, 'x', ms=9, mew=2, color=colors[N])
ax.axhline(0, color='k', lw=0.8)
ax.set_xlabel('Напряжение $V$, В', fontsize=12)
ax.set_ylabel('$\\sqrt{I}$, усл. ед.', fontsize=12)
# ax.set_title('Серия зависимостей $\\sqrt{I}=f(V)$ и экстраполяция к оси абсцисс',
#              fontsize=13, fontweight='bold')
ax.grid(True, ls='--', alpha=0.5)
ax.set_xlim(-0.3, 2.7); ax.set_ylim(-0.02, 0.62)
ax.legend(handles=[plt.Line2D([0],[0], color=colors[N], marker='o', ls='-',
          label=f'N={N}, λ={results[N]["lam"]:.0f} Å, $V_0$={results[N]["V0"]:+.2f}')
          for N in raw], fontsize=9, loc='upper left')
plt.tight_layout(); plt.show()

# ===== График 2: V0(ν) — проверка тренда и сдвига =====
fig2, ax2 = plt.subplots(figsize=(8, 5.5))
Ns = sorted(results, key=lambda N: results[N]['nu'])
nus = np.array([results[N]['nu'] for N in Ns])
v0s = np.array([results[N]['V0'] for N in Ns])
errs = np.array([results[N]['dV0'] for N in Ns])
ax2.errorbar(nus/1e14, v0s, yerr=errs, fmt='o', ms=7, capsize=3,
             color='k', label='экстраполяция')
for N in Ns:
    ax2.annotate(f'{results[N]["lam"]:.0f}', (results[N]['nu']/1e14, results[N]['V0']),
                 textcoords='offset points', xytext=(6,4), fontsize=9)
# регрессия по всем 5
m_all, b_all = np.polyfit(nus, v0s, 1)
xl = np.linspace(nus.min()*0.98, nus.max()*1.02, 50)
ax2.plot(xl/1e14, m_all*xl + b_all, 'r--', label='регрессия по всем 5')
# регрессия без 2830 и 2460
keep = [N for N in Ns if N not in (2830, 2460)]
nu3 = np.array([results[N]['nu'] for N in keep])
v03 = np.array([results[N]['V0'] for N in keep])
m3, b3 = np.polyfit(nu3, v03, 1)
ax2.plot(xl/1e14, m3*xl + b3, 'g-', lw=2, label='регрессия без 2830, 2460')
ax2.set_xlabel('Частота $\\nu$, $10^{14}$ Гц', fontsize=12)
ax2.set_ylabel('$V_0$, В', fontsize=12)
ax2.set_title('Проверка линейности $V_0(\\nu)$', fontsize=13, fontweight='bold')
ax2.grid(True, ls='--', alpha=0.5); ax2.legend(fontsize=9)
plt.tight_layout(); plt.show()

e = 1.602176634e-19
print(f"\nНаклон по всем 5:  {m_all:.4e} В/с -> h = {e*m_all:.4e} Дж·с")
print(f"Наклон без 2830,2460: {m3:.4e} В/с -> h = {e*m3:.4e} Дж·с")
print("Табличное h = 6.626e-34 Дж·с")