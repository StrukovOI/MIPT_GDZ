import numpy as np
from scipy import stats

# Данные
wavelength = np.array([404.7, 435.8, 491.6, 546.1, 577.0, 579.1])  # нм
sin_phi_minus1 = np.array([0.2005, 0.2193, 0.2594, 0.2662, 0.2844, 0.2834])
sin_phi_plus1 = np.array([0.2013, 0.2196, 0.2593, 0.2655, 0.2834, 0.2824])

# Индексы точек для аппроксимации (без 491.6 нм - индекс 2)
indices_approx = [0, 1, 3, 4, 5]

# Инструментальная погрешность гониометра
delta_phi_arcmin = 1.0  # 1 угловая минута
delta_phi_rad = delta_phi_arcmin * np.pi / (180 * 60)  # в радианах

print("="*70)
print("РАСЧЁТ ПЕРИОДА РЕШЁТКИ И ЕГО ПОГРЕШНОСТИ")
print("="*70)

def calculate_grating_period(wavelength, sin_phi, order, indices):
    """Расчёт периода решётки и его погрешности"""
    
    # Данные для аппроксимации
    x = wavelength[indices]
    y = sin_phi[indices]
    n = len(x)
    
    # Линейная регрессия МНК: y = k*x + b
    slope, intercept, r_value, p_value, std_err = stats.linregress(x, y)
    
    # Период решётки: d = m/k (для m=1: d = 1/k)
    d = order / slope  # в нм
    d_um = d * 1e-3    # в мкм
    
    # 1. ПОГРЕШНОСТЬ МНК
    # Стандартная ошибка углового коэффициента
    std_err_slope = std_err
    
    # Погрешность периода из МНК: Δd = Δk/k²
    delta_d_mnk = std_err_slope / (slope**2)  # в нм
    delta_d_mnk_um = delta_d_mnk * 1e-3       # в мкм
    
    # Относительная погрешность МНК
    rel_err_mnk = delta_d_mnk / d * 100
    
    # 2. ИНСТРУМЕНТАЛЬНАЯ ПОГРЕШНОСТЬ
    # Из формулы d = m*λ/sin(φ), дифференцируем:
    # Δd/d = |cot(φ)| * Δφ (в радианах)
    
    # Средний угол для данных
    mean_sin_phi = np.mean(y)
    mean_phi = np.arcsin(mean_sin_phi)
    cot_phi = np.cos(mean_phi) / np.sin(mean_phi)
    
    # Относительная инструментальная погрешность
    rel_err_instr = abs(cot_phi) * delta_phi_rad
    delta_d_instr = d * rel_err_instr  # в нм
    delta_d_instr_um = delta_d_instr * 1e-3  # в мкм
    rel_err_instr_percent = rel_err_instr * 100
    
    # 3. ИТОГОВАЯ ПОГРЕШНОСТЬ (квадратичное сложение)
    rel_err_total = np.sqrt(rel_err_mnk**2 + rel_err_instr_percent**2) / 100
    delta_d_total = d * rel_err_total  # в нм
    delta_d_total_um = delta_d_total * 1e-3  # в мкм
    
    # 4. СТАНДАРТНОЕ ОТКЛОНЕНИЕ ТОЧЕК ОТ ПРЯМОЙ
    y_pred = slope * x + intercept
    residuals = y - y_pred
    std_residual = np.sqrt(np.sum(residuals**2) / (n - 2))
    
    print(f"\n--- ПОРЯДОК СПЕКТРА m = {order:+d} ---")
    print(f"\nПараметры аппроксимации:")
    print(f"  Угловой коэффициент k = {slope:.8f} нм⁻¹")
    print(f"  Стандартная ошибка k: ±{std_err_slope:.8f} нм⁻¹")
    print(f"  Свободный член b = {intercept:.8f}")
    print(f"  R² = {r_value**2:.8f}")
    print(f"  Число точек: {n}")
    
    print(f"\nПериод решётки:")
    print(f"  d = {d:.2f} нм = {d_um:.4f} мкм")
    
    print(f"\nПогрешности:")
    print(f"  1. Погрешность МНК:")
    print(f"     Δd_MNK = {delta_d_mnk:.2f} нм = {delta_d_mnk_um:.4f} мкм")
    print(f"     Относительная: {rel_err_mnk:.2f}%")
    
    print(f"\n  2. Инструментальная погрешность:")
    print(f"     Средний угол φ = {np.degrees(mean_phi):.2f}°")
    print(f"     cot(φ) = {cot_phi:.4f}")
    print(f"     Δφ = {delta_phi_arcmin}' = {delta_phi_rad:.2e} рад")
    print(f"     Δd_instr = {delta_d_instr:.2f} нм = {delta_d_instr_um:.4f} мкм")
    print(f"     Относительная: {rel_err_instr_percent:.2f}%")
    
    print(f"\n  3. Итоговая погрешность:")
    print(f"     Δd_total = √(Δd_MNK² + Δd_instr²)")
    print(f"     Δd_total = {delta_d_total:.2f} нм = {delta_d_total_um:.4f} мкм")
    print(f"     Относительная: {rel_err_total*100:.2f}%")
    
    print(f"\n  4. Стандартное отклонение точек от прямой:")
    print(f"     σ = {std_residual:.6f}")
    
    print(f"\nРЕЗУЛЬТАТ:")
    print(f"  d = ({d_um:.4f} ± {delta_d_total_um:.4f}) мкм")
    print(f"  d = ({d:.2f} ± {delta_d_total:.2f}) нм")
    print(f"  Относительная погрешность: {rel_err_total*100:.2f}%")
    
    return d, delta_d_total, delta_d_mnk, delta_d_instr

