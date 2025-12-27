import math
import cmath

def calculate_H1_over_H0(nu, sigma):
    """
    Вычисляет |H1/H0| для заданной частоты и проводимости
    """
    # Константы
    mu0 = 4 * math.pi * 1e-7  # Гн/м
    a = 0.0225  # м
    h = 0.0015  # м
    
    # Угловая частота
    omega = 2 * math.pi * nu
    
    # Комплексный параметр α
    alpha = cmath.sqrt(1j * omega * sigma * mu0)
    
    # Аргументы гиперболических функций
    z = alpha * h
    
    # Гиперболические функции комплексного аргумента
    ch_z = cmath.cosh(z)
    sh_z = cmath.sinh(z)
    
    # Знаменатель формулы
    denominator = ch_z + 0.5 * alpha * a * sh_z
    
    # Отношение H1/H0
    H1_over_H0 = 1.0 / denominator
    
    # Модуль отношения
    return abs(H1_over_H0)

# Значения проводимости (можно менять)
sigma_values = [
    4.44e7,  # σ_min
    5.6e7,   # σ_table
    6.78e7   # σ_max
]

# Список частот (можно менять)
frequencies = [
    20, 30, 40, 50, 60, 70, 80, 90, 100, 110,
    120, 140, 160, 100, 120, 140, 160, 180, 200,
    300, 400, 500, 600, 700, 800, 900, 1000,
    1300, 1600, 2000, 2600, 3300, 4300, 5500,
    7000, 9000, 11300, 14500, 18500, 23500, 30000
]

# Удаляем дубликаты частот и сортируем
frequencies = sorted(set(frequencies))

print("Частота (Гц)\t|H1/H0| (σ_min)\t|H1/H0| (σ_table)\t|H1/H0| (σ_max)")
print("-" * 80)

for nu in frequencies:
    results = []
    for sigma in sigma_values:
        result = calculate_H1_over_H0(nu, sigma)
        results.append(result)
    
    print(f"{nu}\t{results[0]:.6f}\t{results[1]:.6f}\t{results[2]:.6f}")

# Дополнительно: вывод в формате для Excel
print("\n" + "="*80)
print("Данные для копирования в Excel:")
print("Частота\tσ_min\tσ_table\tσ_max")
for nu in frequencies:
    results = []
    for sigma in sigma_values:
        result = calculate_H1_over_H0(nu, sigma)
        results.append(result)
    
    print(f"{nu}\t{results[0]}\t{results[1]}\t{results[2]}")