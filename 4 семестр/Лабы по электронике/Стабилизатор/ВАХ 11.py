import numpy as np
import matplotlib.pyplot as plt

# Исходные данные: U в 10^-2 кВ, I в 10^-4 А
U = np.array([59, 59, 60, 61, 61, 62, 64, 68])
I = np.array([17, 15, 13, 11, 9, 7, 5, 3])

# U = np.array([ 125, 122, 120, 118, 115])
# I = np.array([ 9, 7, 5, 3, 1])

# Аргон
# Первая ВАХ
# U = np.array([ 40, 40, 42, 44, 47, 48, 49, 49])
# I = np.array([ 15, 13, 11, 9, 7, 5, 3, 1])

# Вторая ВАХ
# U = np.array([ 93, 93, 92, 89, 86, 83, 80, 76, 69])
# I = np.array([ 17, 15, 13, 11, 9, 7, 5, 3, 1])

# Погрешности: половина последнего разряда (явно указываем int)
dU = np.full_like(U, 1, dtype=int)   # для напряжения
dI = np.full_like(I, 1, dtype=int)   # для тока

print(*dU)  # теперь должно вывести 0.5 0.5 ...

# Линейная аппроксимация
coeffs = np.polyfit(U, I, 1)
k, b = coeffs
print(f'Коэффициенты аппроксимации: k = {k:.3f}, b = {b:.3f}')

U_fit = np.linspace(U.min(), U.max(), 100)
I_fit = k * U_fit + b

plt.figure(figsize=(10, 6))
plt.errorbar(U, I, xerr=dU, yerr=dI, fmt='ro', markersize=8, capsize=3,
             label='Экспериментальные точки')
plt.plot(U_fit, I_fit, 'b-', linewidth=2,
         label=f'Линейная аппроксимация: I = {k:.2f}·U + {b:.2f}')

plt.xlabel('Напряжение U (10⁻² кВ)')
plt.ylabel('Ток I (10⁻⁴ А)')
plt.grid(True, linestyle='--', alpha=0.6)
plt.legend()
plt.tight_layout()
plt.show()