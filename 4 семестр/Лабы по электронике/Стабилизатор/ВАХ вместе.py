import numpy as np
import matplotlib.pyplot as plt

# Данные первой ВАХ
U1 = np.array([ 59, 59, 60, 61, 61, 62, 64, 68 ])
I1 = np.array([ 17, 15, 13, 11, 9, 7, 5, 3])

# Данные второй ВАХ
U2 = np.array([ 40, 40, 42, 44, 47, 48, 49, 49])
I2 = np.array([ 15, 13, 11, 9, 7, 5, 3, 1])

# Погрешности (половина последнего разряда) – явно int
dU1 = np.full_like(U1, 1, dtype=int)
dI1 = np.full_like(I1, 1, dtype=int)
dU2 = np.full_like(U2, 1, dtype=int)
dI2 = np.full_like(I2, 1, dtype=int)

# Линейная аппроксимация I = k·U + b
coeffs1 = np.polyfit(U1, I1, 1)
k1, b1 = coeffs1
coeffs2 = np.polyfit(U2, I2, 1)
k2, b2 = coeffs2

print(f'Набор 1: k = {k1:.3f}, b = {b1:.3f}')
print(f'Набор 2: k = {k2:.3f}, b = {b2:.3f}')

# Прямые для аппроксимации
U1_fit = np.linspace(U1.min(), U1.max(), 100)
I1_fit = k1 * U1_fit + b1
U2_fit = np.linspace(U2.min(), U2.max(), 100)
I2_fit = k2 * U2_fit + b2

# Построение
plt.figure(figsize=(10, 6))

plt.errorbar(U1, I1, xerr=dU1, yerr=dI1,
             fmt='o', color='red', markersize=6, capsize=3,
             ecolor='red', elinewidth=1, label='Воздух')
plt.plot(U1_fit, I1_fit, 'b-', linewidth=2,)

plt.errorbar(U2, I2, xerr=dU2, yerr=dI2,
             fmt='s', color='lime', markersize=6, capsize=3,
             ecolor='lime', elinewidth=1, label='Аргон')
plt.plot(U2_fit, I2_fit, 'm-', linewidth=2)

plt.xlabel('Напряжение U (10⁻² кВ)')
plt.ylabel('Ток I (10⁻⁴ А)')
plt.grid(True, linestyle='--', alpha=0.6)
plt.legend()
plt.tight_layout()
plt.show()