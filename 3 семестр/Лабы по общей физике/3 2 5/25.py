import numpy as np
import matplotlib.pyplot as plt
from scipy.interpolate import CubicSpline

# Данные для 408 Ом
nu_nu0_408 = np.array([1, 0.985815603, 0.971631206, 0.957446809, 0.943262411, 
                       1.014184397, 1.028368794, 1.042553191, 1.056737589, 
                       1.070921986, 1.085106383])
U_U0_408 = np.array([1, 0.95959596, 0.828282828, 0.676767677, 0.535353535, 
                     0.898989899, 0.757575758, 0.636363636, 0.525252525, 
                     0.454545455, 0.414141414])

# Данные для 2000 Ом
nu_nu0_2000 = np.array([1, 0.985815603, 0.971631206, 0.957446809, 0.943262411, 
                        0.929078014, 0.914893617, 0.90070922, 1.014184397, 
                        1.028368794, 1.042553191, 1.056737589, 1.070921986, 
                        1.085106383, 1.09929078, 1.113475177])
U_U0_2000 = np.array([1, 0.919191919, 0.777777778, 0.636363636, 0.505050505, 
                      0.414141414, 0.353535354, 0.292929293, 0.939393939, 
                      0.818181818, 0.676767677, 0.555555556, 0.474747475, 
                      0.414141414, 0.373737374, 0.333333333])

# Сортировка данных для плавных кривых
sort_idx_408 = np.argsort(nu_nu0_408)
sort_idx_2000 = np.argsort(nu_nu0_2000)

nu_nu0_408_sorted = nu_nu0_408[sort_idx_408]
U_U0_408_sorted = U_U0_408[sort_idx_408]

nu_nu0_2000_sorted = nu_nu0_2000[sort_idx_2000]
U_U0_2000_sorted = U_U0_2000[sort_idx_2000]

# Создание сглаженных кривых с помощью кубических сплайнов
cs_408 = CubicSpline(nu_nu0_408_sorted, U_U0_408_sorted)
cs_2000 = CubicSpline(nu_nu0_2000_sorted, U_U0_2000_sorted)

# Генерация большего количества точек для плавных кривых
nu_nu0_smooth = np.linspace(min(nu_nu0_2000_sorted.min(), nu_nu0_408_sorted.min()), 
                           max(nu_nu0_2000_sorted.max(), nu_nu0_408_sorted.max()), 200)

U_U0_408_smooth = cs_408(nu_nu0_smooth)
U_U0_2000_smooth = cs_2000(nu_nu0_smooth)

# Построение графика
plt.figure(figsize=(10, 6))

# Сглаженные резонансные кривые
plt.plot(nu_nu0_smooth, U_U0_408_smooth, 'r-', linewidth=1.5, alpha=0.8, label='R = 408 Ом')
plt.plot(nu_nu0_smooth, U_U0_2000_smooth, 'b-', linewidth=1.5, alpha=0.8, label='R = 2000 Ом')

# Экспериментальные точки (тонкие)
plt.plot(nu_nu0_408_sorted, U_U0_408_sorted, 'ro', markersize=3, alpha=0.7)
plt.plot(nu_nu0_2000_sorted, U_U0_2000_sorted, 'bo', markersize=3, alpha=0.7)

# Настройка графика
plt.xlabel(r'$\nu/\nu_0$', fontsize=14)
plt.ylabel(r'$U/U_0$', fontsize=14)
# plt.title('Резонансные кривые колебательного контура', fontsize=16)
plt.legend(fontsize=12)
plt.grid(True, linestyle='--', alpha=0.7)

# Добавление вертикальной линии на резонансной частоте
plt.axvline(x=1, color='gray', linestyle=':', alpha=0.7)

# Установка пределов по осям
plt.xlim(0.89, 1.16)
plt.ylim(0, 1.05)

# Дополнительная сетка
plt.minorticks_on()
plt.grid(True, which='minor', linestyle=':', alpha=0.4)

plt.tight_layout()
plt.show()