# Расчёт для обоих порядков
d_minus1, delta_total_minus1, delta_mnk_minus1, delta_instr_minus1 = \
    calculate_grating_period(wavelength, sin_phi_minus1, -1, indices_approx)

d_plus1, delta_total_plus1, delta_mnk_plus1, delta_instr_plus1 = \
    calculate_grating_period(wavelength, sin_phi_plus1, 1, indices_approx)

# Среднее значение
d_avg = (d_minus1 + d_plus1) / 2
d_avg_um = d_avg * 1e-3

# Погрешность среднего (если независимые измерения)
delta_avg = np.sqrt(delta_total_minus1**2 + delta_total_plus1**2) / 2
delta_avg_um = delta_avg * 1e-3

print("\n" + "="*70)
print("ИТОГОВЫЙ РЕЗУЛЬТАТ (усреднение по обоим порядкам)")
print("="*70)
print(f"\nСредний период решётки:")
print(f"  d = ({d_avg_um:.4f} ± {delta_avg_um:.4f}) мкм")
print(f"  d = ({d_avg:.2f} ± {delta_avg:.2f}) нм")
print(f"  Относительная погрешность: {delta_avg/d_avg*100:.2f}%")

print(f"\nСравнение с номиналом (100 штр/мм → d = 10.00 мкм):")
print(f"  Отклонение от номинала: {abs(d_avg_um - 10.0):.4f} мкм")
print(f"  Относительное отклонение: {abs(d_avg_um - 10.0)/10.0*100:.2f}%")

# Проверка: попадает ли номинал в доверительный интервал
if abs(d_avg_um - 10.0) <= delta_avg_um:
    print(f"  ✓ Номинальное значение попадает в доверительный интервал")
else:
    print(f"  ✗ Номинальное значение НЕ попадает в доверительный интервал")

print("\n" + "="*70)
print("ДОПОЛНИТЕЛЬНЫЕ РАСЧЁТЫ")
print("="*70)

# Число штрихов на мм
N_per_mm = 1 / (d_avg_um)  # штр/мм
delta_N = delta_avg_um / (d_avg_um**2)  # погрешность

print(f"\nЧисло штрихов на 1 мм:")
print(f"  N = {N_per_mm:.2f} ± {delta_N:.2f} штр/мм")

# Разрешающая способность (теоретическая)
# Для полной ширины решётки (предположим, что освещено ~20 мм)
illuminated_width_mm = 20  # мм (оценочно)
N_total = N_per_mm * illuminated_width_mm
print(f"\nТеоретическая разрешающая способность (для m=1, ширина пучка ~{illuminated_width_mm} мм):")
print(f"  R = m·N = 1 × {N_total:.0f} = {N_total:.0f}")
print(f"  Минимальная разрешаемая разность длин волн:")
print(f"  δλ = λ/R = 577 нм / {N_total:.0f} = {577/N_total:.2f} нм")

print("\n" + "="*70)