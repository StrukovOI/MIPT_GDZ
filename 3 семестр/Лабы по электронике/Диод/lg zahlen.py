import numpy as np
import matplotlib.pyplot as plt
from scipy.stats import linregress

# Геометрические параметры диода
r_k = 0.075e-3  # радиус катода в метрах (0.15 мм / 2)
r_a = 5e-3      # радиус анода в метрах (10 мм / 2)
l = 0.045       # длина катода в метрах (45 мм)
f_ratio = 1.0   # функция отношения радиусов анода и катода

# Физические константы
epsilon_0 = 8.85e-12  # электрическая постоянная в Ф/м
e_m_theoretical = 1.76e11  # теоретическое значение удельного заряда в Кл/кг

# Токи накала и соответствующие напряжения накала
I_h_values = [2.4, 2.5, 2.6, 2.7, 2.8]
U_h_values = {2.4: 3.7, 2.5: 4.0, 2.6: 4.2, 2.7: 4.6, 2.8: 4.9}

# Данные ВАХ для каждого тока накала
V_a_data = {}
I_a_data = {}

# Данные для I_h = 2.4 А
V_a_data[2.4] = np.array([1, 2, 3, 4, 5, 10, 20, 30, 40, 50, 60, 70, 80, 90, 100, 110, 120, 130, 140])
I_a_data[2.4] = np.array([0.079, 0.108, 0.144, 0.151, 0.153, 0.162, 0.167, 0.171, 0.174, 
                          0.176, 0.178, 0.181, 0.182, 0.184, 0.186, 0.188, 0.189, 0.191, 0.192]) * 1e-6

# Данные для I_h = 2.5 А
V_a_data[2.5] = np.array([1, 2, 3, 4, 5, 10, 20, 30, 40, 50, 60, 70, 80, 90, 100, 110, 120, 130, 140])
I_a_data[2.5] = np.array([0.147, 0.188, 0.26, 0.367, 0.417, 0.478, 0.498, 0.51, 0.52,
                          0.53, 0.54, 0.547, 0.555, 0.562, 0.567, 0.572, 0.58, 0.584, 0.589]) * 1e-6

# Данные для I_h = 2.6 А
V_a_data[2.6] = np.array([1, 2, 3, 4, 5, 10, 20, 30, 40, 50, 60, 70, 80, 90, 100, 110, 120, 130, 140])
I_a_data[2.6] = np.array([0.16, 0.27, 0.34, 0.43, 0.59, 0.91, 0.96, 0.995, 1.02,
                          1.04, 1.053, 1.07, 1.08, 1.09, 1.1, 1.12, 1.136, 1.145, 1.155]) * 1e-6

# Данные для I_h = 2.7 А
V_a_data[2.7] = np.array([1, 2, 3, 4, 5, 10, 20, 30, 40, 50, 60, 70, 80, 90, 100, 110, 120, 130, 140])
I_a_data[2.7] = np.array([0.45, 0.505, 0.612, 0.601, 0.825, 1.67, 2.73, 2.85, 2.92,
                          3.05, 3.1, 3.17, 3.21, 3.24, 3.27, 3.3, 3.34, 3.37, 3.41]) * 1e-6

# Данные для I_h = 2.8 А
V_a_data[2.8] = np.array([1, 2, 3, 4, 5, 10, 20, 30, 40, 50, 60, 70, 80, 90, 100, 110, 120, 130, 140])
I_a_data[2.8] = np.array([0.65, 0.783, 0.98, 1.01, 1.25, 2.06, 5.04, 6.2, 6.54,
                          6.75, 6.9, 7.13, 7.28, 7.5, 7.7, 7.78, 7.85, 7.96, 8.05]) * 1e-6

# Создание фигуры с одним графиком
plt.figure(figsize=(10, 7))
plt.style.use('seaborn-v0_8-whitegrid')

# Цвета для разных токов накала
colors = ['#1f77b4', '#ff7f0e', '#2ca02c', '#d62728', '#9467bd']

# Словари для хранения результатов
experimental_g = {}
theoretical_g = {}
calculated_e_m = {}
efficiency = {}
slope_values = {}

# Количество точек для анализа начального участка (первые 12 точек)
n_points = 6

