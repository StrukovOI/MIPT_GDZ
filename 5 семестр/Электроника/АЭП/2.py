import numpy as np
import matplotlib.pyplot as plt
from scipy import stats

# ==========================================
# 1. Исходные данные
# ==========================================
U_in_V = np.array([6.6, 6.7, 7.0, 1.63, 1.65, 1.67, 1.68, 1.71, 1.74, 1.76, 1.79, 1.82, 1.84])
U_kV = np.array([1.52, 1.54, 1.60, 1.63, 1.65, 1.67, 1.68, 1.71, 1.74, 1.76, 1.79, 1.82, 1.84])
I_uA = np.array([4.25, 5.25, 9.75, 16.25, 19.38, 22.50, 26.25, 33.75, 42.50, 52.50, 62.50, 72.50, 85.00])

# Перевод в базовые единицы (Вольты и Амперы) для формул
U_V = U_kV * 1000.0
I_A = I_uA * 1e-6

# ==========================================
# 2. Параметры для расчёта
# ==========================================
phi = 4.7       # Работа выхода для углеродных материалов, эВ
R_cm = 0.1      # Расстояние катод-анод = 1 мм = 0.1 см
k_geom = 0.5    # Геометрический коэффициент (1/2 для параболического острия)
gamma = 1.7     # Фактор сжатия (среднее значение)
B_const = 6.83e7 # Константа из уравнения ФН

# Погрешности
dU_kV = 0.01    # Абсолютная погрешность напряжения, кВ
dI_rel = 0.025  # Относительная погрешность тока (2.5%)

# ==========================================
# 3. Подготовка данных для координат ФН
# ==========================================
x = 1.0 / U_V
y = np.log(I_A / (U_V**2))

# Погрешности для графика
# dy = sqrt((dI/I)^2 + (2*dU/U)^2)
dy = np.sqrt(dI_rel**2 + (2 * dU_kV / U_kV)**2)

# Линейная регрессия с весами (взвешенный МНК)
weights = 1.0 / dy**2
slope, intercept, r_value, p_value, std_err = stats.linregress(x, y)

# Для взвешенной регрессии можно использовать polyfit с весами
# Но для простоты используем обычную linregress, std_err уже учитывает разброс

# ==========================================
# 4. Расчёт физических величин
# ==========================================
# Форм-фактор: beta = -B * phi^(3/2) / slope
beta = -B_const * (phi**1.5) / slope

# Погрешность beta: d_beta/beta = sqrt((d_slope/slope)^2 + (1.5*d_phi/phi)^2)
# Принимаем d_phi = 0.1 эВ (типичная неопределённость работы выхода)
d_phi = 0.1
d_beta_beta = np.sqrt((std_err/abs(slope))**2 + (1.5 * d_phi / phi)**2)
d_beta = beta * d_beta_beta

# Радиус острия: r = R / (k_geom * beta)
r_cm = R_cm / (k_geom * beta)
r_nm = r_cm * 1e7  # Перевод см в нанометры

# Погрешность r: dr/r = sqrt((dR/R)^2 + (dbeta/beta)^2)
# Принимаем dR = 0.01 см (погрешность задания расстояния)
dR = 0.01
dr_r = np.sqrt((dR/R_cm)**2 + (d_beta/beta)**2)
dr_nm = r_nm * dr_r

# Увеличение микроскопа: M = R / (gamma * r)
M = R_cm / (gamma * r_cm)

# Погрешность M: dM/M = sqrt((dR/R)^2 + (dr/r)^2 + (dgamma/gamma)^2)
# Принимаем dgamma = 0.2 (разброс фактора сжатия)
dgamma = 0.2
dM_M = np.sqrt((dR/R_cm)**2 + (dr_r)**2 + (dgamma/gamma)**2)
dM = M * dM_M

# Коэффициент детерминации
r_squared = r_value**2

# ==========================================
# 5. Функция для форматирования с ЗАПЯТОЙ
# ==========================================
def fmt(val, decimals=2):
    """Форматирует число с запятой вместо точки"""
    return f"{val:.{decimals}f}".replace('.', ',')

