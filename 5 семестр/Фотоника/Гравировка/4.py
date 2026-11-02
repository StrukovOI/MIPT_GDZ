import numpy as np
import matplotlib.pyplot as plt

# Настройка шрифтов
plt.rcParams['font.sans-serif'] = ['Arial', 'DejaVu Sans', 'Helvetica']
plt.rcParams['axes.unicode_minus'] = False

# Данные (без первой точки 13.5 А)
I = np.array([13.8, 14.1, 14.4, 14.7, 15.0, 15.3, 15.6, 15.9, 16.2, 16.5, 16.8, 17.1, 17.4])
P_out = np.array([2, 40, 102, 182, 264, 352, 460, 570, 680, 820, 922, 1015, 1082])
# FWHM = np.array([0.45, 0.43, 0.43, 0.4225, 0.375, 0.34, 0.3275, 0.315, 0.2825, 0.2725, 0.2825, 0.261, 0.265])
trailing = np.array([0.39, 0.37, 0.38, 0.36, 0.275, 0.265, 0.225, 0.26, 0.215, 0.215, 0.215, 0.19, 0.192])
leading = np.array([0.51, 0.49, 0.48, 0.485, 0.475, 0.415, 0.43, 0.37, 0.35, 0.33, 0.35, 0.332, 0.338])

# Мощность накачки (напряжение ~168 В)
V_pump = 168.0
P_pump = I * V_pump

# Линеаризация и аппроксимация для каждой кривой
def fit_and_predict(y):
    inv_y = 1.0 / y
    a, b = np.polyfit(P_pump, inv_y, 1)
    P_smooth = np.linspace(min(P_pump), max(P_pump), 200)
    y_fit = 1.0 / (a * P_smooth + b)
    return P_smooth, y_fit, a, b

# P_s_fwhm, fwhm_fit, a_fwhm, b_fwhm = fit_and_predict(FWHM)
P_s_trail, trail_fit, a_trail, b_trail = fit_and_predict(trailing)
P_s_lead, lead_fit, a_lead, b_lead = fit_and_predict(leading)

# Построение графика
plt.figure(figsize=(10, 7))

# Экспериментальные точки
# plt.errorbar(P_pump, FWHM, yerr=0.02, fmt='ko', ecolor='gray', capsize=2, markersize=5, label='FWHM')
plt.errorbar(P_pump, trailing, yerr=0.02, fmt='bo', ecolor='gray', capsize=2, markersize=5, label='Задний фронт')
plt.errorbar(P_pump, leading, yerr=0.02, fmt='ro', ecolor='gray', capsize=2, markersize=5, label='Передний фронт')

# Аппроксимации
# plt.plot(P_s_fwhm, fwhm_fit, 'k-', linewidth=1.5)
plt.plot(P_s_trail, trail_fit, 'b-', linewidth=1.5)
plt.plot(P_s_lead, lead_fit, 'r-', linewidth=1.5)

plt.xlabel('Мощность накачки $P_{\\text{нак}}$, Вт', fontsize=13)
plt.ylabel('Длительность, мкс', fontsize=13)
# plt.title('Зависимость длительности импульса и его фронтов от мощности накачки\n(режим модуляции добротности)', fontsize=14)
plt.legend(fontsize=11, loc='upper right')
plt.grid(True, linestyle=':', alpha=0.8)
plt.tight_layout()

# plt.savefig('pulse_duration_all.png', dpi=300)
# print("График сохранен как 'pulse_duration_all.png'")
print(f"\nПараметры аппроксимации τ = 1/(aP + b):")
# print(f"  FWHM:        a = {a_fwhm:.6f}, b = {b_fwhm:.4f}")
print(f"  Задний фронт: a = {a_trail:.6f}, b = {b_trail:.4f}")
print(f"  Передний фронт: a = {a_lead:.6f}, b = {b_lead:.4f}")

plt.show()