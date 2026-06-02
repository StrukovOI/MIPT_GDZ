import numpy as np
import matplotlib.pyplot as plt

# --- График 2: Эффективность рассеяния Q_scat от параметра x ---
# Расширяем диапазон до 50, чтобы увидеть затухание осцилляций
x = np.linspace(0.01, 50, 3000)

# Рэлеевский предел: Q_scat ~ (8/3)x^4 для малых x
Q_rayleigh = (8/3) * x**3 

# Аппроксимация осцилляций Ми: сумма затухающих гармоник
# Затухание медленное, чтобы осцилляции были видны до x~30-40
osc1 = 1.0 * np.sin(2.2 * x) * np.exp(-x/15)      # Основная мода
osc2 = 0.6 * np.sin(4.5 * x + 0.5) * np.exp(-x/20) # Вторая гармоника  
osc3 = 0.3 * np.sin(7 * x + 1.0) * np.exp(-x/25)   # Высшие гармоники

# Плавный переход от Рэлея к режиму Ми
transition = 1 - np.exp(-x**2 / 2.5)

Q_mie_approx = (Q_rayleigh * (1 - transition) + 
                (2.0 + osc1 + osc2 + osc3) * transition)

# Для x < 0.6 строго следуем Рэлею
mask = x < 0.6
Q_mie_approx[mask] = Q_rayleigh[mask]

plt.figure(figsize=(12, 7))
plt.plot(x, Q_rayleigh, '--', color='blue', linewidth=2, 
         label=r'Рэлеевское рассеяние ($\propto x^4$)', alpha=0.6)
plt.axhline(2, color='gray', linestyle=':', linewidth=1.5, 
            label=r'Среднее значение $\langle Q \rangle \approx 2$')
plt.plot(x, Q_mie_approx, '-', color='red', linewidth=2.5, 
         label='Рассеяние Ми')

# Аннотации областей
# plt.annotate('Рэлеевский режим', xy=(0.4, 0.5), fontsize=10, color='blue',
#              bbox=dict(boxstyle='round,pad=0.4', facecolor='white', alpha=0.9))
# plt.annotate('Осцилляции Ми', xy=(8, 2.8), fontsize=10, color='red',
#              bbox=dict(boxstyle='round,pad=0.4', facecolor='white', alpha=0.9))
# plt.annotate('Затухание осцилляций', xy=(35, 2.1), fontsize=10, color='darkred',
#              bbox=dict(boxstyle='round,pad=0.4', facecolor='white', alpha=0.9))

# plt.title(r'Эффективность рассеяния $Q_{расс}$ от параметра размера $x$', pad=15, fontsize=14)
plt.xlabel(r'Параметр размера $x = 2\pi a / \lambda$', fontsize=12)
plt.ylabel('Фактор эффективности $Q_{расс}$', fontsize=12)
plt.legend(loc='upper right', fontsize=10)
plt.grid(True, linestyle='--', alpha=0.5)
plt.xlim(0, 50)
plt.ylim(0, 3.5)
plt.xticks(np.arange(0, 51, 5))

plt.tight_layout()
plt.savefig('mie_efficiency_extended.png', dpi=300, bbox_inches='tight')
plt.show()