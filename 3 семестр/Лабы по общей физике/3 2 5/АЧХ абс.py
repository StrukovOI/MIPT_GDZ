# import numpy as np
# import matplotlib.pyplot as plt
# from scipy.interpolate import CubicSpline

# # Данные для 408 Ом (Q ≈ 10.3)
# nu_nu0_408 = np.array([1, 0.985815603, 0.971631206, 0.957446809, 0.943262411, 
#                        1.014184397, 1.028368794, 1.042553191, 1.056737589, 
#                        1.070921986, 1.085106383])
# U_U0_408 = np.array([1, 0.959, 0.848, 0.637, 0.549, 
#                      0.902, 0.75, 0.638, 0.526, 
#                      0.455, 0.414])

# # Данные для 2000 Ом (Q ≈ 2.4) - значительно шире
# nu_nu0_2000 = np.array([1, 0.91, 0.85, 0.805, 0.75, 
#                         0.70, 0.65, 1.10, 1.15, 
#                         1.20, 1.25, 1.32, 1.35])
# U_U0_2000 = np.array([1, 0.85, 0.70, 0.55, 0.42, 
#                       0.33, 0.27, 0.80, 0.65, 
#                       0.52, 0.42, 0.35, 0.30])

# # Сортировка данных для плавных кривых
# sort_idx_408 = np.argsort(nu_nu0_408)
# sort_idx_2000 = np.argsort(nu_nu0_2000)

# nu_nu0_408_sorted = nu_nu0_408[sort_idx_408]
# U_U0_408_sorted = U_U0_408[sort_idx_408]

# nu_nu0_2000_sorted = nu_nu0_2000[sort_idx_2000]
# U_U0_2000_sorted = U_U0_2000[sort_idx_2000]

# # Создание сглаженных кривых с помощью кубических сплайнов
# cs_408 = CubicSpline(nu_nu0_408_sorted, U_U0_408_sorted)
# cs_2000 = CubicSpline(nu_nu0_2000_sorted, U_U0_2000_sorted)

# # Генерация большего количества точек для плавных кривых
# nu_nu0_smooth = np.linspace(0.65, 1.35, 200)

# U_U0_408_smooth = cs_408(nu_nu0_smooth)
# U_U0_2000_smooth = cs_2000(nu_nu0_smooth)

# # Построение графика
# plt.figure(figsize=(10, 6))

# # Сглаженные резонансные кривые
# plt.plot(nu_nu0_smooth, U_U0_408_smooth, 'r-', linewidth=1.5, alpha=0.8, label='R = 408 Ом (Q≈10.3)')
# plt.plot(nu_nu0_smooth, U_U0_2000_smooth, 'b-', linewidth=1.5, alpha=0.8, label='R = 2000 Ом (Q≈2.4)')

# # Экспериментальные точки (тонкие)
# plt.plot(nu_nu0_408_sorted, U_U0_408_sorted, 'ro', markersize=3, alpha=0.7)
# plt.plot(nu_nu0_2000_sorted, U_U0_2000_sorted, 'bo', markersize=3, alpha=0.7)

# # Настройка графика
# plt.xlabel(r'$\nu/\nu_0$', fontsize=14)
# plt.ylabel(r'$U/U_0$', fontsize=14)
# plt.legend(fontsize=12)
# plt.grid(True, linestyle='--', alpha=0.7)

# # Добавление вертикальной линии на резонансной частоте
# plt.axvline(x=1, color='gray', linestyle=':', alpha=0.7)

# # Добавление горизонтальной линии на уровне 0.707
# plt.axhline(y=1/np.sqrt(2), color='green', linestyle='--', alpha=0.5, label='Уровень 0.707')

# # Установка пределов по осям
# plt.xlim(0.65, 1.35)
# plt.ylim(0, 1.05)

# # Дополнительная сетка
# plt.minorticks_on()
# plt.grid(True, which='minor', linestyle=':', alpha=0.4)

# plt.tight_layout()
# plt.show()

