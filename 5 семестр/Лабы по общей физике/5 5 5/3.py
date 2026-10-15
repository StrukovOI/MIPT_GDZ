import numpy as np

# Калибровочные данные
E = np.array([0.511, 0.6617, 1.1732, 1.274, 1.3325])  # МэВ
N = np.array([747.769, 950.315, 1637.490, 1761.878, 1849.134])  # каналы
dN = np.array([58.799, 63.549, 85.430, 108.979, 93.856])  # погрешности N

# Линейная аппроксимация N = a*E + b
a, b = np.polyfit(E, N, 1)

# Расчет погрешностей коэффициентов
n = len(E)
N_pred = a * E + b
residuals = N - N_pred

# Стандартная ошибка регрессии
s = np.sqrt(np.sum(residuals**2) / (n - 2))

# Погрешность коэффициента a
Sxx = np.sum((E - np.mean(E))**2)
da = s / np.sqrt(Sxx)

# Погрешность коэффициента b
db = s * np.sqrt(np.sum(E**2) / (n * Sxx))

print("=== РЕЗУЛЬТАТЫ КАЛИБРОВКИ ===")
print(f"a = {a:.2f} ± {da:.2f} каналов/МэВ")
print(f"b = {b:.2f} ± {db:.2f} каналов")
print(f"\nОтносительные погрешности:")
print(f"Δa/a = {da/a*100:.2f}%")
print(f"Δb/b = {db/b*100:.2f}%")

# Проверка качества аппроксимации
r_squared = 1 - np.sum(residuals**2) / np.sum((N - np.mean(N))**2)
print(f"\nКоэффициент детерминации R² = {r_squared:.6f}")