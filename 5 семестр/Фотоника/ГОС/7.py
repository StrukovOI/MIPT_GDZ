import numpy as np
import matplotlib.pyplot as plt

# Настройка стиля и шрифтов для красивого отчёта
plt.style.use('seaborn-v0_8-paper')
plt.rcParams['font.family'] = 'serif'
plt.rcParams['font.serif'] = ['Times New Roman', 'DejaVu Serif']
plt.rcParams['axes.unicode_minus'] = False

def fmt(val, decimals=3):
    return f"{val:.{decimals}f}".replace('.', ',')

# =============================================================================
# 1. Точные параметры из нашего расчёта
# =============================================================================
z1 = 79.7   # см
z2 = 49.2   # см
w1 = 0.2713 # мм
w2 = 0.2850 # мм
w0 = 0.1232 # мм
z0 = 64.9   # см
lam = 0.6328e-4 # см (переводим в см для согласованности на графике)

# Массив для плавных кривых
z = np.linspace(20, 100, 500)
# Формула для огибающей в см: w(z) = sqrt(w0^2 + (lam^2 / (pi^2 * w0^2)) * (z - z0)^2)
# Примечание: w0 и lam должны быть в одних единицах (см)
w0_cm = w0 / 10.0
lam_cm = lam
w_z_cm = np.sqrt(w0_cm**2 + (lam_cm**2 / (np.pi**2 * w0_cm**2)) * (z - z0)**2)
w_z_mm = w_z_cm * 10.0 # возвращаем в мм для оси Y

# =============================================================================
# 2. Построение ДВУХПАНЕЛЬНОГО наглядного графика
# =============================================================================
fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(9, 10), gridspec_kw={'height_ratios': [1.2, 1]})

# ---------------- ПАНЕЛЬ 1: Строгий расчётный график ----------------
ax1.plot(z, w_z_mm**2, 'r-', linewidth=2.5, label='Теоретическая парабола $\omega^2(z)$')

# Экспериментальные точки
ax1.errorbar([z1, z2], [w1**2, w2**2], yerr=[2*w1*0.003, 2*w2*0.003], 
             fmt='o', color='blue', markersize=10, capsize=6, capthick=2,
             label='Экспериментальные точки')

# Чёткие указатели на перетяжку
ax1.axvline(x=z0, color='green', linestyle='--', linewidth=1.5, alpha=0.7)
ax1.axhline(y=w0**2, color='green', linestyle='--', linewidth=1.5, alpha=0.7)
ax1.plot(z0, w0**2, 'go', markersize=8)

# Текст с результатами прямо на графике
ax1.text(z0 + 1.5, w0**2 + 0.005, 
         f'Перетяжка:\n$z_0 = {fmt(z0, 1)}$ см\n$\omega_0 = {fmt(w0, 3)}$ мм', 
         fontsize=11, bbox=dict(facecolor='white', alpha=0.9, edgecolor='green', boxstyle='round,pad=0.4'))

ax1.set_ylabel(r'Квадрат радиуса пучка $\omega^2$, мм$^2$', fontsize=12)
ax1.set_title('А. Графическое определение перетяжки по зависимости $\omega^2(z)$', fontsize=13, fontweight='bold')
ax1.legend(loc='upper left', fontsize=10)
ax1.grid(True, alpha=0.4)
ax1.set_xlim(40, 90)
ax1.set_ylim(0, 0.09)

# ---------------- ПАНЕЛЬ 2: Интуитивная визуализация профилей ----------------
# Генерируем поперечные координаты x (в мм)
x = np.linspace(-1.0, 1.0, 400)

# Гауссовы профили, нормированные на максимум (=1) для наглядного сравнения ширин
I1 = np.exp(-2 * (x / w1)**2)
I2 = np.exp(-2 * (x / w2)**2)
I0 = np.exp(-2 * (x / w0)**2)

# Рисуем профили
ax2.plot(x, I1, 'b-', linewidth=2, label=f'Профиль при $z_1 = {fmt(z1, 1)}$ см ($\omega_1 = {fmt(w1, 3)}$ мм)')
ax2.plot(x, I2, 'orange', linewidth=2, label=f'Профиль при $z_2 = {fmt(z2, 1)}$ см ($\omega_2 = {fmt(w2, 3)}$ мм)')
ax2.plot(x, I0, 'g--', linewidth=2, label=f'Профиль в перетяжке $z_0$ ($\omega_0 = {fmt(w0, 3)}$ мм)')

# Показываем уровень 1/e^2, на котором измеряется ширина
ax2.axhline(y=np.exp(-2), color='gray', linestyle=':', linewidth=1.5, label=r'Уровень интенсивности $1/e^2 \approx 0.135$')

# Стрелки, показывающие ширину w1 и w2
ax2.annotate('', xy=(-w1, np.exp(-2)), xytext=(w1, np.exp(-2)),
             arrowprops=dict(arrowstyle='<->', color='blue', lw=1.5))
ax2.text(0, np.exp(-2) + 0.05, r'$2\omega_1$', ha='center', va='bottom', color='blue', fontsize=10)

ax2.annotate('', xy=(-w2, np.exp(-2)), xytext=(w2, np.exp(-2)),
             arrowprops=dict(arrowstyle='<->', color='orange', lw=1.5))
ax2.text(0, np.exp(-2) + 0.15, r'$2\omega_2$', ha='center', va='bottom', color='orange', fontsize=10)

ax2.set_xlabel(r'Поперечная координата $x$, мм', fontsize=12)
ax2.set_ylabel(r'Нормированная интенсивность $I/I_{max}$', fontsize=12)
ax2.set_title('Б. Наглядная связь поперечных профилей с огибающей пучка', fontsize=13, fontweight='bold')
ax2.legend(loc='upper right', fontsize=10)
ax2.grid(True, alpha=0.3, axis='y')
ax2.set_xlim(-0.8, 0.8)
ax2.set_ylim(0, 1.15)

plt.tight_layout()
plt.savefig('gaussian_beam_visualization.png', dpi=300)
print("График сохранён в файл 'gaussian_beam_visualization.png'")
plt.show()