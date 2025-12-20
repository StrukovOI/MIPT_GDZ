import numpy as np
import matplotlib.pyplot as plt
from scipy.optimize import curve_fit

# Параметры установки
d_diaphragm = 100e-6  # диаметр диафрагмы [м] = 100 мкм
d_diaphragm_cm = 0.01  # диаметр диафрагмы [см]

# Параметры воздуха
T = 293  # температура [K]
M_air = 0.029  # молярная масса воздуха [кг/моль]
R = 8.314  # универсальная газовая постоянная [Дж/(моль·K)]

# Расчет проводимости диафрагмы для молекулярного течения
# Формула из методички: U = 91 * d² [л/с], где d в см
U_diaphragm = 91 * d_diaphragm_cm**2  # [л/с]

# Альтернативный расчет через среднюю скорость
v_avg = np.sqrt(8 * R * T / (np.pi * M_air))  # средняя тепловая скорость [м/с]
S_diaphragm = np.pi * (d_diaphragm/2)**2  # площадь диафрагмы [м²]
U_diaphragm_alt = (S_diaphragm * v_avg) / 4  # [м³/с]
U_diaphragm_alt_l_s = U_diaphragm_alt * 1000  # перевод в л/с

print(f"Проводимость диафрагмы (по методичке): {U_diaphragm:.6f} л/с")
print(f"Проводимость диафрагмы (через v_avg): {U_diaphragm_alt_l_s:.6f} л/с")

# Предположим, у нас есть экспериментальные данные
# Замените эти массивы на ваши реальные данные
time_experiment = np.linspace(0, 3600, 100)  # время [с]
pressure_B3 = 1e-6 * np.exp(-time_experiment/1800) + 2e-7  # давление B3 [Торр]
pressure_B2 = 0.1 * np.exp(-time_experiment/600) + 0.01    # давление B2 [Торр]

# Расчет потока через диафрагму
Q_diaphragm = U_diaphragm * (pressure_B2 - pressure_B3)  # [Торр·л/с]

# Расчет быстроты действия турбомолекулярного насоса
S_turbo = np.where(pressure_B3 > 0, Q_diaphragm / pressure_B3, 0)  # [л/с]

# Аппроксимация кривой откачки
def exp_decay(t, P0, tau, P_lim):
    return P_lim + (P0 - P_lim) * np.exp(-t/tau)

# Выбираем участок для аппроксимации (после установления режима)
start_idx = 20
t_fit = time_experiment[start_idx:]
P_fit = pressure_B3[start_idx:]

# Аппроксимация
try:
    popt, pcov = curve_fit(exp_decay, t_fit, P_fit, 
                          p0=[P_fit[0], 1000, P_fit[-1]],
                          maxfev=5000)
    P0_fit, tau_fit, P_lim_fit = popt
    
    # Расчет объема камеры (если известна средняя быстрота действия)
    S_turbo_avg = np.mean(S_turbo[start_idx:])
    V_calculated = S_turbo_avg * tau_fit  # [л]
    
    fit_success = True
except:
    fit_success = False
    print("Аппроксимация не удалась")

# Построение графиков
fig, ((ax1, ax2), (ax3, ax4)) = plt.subplots(2, 2, figsize=(15, 12))

# График 1: Давление от времени
ax1.semilogy(time_experiment, pressure_B3, 'b-', linewidth=2, label='B3 (высокий вакуум)')
ax1.semilogy(time_experiment, pressure_B2, 'r-', linewidth=2, label='B2 (форвакуум)')
ax1.set_xlabel('Время, с')
ax1.set_ylabel('Давление, Торр')
ax1.set_title('Зависимость давления от времени')
ax1.legend()
ax1.grid(True, alpha=0.3)

# График 2: Поток через диафрагму
ax2.plot(time_experiment, Q_diaphragm, 'g-', linewidth=2)
ax2.set_xlabel('Время, с')
ax2.set_ylabel('Поток Q, Торр·л/с')
ax2.set_title('Поток через диафрагму от времени')
ax2.grid(True, alpha=0.3)

# График 3: Производительность турбомолекулярного насоса
valid_mask = (pressure_B3 > 1e-8) & (S_turbo > 0)
ax3.semilogx(pressure_B3[valid_mask], S_turbo[valid_mask], 'ro-', markersize=4, linewidth=1)
ax3.set_xlabel('Давление P, Торр')
ax3.set_ylabel('Быстрота действия S, л/с')
ax3.set_title('Производительность турбомолекулярного насоса')
ax3.grid(True, alpha=0.3)

# График 4: Аппроксимация кривой откачки
ax4.semilogy(t_fit, P_fit, 'b-', label='Эксперимент', linewidth=2)
if fit_success:
    ax4.semilogy(t_fit, exp_decay(t_fit, *popt), 'r--', 
                label=f'Аппроксимация: τ={tau_fit:.0f} с', linewidth=2)
ax4.set_xlabel('Время, с')
ax4.set_ylabel('Давление P, Торр')
ax4.set_title('Аппроксимация кривой откачки')
ax4.legend()
ax4.grid(True, alpha=0.3)

plt.tight_layout()
plt.savefig('3_turbo_analysis_complete.pdf', dpi=300, bbox_inches='tight')
plt.show()

# Вывод результатов
print("\n" + "="*50)
print("РЕЗУЛЬТАТЫ РАСЧЕТОВ")
print("="*50)
print(f"Диаметр диафрагмы: {d_diaphragm*1e6:.0f} мкм")
print(f"Проводимость диафрагмы: {U_diaphragm:.2e} л/с")
print(f"Средняя быстрота действия турбонасоса: {np.mean(S_turbo[valid_mask]):.1f} л/с")
if fit_success:
    print(f"Параметр аппроксимации τ: {tau_fit:.0f} с")
    print(f"Предельное давление: {P_lim_fit:.2e} Торр")
    print(f"Рассчитанный объем камеры: {V_calculated:.1f} л")