import numpy as np
import matplotlib.pyplot as plt
from scipy.stats import linregress

# Настройка шрифтов для корректного отображения русского текста
plt.rcParams['font.sans-serif'] = ['DejaVu Sans', 'Arial', 'sans-serif']
plt.rcParams['axes.unicode_minus'] = False

# Исходные данные (фон уже вычтен!)
data = {
    'Алюминий (Al)': {
        'thickness': np.array([2, 4, 6, 8, 10, 12, 14, 16, 18, 20, 22]),
        'counts': np.array([111461, 71724, 48372, 31681, 21340, 13978, 9313, 6312, 4185, 2757, 1759]),
        'rho': 2.70,
        'color': '#1f77b4'
    },
    'Железо (Fe)': {
        'thickness': np.array([1, 2, 3, 4, 5, 6, 7, 8]),
        'counts': np.array([93360, 53406, 30119, 17328, 9848, 5583, 3179, 1781]),
        'rho': 7.87,
        'color': '#2ca02c'
    },
    'Свинец (Pb)': {
        'thickness': np.array([0.47, 0.94, 1.41, 1.88, 2.35, 2.82]),
        'counts': np.array([91993, 53813, 30891, 18745, 11197, 6127]),
        'rho': 11.34,
        'color': '#d62728'
    },
    'Пробка': {
        'thickness': np.array([2, 4, 6, 8, 10, 12, 14, 16]),
        'counts': np.array([163451, 161472, 158261, 154827, 151799, 149135, 146522, 144076]),
        'rho': 0.24,
        'color': '#8c564b'
    }
}

print("=" * 80)
print(f"{'Материал':<15} | {'μ (см⁻¹)':<10} | {'μ\' (см²/г)':<12} | {'R²':<8}")
print("-" * 80)

# === ЧАСТЬ 1: Отдельные графики для каждого материала ===
fig_individual, axes_individual = plt.subplots(2, 2, figsize=(14, 10))
axes_individual = axes_individual.flatten()

results = {}

for idx, (material, props) in enumerate(data.items()):
    thickness = props['thickness']
    counts = props['counts']  # Фон уже вычтен!
    rho = props['rho']
    color = props['color']
    
    # Погрешности
    d_counts = np.sqrt(counts)  # Статистическая погрешность √N
    d_ln_counts = d_counts / counts  # Погрешность ln(N) = ΔN/N
    
    # Погрешность толщины: Δx = n * 0.01 см
    d_thickness = np.arange(1, len(thickness) + 1) * 0.01
    
    # Логарифмируем
    ln_counts = np.log(counts)
    
    # Линейная аппроксимация: ln(N) = -μ·x + ln(N₀)
    slope, intercept, r_value, p_value, std_err = linregress(thickness, ln_counts)
    mu = -slope
    mu_prime = mu / rho
    
    results[material] = {
        'mu': mu,
        'mu_prime': mu_prime,
        'intercept': intercept,
        'r_squared': r_value**2
    }
    
    # Форматируем вывод с запятыми
    mu_str = f"{mu:.4f}".replace('.', ',')
    mu_prime_str = f"{mu_prime:.4f}".replace('.', ',')
    r2_str = f"{r_value**2:.4f}".replace('.', ',')
    
    print(f"{material:<15} | {mu_str:<10} | {mu_prime_str:<12} | {r2_str:<8}")
    
    # Построение графика
    ax = axes_individual[idx]
    
    # Экспериментальные точки с планками погрешностей (одинаковые маленькие кружочки)
    ax.errorbar(
        thickness, ln_counts, 
        xerr=d_thickness,
        yerr=d_ln_counts,
        fmt='o', color=color, 
        ecolor=color, 
        elinewidth=1.5, 
        capsize=3, 
        markersize=5, 
        zorder=5, 
        label='Эксп. данные'
    )
    
    # Линия аппроксимации
    thickness_fit = np.linspace(0, max(thickness), 100)
    ln_counts_fit = slope * thickness_fit + intercept
    ax.plot(thickness_fit, ln_counts_fit, color=color, linestyle='-', linewidth=2, 
            label=f'Аппроксимация\nμ = {mu_str} см⁻¹')
    
    ax.set_title(material, fontsize=12, fontweight='bold')
    ax.set_xlabel('Толщина поглотителя $x$, см', fontsize=11)
    ax.set_ylabel('$\ln(N)$', fontsize=11)
    ax.grid(True, alpha=0.4, linestyle='--')
    ax.legend(fontsize=10, loc='upper right')

plt.tight_layout()
plt.savefig('attenuation_individual.png', dpi=300)
print("\nГрафики по отдельности сохранены как 'attenuation_individual.png'")
plt.show()

# === ЧАСТЬ 2: Все графики на одном листе ===
fig_combined, ax_combined = plt.subplots(figsize=(12, 8))

for material, props in data.items():
    thickness = props['thickness']
    counts = props['counts']  # Фон уже вычтен!
    color = props['color']
    
    d_counts = np.sqrt(counts)
    d_ln_counts = d_counts / counts
    d_thickness = np.arange(1, len(thickness) + 1) * 0.01
    
    ln_counts = np.log(counts)
    
    mu = results[material]['mu']
    intercept = results[material]['intercept']
    mu_str = f"{mu:.4f}".replace('.', ',')
    
    # Экспериментальные точки с планками погрешностей (одинаковые маленькие кружочки)
    ax_combined.errorbar(
        thickness, ln_counts, 
        xerr=d_thickness,
        yerr=d_ln_counts,
        fmt='o', color=color, 
        ecolor=color, 
        elinewidth=1.5, 
        capsize=3, 
        markersize=5, 
        zorder=5, 
        label=f'{material} (эксп.)'
    )
    
    # Линия аппроксимации (используем slope и intercept из результатов)
    thickness_fit = np.linspace(0, max(thickness), 100)
    slope = -mu
    ln_counts_fit = slope * thickness_fit + intercept
    ax_combined.plot(thickness_fit, ln_counts_fit, color=color, linestyle='-', linewidth=2, 
                     label=f'{material}: μ = {mu_str} см⁻¹')

ax_combined.set_xlabel('Толщина поглотителя $x$, см', fontsize=13)
ax_combined.set_ylabel('$\ln(N)$', fontsize=13)
# ax_combined.set_title('Ослабление γ-излучения в различных веществах', fontsize=14, fontweight='bold')
ax_combined.legend(fontsize=11, loc='upper right')
ax_combined.grid(True, alpha=0.4, linestyle='--')

plt.tight_layout()
# plt.savefig('attenuation_combined.png', dpi=300)
# print("Общий график сохранён как 'attenuation_combined.png'")
plt.show()

print("\n=== РЕЗУЛЬТАТЫ ===")
print("Линейные (μ) и массовые (μ') коэффициенты ослабления рассчитаны.")
print("Погрешности: статистические (ΔN = √N) и по толщине (Δx = n·0,01 см).")