# # Проверка ширины резонансных кривых на уровне 0.707
# def find_width(x, y, level=1/np.sqrt(2)):
#     # Находим точки пересечения с уровнем level
#     crossings = []
#     for i in range(len(x)-1):
#         if (y[i] - level) * (y[i+1] - level) <= 0:
#             # Линейная интерполяция для нахождения точного пересечения
#             x_cross = x[i] + (level - y[i]) * (x[i+1] - x[i]) / (y[i+1] - y[i])
#             crossings.append(x_cross)
    
#     if len(crossings) >= 2:
#         width = crossings[1] - crossings[0]
#         return width, crossings
#     else:
#         return None, crossings

# width_408, crossings_408 = find_width(nu_nu0_smooth, U_U0_408_smooth)
# width_2000, crossings_2000 = find_width(nu_nu0_smooth, U_U0_2000_smooth)

# if width_408 and width_2000:
#     print(f"Ширина резонансной кривой для 408 Ом: {width_408:.3f}")
#     print(f"Ширина резонансной кривой для 2000 Ом: {width_2000:.3f}")
#     print(f"Отношение ширины 2000 Ом к 408 Ом: {width_2000/width_408:.1f}")
#     print(f"Расчетные добротности: Q_408 ≈ {1/width_408:.1f}, Q_2000 ≈ {1/width_2000:.1f}")



import numpy as np
import matplotlib.pyplot as plt
from scipy.optimize import curve_fit

# Данные для 408 Ом (Q ≈ 10.3)
nu_nu0_408 = np.array([1, 0.985815603, 0.971631206, 0.957446809, 0.943262411, 
                       1.014184397, 1.028368794, 1.042553191, 1.056737589, 
                       1.070921986, 1.085106383])
U_U0_408 = np.array([1, 0.959, 0.848, 0.637, 0.549, 
                     0.902, 0.75, 0.638, 0.526, 
                     0.455, 0.414])

# Данные для 2000 Ом (Q ≈ 2.4)
nu_nu0_2000 = np.array([1, 0.91, 0.85, 0.805, 0.75, 
                        0.70, 0.65, 1.10, 1.15, 
                        1.20, 1.25, 1.32, 1.35])
U_U0_2000 = np.array([1, 0.85, 0.70, 0.55, 0.42, 
                      0.33, 0.27, 0.80, 0.65, 
                      0.52, 0.42, 0.35, 0.30])

# Сортировка данных
sort_idx_408 = np.argsort(nu_nu0_408)
sort_idx_2000 = np.argsort(nu_nu0_2000)

nu_nu0_408_sorted = nu_nu0_408[sort_idx_408]
U_U0_408_sorted = U_U0_408[sort_idx_408]

nu_nu0_2000_sorted = nu_nu0_2000[sort_idx_2000]
U_U0_2000_sorted = U_U0_2000[sort_idx_2000]

# === ФИЗИЧЕСКИ ОБОСНОВАННАЯ МОДЕЛЬ С ПОДГОНКОЙ ПАРАМЕТРОВ ===
def rlc_response(nu_nu0, Q, nu0_offset=0, amplitude=1.0, baseline=0):
    """
    Физическая модель АЧХ последовательного RLC контура с параметрами подгонки:
    - Q: добротность (основной параметр формы кривой)
    - nu0_offset: относительное смещение резонансной частоты
    - amplitude: амплитудный коэффициент (учитывает погрешности измерений)
    - baseline: базовый уровень (учитывает помехи и смещение)
    
    Формула обеспечивает физически корректное поведение на всех частотах:
    - На ω << ω₀: U/U₀ → 0
    - На ω = ω₀: U/U₀ = amplitude
    - На ω >> ω₀: U/U₀ → 0
    """
    actual_nu_nu0 = nu_nu0 * (1 + nu0_offset)
    return amplitude / np.sqrt(1 + Q**2 * (actual_nu_nu0 - 1/actual_nu_nu0)**2) + baseline

# === ПОДГОНКА ПАРАМЕТРОВ С ФИЗИЧЕСКИМИ ОГРАНИЧЕНИЯМИ ===
# Для R=408 Ом (узкий резонанс)
p0_408 = [10.0, 0.0, 1.0, 0.0]  # Начальные приближения
bounds_408 = ([5, -0.05, 0.8, -0.1], [20, 0.05, 1.2, 0.1])  # Физические ограничения

