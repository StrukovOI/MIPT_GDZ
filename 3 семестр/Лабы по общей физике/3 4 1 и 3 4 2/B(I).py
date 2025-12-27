import matplotlib.pyplot as plt
import numpy as np

# Данные
I = np.array([0.24, 0.54, 0.93, 1.21, 1.51, 1.9, 2.2, 2.5, 2.8, 3.02])
B = np.array([0.069444444, 0.166666667, 0.298611111, 0.375, 0.458333333,
              0.583333333, 0.666666667, 0.75, 0.805555556, 0.861111111])

# Погрешности (измените эти значения по необходимости)
dI = np.array([0.01]*len(I))  # Погрешность по току
dB = np.array([0.014]*len(B))  # Погрешность по магнитному полю

# Создание графика
plt.figure(figsize=(10, 6))

# Экспериментальные точки с крестами погрешностей
plt.errorbar(I, B, xerr=dI, yerr=dB, fmt='o', color='blue', 
             capsize=5, capthick=1, label='Экспериментальные точки')

# Аппроксимирующая прямая
I_fit = np.linspace(0, 3.2, 100)
B_fit = 0.296 * I_fit
plt.plot(I_fit, B_fit, 'r', label='Линейная аппрокисмация B = 0,296·I')

# Настройки графика
plt.xlabel('I, A', fontsize=12)
plt.ylabel('B, Тл', fontsize=12)
plt.title('Градуировочная кривая B = f(I)', fontsize=14)
plt.grid(True, linestyle='--', alpha=0.7)
plt.legend(fontsize=10)
plt.xlim(0, 3.2)
plt.ylim(0, 1.0)

# Показать график
plt.tight_layout()
plt.show()