# График: ВАХ в логарифмических координатах
for idx, I_h in enumerate(I_h_values):
    log_V_a = np.log10(V_a_data[I_h])
    log_I_a = np.log10(I_a_data[I_h])
    plt.plot(log_V_a, log_I_a, 'o-', color=colors[idx], 
             markersize=4, linewidth=1.5, label=f'I_нак = {I_h} А')
    
    # Аппроксимация начального участка (первые n_points точек)
    slope, intercept, r_value, p_value, std_err = linregress(
        log_V_a[:n_points], log_I_a[:n_points]
    )
    slope_values[I_h] = slope
    
    # Расчет первеанса по первым n_points точкам
    g_values = I_a_data[I_h][:n_points] / (V_a_data[I_h][:n_points] ** 1.5)
    g_avg = np.mean(g_values)
    g_std = np.std(g_values)
    experimental_g[I_h] = g_avg
    
    # Теоретический расчет первеанса
    g_theoretical = (4 * np.pi * epsilon_0 / 9) * np.sqrt(2 * e_m_theoretical) * l * f_ratio
    theoretical_g[I_h] = g_theoretical
    
    # Расчет удельного заряда электрона
    e_m_calculated = ((9 * g_avg) / (4 * np.pi * epsilon_0 * l)) ** 2 * (2/3)
    calculated_e_m[I_h] = e_m_calculated
    
    # Расчет КПД (для режима насыщения) - используем последнюю точку
    V_a_sat = V_a_data[I_h][-1]
    I_a_sat = I_a_data[I_h][-1]
    U_h = U_h_values[I_h]
    
    # Мощность накала (приближенно)
    P_heating = I_h * U_h
    # Мощность анодной цепи в режиме насыщения
    P_anode_sat = I_a_sat * V_a_sat
    efficiency[I_h] = (P_anode_sat / P_heating) * 100 if P_heating > 0 else 0

plt.xlabel('lg(U_A)', fontsize=11)
plt.ylabel('lg(I_A)', fontsize=11)
plt.title('ВАХ термоэлектронного диода в логарифмических координатах', fontsize=12, fontweight='bold')
plt.grid(True, alpha=0.3)
plt.legend(fontsize=10)

plt.tight_layout()

# Вывод результатов
print("=" * 100)
print(f"{'Ток накала, А':<15} {'Угл. коэфф.':<15} {'Первеанс, А/В^1.5':<25} {'e/m, ×10¹¹ Кл/кг':<20} {'КПД, %':<10}")
print("-" * 100)
for I_h in I_h_values:
    print(f"{I_h:<15.1f} {slope_values[I_h]:<15.5f} {experimental_g[I_h]:<25.3e} {calculated_e_m[I_h]/1e11:<20.5f} {efficiency[I_h]:<10.5f}")

print("\n" + "=" * 100)
print("РЕЗУЛЬТАТЫ РАСЧЕТА ПО ПЕРВЫМ 12 ТОЧКАМ:")
print(f"Среднее значение e/m: {np.mean([calculated_e_m[I_h] for I_h in I_h_values])/1e11:.3f} ×10¹¹ Кл/кг")
print(f"Теоретическое значение e/m: {e_m_theoretical/1e11:.3f} ×10¹¹ Кл/кг")

# Рассчитаем относительную погрешность для каждого измерения
e_m_errors = []
for I_h in I_h_values:
    error = abs(calculated_e_m[I_h] - e_m_theoretical)/e_m_theoretical*100
    e_m_errors.append(error)

print(f"Средняя относительная погрешность: {np.mean(e_m_errors):.1f}%")
print(f"Максимальная погрешность: {max(e_m_errors):.1f}%")
print(f"Минимальная погрешность: {min(e_m_errors):.1f}%")

# Дополнительная информация о качестве аппроксимации
print(f"\nСреднее значение углового коэффициента (теоретическое = 1.5): {np.mean([slope_values[I_h] for I_h in I_h_values]):.3f}")
print(f"Отклонение от теоретического: {abs(np.mean([slope_values[I_h] for I_h in I_h_values]) - 1.5):.3f}")

# Сохранение графика
# plt.savefig('diode_characteristics_log_first12.png', dpi=300, bbox_inches='tight')
plt.show()