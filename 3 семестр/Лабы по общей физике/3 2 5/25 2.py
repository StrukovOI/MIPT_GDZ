import numpy as np
import matplotlib.pyplot as plt

# Параметры контура (на основе предыдущих расчетов)
L = 0.000655   # Гн (0.655 мГн)
C = 7.78e-11   # Ф (77.8 пФ)
f0 = 705000    # Гц (705 кГц - резонансная частота)
omega0 = 2 * np.pi * f0

# Диапазон частот для построения (в Гц)
f_min = 600000  # 600 кГц
f_max = 800000  # 800 кГц
f = np.linspace(f_min, f_max, 1000)
omega = 2 * np.pi * f

# Функция для вычисления фазы
def phase(omega, R_eff):
    return -np.arctan2(omega*L - 1/(omega*C), R_eff)

# Вычисляем фазы для двух случаев
# Для R = 408 Ом используем R_eff = 408 Ом
# Для R = 2000 Ом используем R_eff = 760 Ом (расчетное эффективное сопротивление)
phi_408 = phase(omega, 408)
phi_760 = phase(omega, 760)

# Переводим фазы в градусы
phi_408_deg = np.degrees(phi_408)
phi_760_deg = np.degrees(phi_760)

# Построение графика
plt.figure(figsize=(10, 6))
plt.plot(f/1000, phi_408_deg, 'r-', linewidth=1.5, label='R = 408 Ом')
plt.plot(f/1000, phi_760_deg, 'b-', linewidth=1.5, label='R = 2000 Ом')
plt.axvline(f0/1000, color='gray', linestyle='--', alpha=0.7, label=f'Резонансная частота {f0/1000} кГц')
plt.axhline(0, color='gray', linestyle=':', alpha=0.5)

# Настройка графика
plt.xlabel('Частота, кГц', fontsize=12)
plt.ylabel('Фаза, градусы', fontsize=12)
plt.title('Теоретические ФЧХ колебательного контура', fontsize=14)
plt.legend(fontsize=10)
plt.grid(True, linestyle='--', alpha=0.7)

# Установка пределов по осям
plt.xlim(f_min/1000, f_max/1000)
plt.ylim(-90, 90)

# Добавление дополнительной сетки
plt.minorticks_on()
plt.grid(True, which='minor', linestyle=':', alpha=0.4)

plt.tight_layout()
plt.show()