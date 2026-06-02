import numpy as np
import matplotlib.pyplot as plt
from scipy.special import spherical_jn, spherical_yn

# ==========================================================
# 1. Вспомогательные функции (Риккати-Бессель)
# ==========================================================
def psi_n(n, z): return z * spherical_jn(n, z)
def xi_n(n, z): return z * (spherical_jn(n, z) + 1j * spherical_yn(n, z))

def psi_prime(n, z):
    if n == 0: return np.cos(z)
    return z * spherical_jn(n-1, z) - n * spherical_jn(n, z)

def xi_prime(n, z):
    if n == 0: return np.exp(1j * z)
    j_p = spherical_jn(n-1, z) if n > 0 else spherical_jn(0, z)
    y_p = spherical_yn(n-1, z) if n > 0 else spherical_yn(0, z)
    j_c = spherical_jn(n, z)
    y_c = spherical_yn(n, z)
    return z * (j_p + 1j*y_p) - n * (j_c + 1j*y_c)

# ==========================================================
# 2. Параметры расчёта
# ==========================================================
wavelength = 0.532      # мкм
radius = 1.0            # мкм (умеренный размер для наглядных, но не избыточных осцилляций)
m = 1.33 + 0.0j         # вода / воздух
x = 2 * np.pi * radius / wavelength

theta_deg = np.linspace(0, 180, 1500)
theta_rad = np.deg2rad(theta_deg)
mu = np.cos(theta_rad)

# --- Рэлей ---
I_ray = 1 + np.cos(theta_rad)**2

# --- Ми (точный BHMIE) ---
n_max = int(np.floor(x + 4*x**(1/3) + 2))
a = np.zeros(n_max+1, dtype=complex)
b = np.zeros(n_max+1, dtype=complex)

for n in range(1, n_max+1):
    px, xx, pmx = psi_n(n, x), xi_n(n, x), psi_n(n, m*x)
    ppx, xpx, pmx_p = psi_prime(n, x), xi_prime(n, x), psi_prime(n, m*x)
    a[n] = (m * pmx * ppx - px * pmx_p) / (m * pmx * xpx - xx * pmx_p)
    b[n] = (pmx * ppx - m * px * pmx_p) / (pmx * xpx - m * xx * pmx_p)

# Угловые функции π_n, τ_n
pi = np.zeros((n_max+1, len(mu)))
tau = np.zeros((n_max+1, len(mu)))
pi[1] = np.ones_like(mu)
tau[1] = mu
for n in range(2, n_max+1):
    pi[n] = ((2*n - 1)/(n - 1)) * mu * pi[n-1] - (n/(n - 1)) * pi[n-2]
    tau[n] = n * mu * pi[n] - (n + 1) * pi[n-1]

S1 = np.zeros_like(mu, dtype=complex)
S2 = np.zeros_like(mu, dtype=complex)
for n in range(1, n_max+1):
    f = (2*n + 1) / (n * (n + 1))
    S1 += f * (a[n] * pi[n] + b[n] * tau[n])
    S2 += f * (a[n] * tau[n] + b[n] * pi[n])

I_mie = 0.5 * (np.abs(S1)**2 + np.abs(S2)**2)

# ==========================================================
# 3. Нормализация и выбор шкалы для Ми
# ==========================================================
I_ray_norm = I_ray / I_ray.max()
I_mie_norm = I_mie / I_mie.max()

# >>> НАСТРОЙКА ШКАЛЫ <<<
# Варианты: 'linear', 'moderate_db', 'power'
SCALE_MODE = 'moderate_db'  # ← измените это значение

if SCALE_MODE == 'linear':
    I_mie_vis = I_mie_norm
    r_label = 'Относительная интенсивность'
    r_lim = (0, 1.1)
    r_ticks = [0, 0.5, 1.0]
    
elif SCALE_MODE == 'moderate_db':
    eps = 1e-12
    I_mie_vis = 10 * np.log10(I_mie_norm + eps)  # дБ
    r_label = 'Интенсивность, дБ'
    r_lim = (-25, 0)        # ← умеренный диапазон: видны лепестки до ~300× слабее максимума
    r_ticks = [-25, -20, -15, -10, -5, 0]
    
elif SCALE_MODE == 'power':
    exponent = 0.3  # степень сжатия: 0.2–0.4 даёт хороший баланс
    I_mie_vis = I_mie_norm ** exponent
    r_label = f'$(I/I_{{max}})^{{{exponent}}}$'
    r_lim = (0, 1.1)
    r_ticks = [0, 0.3, 0.6, 1.0]

# Зеркальное отражение для полного круга
def make_full_circle(theta_deg, I):
    theta_back = 360 - theta_deg[-2:0:-1]
    I_back = I[-2:0:-1]
    return np.concatenate([theta_deg, theta_back]), np.concatenate([I, I_back])

theta_ray_full, I_ray_full = make_full_circle(theta_deg, I_ray_norm)
theta_mie_full, I_mie_vis_full = make_full_circle(theta_deg, I_mie_vis)
theta_ray_rad = np.deg2rad(theta_ray_full)
theta_mie_rad = np.deg2rad(theta_mie_full)

# ==========================================================
# 4. Визуализация
# ==========================================================
fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(14, 7), 
                               subplot_kw={'projection': 'polar'})

# --- Рэлей (всегда линейная шкала) ---
ax1.plot(theta_ray_rad, I_ray_full, 'b-', linewidth=2)
ax1.fill(theta_ray_rad, I_ray_full, alpha=0.15, color='blue')
ax1.set_title("Рэлеевское рассеяние", va='bottom', fontsize=13, pad=15)
ax1.set_theta_zero_location('N')
ax1.set_theta_direction(-1)
ax1.set_thetamin(0); ax1.set_thetamax(360)
ax1.set_rlim(0, 1.1); ax1.grid(True, linestyle='--', alpha=0.5)
ax1.text(0, 1.05, '0°', ha='center', fontsize=9)
ax1.text(np.pi, 1.05, '180°', ha='center', fontsize=9)

# --- Ми (выбранная шкала) ---
ax2.plot(theta_mie_rad, I_mie_vis_full, 'r-', linewidth=2)
ax2.fill(theta_mie_rad, I_mie_vis_full, alpha=0.2, color='red')
scale_name = {'linear':'линейная', 'moderate_db':'лог.', 'power':'степенная'}
ax2.set_title(f"Рассеяние Ми, {scale_name[SCALE_MODE]} шкала", va='bottom', fontsize=13, pad=15)
ax2.set_theta_zero_location('N')
ax2.set_theta_direction(-1)
ax2.set_thetamin(0); ax2.set_thetamax(360)
ax2.set_rlim(r_lim)
ax2.set_yticks(r_ticks)
ax2.set_yticklabels([f'{t}' for t in r_ticks], fontsize=8)
ax2.grid(True, linestyle='--', alpha=0.5)
ax2.text(0, r_lim[1]*0.9 if SCALE_MODE=='linear' else -3, '0°', ha='center', fontsize=9)
ax2.text(np.pi, r_lim[1]*0.9 if SCALE_MODE=='linear' else -3, '180°', ha='center', fontsize=9)

# fig.suptitle(f'Индикатрисы рассеяния (частица {radius} мкм, $\lambda={wavelength}$ мкм, $x={x:.1f}$)', 
            #  fontsize=15, y=1.02)
plt.tight_layout()
plt.savefig(f'indicatrices_{SCALE_MODE}.png', dpi=300, bbox_inches='tight')
plt.show()