popt_408, _ = curve_fit(
    lambda x, Q, nu0_offset, amplitude, baseline: rlc_response(x, Q, nu0_offset, amplitude, baseline),
    nu_nu0_408_sorted, U_U0_408_sorted,
    p0=p0_408, bounds=bounds_408, method='trf'
)
Q_fit_408, nu0_offset_408, amplitude_408, baseline_408 = popt_408

# Для R=2000 Ом (широкий резонанс)
p0_2000 = [2.4, 0.0, 1.0, 0.0]
bounds_2000 = ([1, -0.1, 0.7, -0.1], [5, 0.1, 1.3, 0.1])

popt_2000, _ = curve_fit(
    lambda x, Q, nu0_offset, amplitude, baseline: rlc_response(x, Q, nu0_offset, amplitude, baseline),
    nu_nu0_2000_sorted, U_U0_2000_sorted,
    p0=p0_2000, bounds=bounds_2000, method='trf'
)
Q_fit_2000, nu0_offset_2000, amplitude_2000, baseline_2000 = popt_2000

# === ГЕНЕРАЦИЯ ГЛАДКИХ КРИВЫХ ===
nu_nu0_smooth = np.linspace(0.65, 1.35, 500)
theory_408 = rlc_response(nu_nu0_smooth, Q_fit_408, nu0_offset_408, amplitude_408, baseline_408)
theory_2000 = rlc_response(nu_nu0_smooth, Q_fit_2000, nu0_offset_2000, amplitude_2000, baseline_2000)

# === ПОСТРОЕНИЕ ГРАФИКА ===
plt.figure(figsize=(13, 8))

# Экспериментальные точки
plt.scatter(nu_nu0_408_sorted, U_U0_408_sorted, c='red', s=10, alpha=0.95, linewidth=1.5, zorder=5)
plt.scatter(nu_nu0_2000_sorted, U_U0_2000_sorted, c='blue', s=10, alpha=0.95, linewidth=1.5, zorder=5)

# Теоретические кривые
plt.plot(nu_nu0_smooth, theory_408, 'r-', linewidth=1.5, alpha=0.98, 
         zorder=4, label=f'R = 408 Ом (Q = 10,3)')
plt.plot(nu_nu0_smooth, theory_2000, 'b-', linewidth=1.5, alpha=0.98, 
         zorder=4, label=f'R = 2000 Ом (Q = 2,4)')

# Физические линии уровня
plt.axhline(y=1/np.sqrt(2), color='green', linestyle='--', linewidth=2, alpha=0.85)
plt.axvline(x=1, color='gray', linestyle='--', linewidth=2, alpha=0.7)

# Настройки осей и сетки
plt.xlabel(r'$\nu/\nu_0$', fontsize=16, fontweight='bold')
plt.ylabel(r'$U/U_0$', fontsize=16, fontweight='bold')
plt.xlim(0.64, 1.36)
plt.ylim(-0.05, 1.08)
plt.grid(True, linestyle='--', alpha=0.8, which='major', linewidth=1)
plt.grid(True, linestyle=':', alpha=0.5, which='minor', linewidth=0.7)
plt.minorticks_on()

# Легенда и аннотации
legend = plt.legend(loc='upper right', fontsize=12, framealpha=0.95, edgecolor='gray')
legend.get_frame().set_linewidth(1.5)

# Информация о параметрах
params_info = (f'Подогнанные параметры:\n'
               f'R=408 Ом: Q = {Q_fit_408:.2f}, Амплитуда = {amplitude_408:.3f}\n'
               f'R=2000 Ом: Q = {Q_fit_2000:.2f}, Амплитуда = {amplitude_2000:.3f}')
# plt.annotate(params_info, xy=(0.02, 0.05), xycoords='axes fraction',
#              bbox=dict(boxstyle="round,pad=0.4", fc="white", ec="gray", alpha=0.9),
#              fontsize=10, fontweight='bold')

plt.tight_layout()
plt.show()