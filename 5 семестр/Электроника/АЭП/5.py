import numpy as np
import matplotlib.pyplot as plt
from scipy.optimize import curve_fit

# ==========================================
# 1. Данные ручной ВАХ и погрешности
# ==========================================
U_kV = np.array([1.52, 1.54, 1.60, 1.63, 1.65, 1.67, 1.68, 1.71, 1.74, 1.76, 1.79, 1.82, 1.84])
I_uA = np.array([4.25, 5.25, 9.75, 16.25, 19.38, 22.50, 26.25, 33.75, 42.50, 52.50, 62.50, 72.50, 85.00])

dU = 0.01          # Абсолютная погрешность напряжения, кВ
dI = 0.025 * I_uA  # Абсолютная погрешность тока (2.5% от значения), мкА

# ==========================================
# 2. Линейная подгонка в координатах Ф-Н для получения начальных значений
# ==========================================
# ln(I/U²) = ln(C) - D/U
x_lin = 1.0 / U_kV
y_lin = np.log(I_uA / (U_kV**2))

# Линейная регрессия
slope_lin, intercept_lin = np.polyfit(x_lin, y_lin, 1)
D_init = -slope_lin          # D = -наклон (в кВ)
C_init = np.exp(intercept_lin)  # C = e^{свободный член} (в мкА/кВ²)

print(f"Начальные значения из линейной регрессии:")
print(f"   C = {C_init:.4e} мкА/кВ²")
print(f"   D = {D_init:.2f} кВ")

# ==========================================
# 3. Нелинейная подгонка с физическими погрешностями
# ==========================================
def fowler_nordheim(U, C, D):
    return C * U**2 * np.exp(-D / U)

# Используем хорошие начальные значения
p0 = [C_init, D_init]

# Подгонка с весами sigma=dI (взвешенный МНК)
popt, pcov = curve_fit(fowler_nordheim, U_kV, I_uA, p0=p0, sigma=dI, absolute_sigma=True)
C_fit, D_fit = popt
perr = np.sqrt(np.diag(pcov))

print(f"\n✅ Параметры физической аппроксимации Ф-Н:")
print(f"   C = {C_fit:.4e} ± {perr[0]:.2e} мкА/кВ²")
print(f"   D = {D_fit:.2f} ± {perr[1]:.2f} кВ")

# ==========================================
# 4. Построение гладкой кривой
# ==========================================
U_smooth = np.linspace(U_kV.min() - 0.02, U_kV.max() + 0.02, 300)
I_smooth = fowler_nordheim(U_smooth, C_fit, D_fit)

# ==========================================
# 5. Отрисовка графика
# ==========================================
plt.figure(figsize=(9, 6))

# Физическая кривая
plt.plot(U_smooth, I_smooth, color='red', linewidth=1.5,
         label=f'Аппроксимация Ф-Н: $I = C U^2 e^{{-D/U}}$\n'
               f'$C = {C_fit:.2e}$, $D = {D_fit:.2f}$ кВ')

# Экспериментальные точки с крестами погрешностей
plt.errorbar(U_kV, I_uA, xerr=dU, yerr=dI, fmt='o', color='red',
             ecolor='black', capsize=4, markersize=6,
             label='Экспериментальные данные')

plt.xlabel('Напряжение $U$, кВ', fontsize=12)
plt.ylabel('Ток $I$, мкА', fontsize=12)
plt.grid(True, alpha=0.3)
plt.legend(fontsize=10, loc='upper left')
plt.tight_layout()

# plt.savefig('manual_IV.pdf', bbox_inches='tight')
# plt.savefig('manual_IV.png', dpi=300, bbox_inches='tight')
# print("\n✅ manual_IV.pdf/png создан с корректной физической аппроксимацией")
plt.show()