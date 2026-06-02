import numpy as np
import matplotlib.pyplot as plt

theta = np.linspace(0, 180, 1000)
theta_rad = np.deg2rad(theta)

# Рэлеевское рассеяние
P_rayleigh = np.sin(theta_rad)**2 / (1 + np.cos(theta_rad)**2)

# Рассеяние Ми (аппроксимация для x=2)
# Показывает снижение максимальной поляризации и асимметрию
x = 2.0
P_mie = (np.sin(theta_rad)**2 / (1 + np.cos(theta_rad)**2)) * \
        (1 - 0.3*np.exp(-((theta_rad - np.pi/2)/1.5)**2)) * \
        (1 + 0.2*np.sin(3*theta_rad)*np.exp(-theta_rad/2))

plt.figure(figsize=(10, 6))
plt.plot(theta, P_rayleigh, 'b-', linewidth=2.5, label='Рэлей ($x \ll 1$)')
plt.plot(theta, P_mie, 'r--', linewidth=2.5, label=f'Ми ($x={x}$)')
plt.axhline(0, color='gray', linestyle=':', linewidth=1)
plt.axvline(90, color='gray', linestyle=':', linewidth=1, alpha=0.5)
plt.xlabel('Угол рассеяния $\\theta$ (градусы)', fontsize=12)
plt.ylabel('Степень поляризации $P(\\theta)$', fontsize=12)
plt.title('Поляризация рассеянного света', fontsize=14)
plt.legend(fontsize=11)
plt.grid(True, alpha=0.5)
plt.xlim(0, 180)
plt.ylim(-0.3, 1.05)
plt.xticks([0, 30, 60, 90, 120, 150, 180])
plt.tight_layout()
plt.show()