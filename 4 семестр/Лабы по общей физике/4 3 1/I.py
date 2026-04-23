import numpy as np
import matplotlib.pyplot as plt
from scipy.special import fresnel

# ==========================================================
# 1. Расчёт функции Френеля и распределения интенсивности
# ==========================================================
# Безразмерная координата v (от тени к свету)
v = np.linspace(-3.5, 3.5, 1000)

# scipy.special.fresnel возвращает (S(v), C(v))
S, C = fresnel(v)

# Относительная интенсивность для дифракции на полуплоскости (крае экрана)
# I(v)/I_0 = 0.5 * [(0.5 + C(v))^2 + (0.5 + S(v))^2]
I_rel = 0.5 * ((0.5 + C)**2 + (0.5 + S)**2)

# ==========================================================
# 2. Построение графиков
# ==========================================================
plt.style.use('seaborn-v0_8-whitegrid')
fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(14, 6))

# --- График 1: Распределение интенсивности ---
ax1.plot(v, I_rel, color='#1f77b4', linewidth=2.5)
ax1.axvline(0, color='black', linestyle='--', linewidth=1.5, label='Граница света и тени (x=0)')
ax1.set_xlabel('Координата $x$', fontsize=12)
ax1.set_ylabel('Относительная интенсивность $I/I_0$', fontsize=12)
ax1.set_title('Распределение интенсивности на границе света и тени', fontsize=13)
ax1.set_xlim(-3.5, 3.5)
ax1.set_ylim(0, 1.1)
ax1.legend(loc='lower right')
ax1.grid(True, alpha=0.3)
# Аннотации на графике интенсивности
ax1.annotate('Тень', xy=(-2, 0.05), xytext=(-2.5, 0.3),
             arrowprops=dict(arrowstyle='->', color='gray'), fontsize=11)
ax1.annotate('Освещённая область', xy=(2, 0.9), xytext=(1.5, 0.6),
             arrowprops=dict(arrowstyle='->', color='gray'), fontsize=11)
ax1.annotate('$I/I_0 = 0.25$', xy=(0, 0.25), xytext=(-1.2, 0.45),
             arrowprops=dict(arrowstyle='->', color='red'), fontsize=11, color='red')

# --- График 2: Спираль Корню ---
ax2.plot(C, S, color='#1f77b4', linewidth=2, label='Спираль Корню')
ax2.plot([-0.5, 0.5], [-0.5, 0.5], 'ko', markersize=6) # Фокусы спирали

# Вектор амплитуды на краю экрана (v=0)
C0, S0 = 0.0, 0.0
ax2.quiver(-0.5, -0.5, C0 + 0.5, S0 + 0.5, angles='xy', scale_units='xy', 
           scale=1, color='red', width=0.015, label='Вектор на краю ($x=0$)')
ax2.plot(C0, S0, 'ro', markersize=8)

# Вектор амплитуды вдали от края (v → ∞)
C_inf, S_inf = 0.5, 0.5
ax2.quiver(-0.5, -0.5, C_inf + 0.5, S_inf + 0.5, angles='xy', scale_units='xy', 
           scale=1, color='green', width=0.0075, label='Вектор вдали ($x \\to \\infty$)')
ax2.plot(C_inf, S_inf, 'go', markersize=8)

ax2.set_xlabel('$I_1(x)$', fontsize=12)
ax2.set_ylabel('$I_2(x)$', fontsize=12)
ax2.set_title('Спираль Корню и векторы амплитуд', fontsize=13)
ax2.axis('equal')
ax2.set_xlim(-0.8, 0.8)
ax2.set_ylim(-0.8, 0.8)
ax2.legend(loc='upper left')
ax2.grid(True, alpha=0.3)

# Аннотации к векторам
ax2.text(C0 - 0.15, S0 + 0.15, '$x=0$', color='red', fontsize=11, fontweight='bold')
ax2.text(C_inf + 0.05, S_inf + 0.05, '$x \\to \\infty$', color='green', fontsize=11, fontweight='bold')

plt.tight_layout()
plt.show()

# Сохранение рисунков (опционально)
# fig.savefig('fresnel_edge_intensity.png', dpi=300)
# fig.savefig('cornu_spiral_vectors.png', dpi=300)

