import numpy as np
import matplotlib.pyplot as plt
from scipy import stats

# Данные из таблицы
inv_R2 = np.array([5.23645E-06, 3.57346E-06, 1.88168E-06, 9.44429E-07, 4.27745E-07, 2.42905E-07])  # 1/Ом²
inv_theta2 = np.array([6.33270407, 4.230202378, 2.169255962, 1.079113914, 0.421412665, 0.285417175])  # 1/θ²

# Исходные данные для расчета погрешностей
R_exp = np.array([437, 529, 729, 1029, 1529, 2029])  # Экспериментальные сопротивления, Ом
theta = np.array([0.397, 0.486, 0.679, 0.963, 1.540, 1.872])  # Значения θ

# Расчет погрешностей
delta_R = 0.5  # Погрешность R, Ом
delta_rel_ab = 0.01  # Относительная погрешность a и b (1%)

# Погрешность 1/R²: Δ(1/R²) = (2/R³) * ΔR
delta_inv_R2 = (2 / R_exp**3) * delta_R

# Погрешность θ: Δθ = θ * √((Δa/a)² + (Δb/b)²) = θ * √(0.01² + 0.01²) = θ * 0.01414
delta_theta = theta * np.sqrt(2 * delta_rel_ab**2)

# Погрешность 1/θ²: Δ(1/θ²) = (2/θ³) * Δθ
delta_inv_theta2 = (2 / theta**3) * delta_theta

# Линейная регрессия (МНК)
slope, intercept, r_value, p_value, std_err = stats.linregress(inv_R2, inv_theta2)

# Создание точек для аппроксимирующей прямой
inv_R2_line = np.linspace(inv_R2.min(), inv_R2.max(), 100)
inv_theta2_line = slope * inv_R2_line + intercept

# Построение графика с погрешностями
plt.figure(figsize=(8, 6))
plt.errorbar(inv_R2, inv_theta2, 
             xerr=delta_inv_R2, 
             yerr=delta_inv_theta2,
             fmt='ro', 
             markersize=6, 
             capsize=4,
             capthick=1,
             elinewidth=1,
             label='Экспериментальные точки')

plt.plot(inv_R2_line, inv_theta2_line, 'b-', linewidth=2, 
         label=r'Аппроксимация: $1/\Theta^2 = 1{,}22\cdot10^6 \cdot 1/R_{\Sigma}^2 - 0{,}0733$')

# Настройка графика
plt.xlabel(r'$1/R_{\Sigma}^2$, Ом⁻²', fontsize=12)
plt.ylabel('$1/\\Theta^2$', fontsize=12)
plt.legend(fontsize=10)
plt.grid(True, linestyle='--', alpha=0.7)

# Вывод параметров аппроксимации
print(f"Коэффициент наклона: {slope:.2e}")
print(f"Свободный член: {intercept:.4f}")
print(f"Коэффициент детерминации R²: {r_value**2:.4f}")
print(f"Стандартная ошибка наклона: {std_err:.2e}")

plt.tight_layout()
plt.show()