def fmt_sci(val, decimals=2):
    """Форматирует число в научном формате с запятой"""
    if abs(val) < 0.01 or abs(val) >= 1000:
        return f"{val:.{decimals}e}".replace('.', ',')
    else:
        return f"{val:.{decimals}f}".replace('.', ',')

# ==========================================
# 6. Вывод результатов для отчёта
# ==========================================
print("="*60)
print("РЕЗУЛЬТАТЫ РАСЧЁТА ДЛЯ ОТЧЁТА")
print("="*60)
print(f"Наклон прямой ФН (k):          {fmt(slope, 2)} ± {fmt(std_err, 2)}")
print(f"Свободный член (b):            {fmt(intercept, 2)}")
print(f"Коэффициент детерминации R²:   {fmt(r_squared, 4)}")
print("-" * 60)
print(f"Форм-фактор острия (β):        {fmt_sci(beta, 2)} ± {fmt_sci(d_beta, 2)} см⁻¹")
print(f"Радиус закругления (r):        {fmt(r_nm, 2)} ± {fmt(dr_nm, 2)} нм")
print(f"Коэффициент увеличения (M):    {fmt(M, 0)} ± {fmt(dM, 0)}")
print("="*60)
print("\nПараметры расчёта:")
print(f"  Работа выхода φ = {fmt(phi, 1)} ± {fmt(d_phi, 1)} эВ")
print(f"  Расстояние R = {fmt(R_cm*10, 1)} ± {fmt(dR*10, 2)} мм")
print(f"  Фактор сжатия γ = {fmt(gamma, 1)} ± {fmt(dgamma, 1)}")
print("="*60)

# ==========================================
# 7. Построение графика с погрешностями
# ==========================================
plt.figure(figsize=(9, 7))

# Экспериментальные точки с погрешностями
plt.errorbar(x, y, yerr=dy, fmt='ro', capsize=4, label='Экспериментальные точки', 
             ecolor='red', elinewidth=1.5, capthick=1.5, zorder=5)

# Линия аппроксимации
x_fit = np.linspace(min(x)*0.99, max(x)*1.01, 100)
y_fit = slope * x_fit + intercept
plt.plot(x_fit, y_fit, 'b-', linewidth=2, 
         label=f'Линейная аппроксимация\n$y = {fmt(slope, 1)}x + ({fmt(intercept, 1)})$')

# Оформление
# plt.title('Вольт-амперная характеристика в координатах Фаулера–Нордгейма', 
#           fontsize=12, fontweight='bold')
plt.xlabel(r'$1/U$, В$^{-1}$', fontsize=12)
plt.ylabel(r'$\ln(I/U^2)$, А/В$^2$', fontsize=12)
plt.grid(True, linestyle='--', alpha=0.7)
plt.legend(fontsize=10, loc='best')
plt.tight_layout()

# Сохранение графика
# plt.savefig('fn_plot.pdf', format='pdf', bbox_inches='tight')
# plt.savefig('fn_plot.png', format='png', dpi=300, bbox_inches='tight')
# print("\n✓ График сохранён как 'fn_plot.pdf' и 'fn_plot.png'")
plt.show()

# ==========================================
# 8. Таблица данных для LaTeX
# ==========================================
print("\n" + "="*60)
print("ТАБЛИЦА ДЛЯ ВСТАВКИ В LATEX:")
print("="*60)
print("\\begin{tabular}{|c|c|c|c|}")
print("\\hline")
print("$U$, В & $1/U$, В$^{-1}$ & $\\ln(I/U^2)$ & $\\Delta[\\ln(I/U^2)]$ \\\\")
print("\\hline")
for i in range(len(U_V)):
    print(f"{U_V[i]:.0f} & {fmt(x[i], 4)} & {fmt(y[i], 2)} & {fmt(dy[i], 3)} \\\\")
print("\\hline")
print("\\end{tabular}")