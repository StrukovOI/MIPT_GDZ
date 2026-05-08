import numpy as np
import matplotlib.pyplot as plt

# Параметры
d = 2000.0  # период решётки, нм (500 штр/мм)
lambda_avg = 578.05  # средняя длина волны жёлтого дублета, нм

# Экспериментальные данные (модуль дисперсии, все значения положительные)
m_exp = np.array([-2, -1, 1, 2])
D_exp = np.array([23.76, 11.43, 11.62, 25.62])  # "/Å (по модулю)
D_err = np.array([0.93, 0.10, 0.10, 0.93])

# Теоретическая дисперсия (по модулю): |D| = |m| / (d * cos(phi)) в "/Å
def D_theory_abs(m, d, lam):
    """Модуль теоретической угловой дисперсии в "/Å"""
    factor = 206265 / 10  # рад/нм -> "/Å
    m_abs = np.abs(m)
    return factor * m_abs / np.sqrt(d**2 - (m_abs * lam)**2)

# Плавная кривая для положительной ветви [0; 2.5]
m_pos = np.linspace(0, 2.5, 200)
D_pos = D_theory_abs(m_pos, d, lambda_avg)

# Отрицательная ветвь — зеркальное отражение относительно оси Y
m_neg = -m_pos
D_neg = D_pos  # D(-m) = D(m)

# Построение графика
fig, ax = plt.subplots(figsize=(9, 6))

# Теоретическая кривая: положительная ветвь
ax.plot(m_pos, D_pos, 'b-', linewidth=2, label='Теория: $|D| = \\frac{|m|}{d\\cos\\varphi_m}$')

# Теоретическая кривая: отрицательная ветвь (отражение)
ax.plot(m_neg, D_neg, 'b-', linewidth=2)

# Экспериментальные точки с погрешностями
ax.errorbar(m_exp, D_exp, yerr=D_err, fmt='ro', capsize=4, 
            label='Эксперимент (|m| = 1, 2)', markersize=8, linewidth=1.5)

# Вертикальная линия m = 0
ax.axvline(0, color='gray', linewidth=0.5, linestyle='--', alpha=0.5)

# Оформление
ax.set_xlabel('Порядок спектра $m$', fontsize=12)
ax.set_ylabel('Угловая дисперсия $|D|$, $^{\prime\prime}$/Å', fontsize=12)
# ax.set_title('Зависимость модуля угловой дисперсии от порядка спектра', fontsize=14, pad=15)
ax.grid(True, alpha=0.3, linestyle='--')
ax.legend(fontsize=10)
ax.set_xlim(-2.8, 2.8)
ax.set_ylim(0, 75)  # только положительные значения

# Подпись параметров
# textstr = f'Параметры:\n$d = {d/1000:.2f}$ мкм\n$\\lambda = {lambda_avg}$ нм'
# props = dict(boxstyle='round', facecolor='wheat', alpha=0.3)
# ax.text(0.02, 0.98, textstr, transform=ax.transAxes, fontsize=9,
#         verticalalignment='top', bbox=props)

plt.tight_layout()
plt.show()

# Численные значения для отчёта
print("="*60)
print("ЗНАЧЕНИЯ ДЛЯ ГРАФИКА")
print("="*60)
print(f"\nТеоретические значения |D|:")
for m in [-2, -1, 1, 2]:
    print(f"  m = {m:+d}: |D| = {D_theory_abs(m, d, lambda_avg):.2f} ″/Å")

print(f"\nЭкспериментальные значения:")
for m, D, err in zip(m_exp, D_exp, D_err):
    print(f"  m = {m:+d}: |D| = {D:.2f} ± {err:.2f} ″/Å")