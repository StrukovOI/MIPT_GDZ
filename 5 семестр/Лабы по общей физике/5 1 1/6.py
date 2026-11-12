import numpy as np
import matplotlib.pyplot as plt
from scipy.interpolate import make_interp_spline

# Настройка шрифтов для стиля отчета МФТИ
plt.rcParams['font.family'] = 'serif'
plt.rcParams['font.serif'] = ['Times New Roman', 'DejaVu Serif']
plt.rcParams['axes.unicode_minus'] = False

# Функция для перевода N в длину волны (Å)
def get_lambda(N):
    return 1.5734e-3 * N**2 - 5.8206 * N + 10653.67

# --- Данные для N = 2830 (λ ≈ 6782.6 Å) ---
N1, lam1 = 2830, get_lambda(2830)
V1 = np.array([7.45, 7.235, 7.097, 7.047, 6.882, 6.746, 6.393, 5.992, 5.5, 5.088, 
               4.52, 4.085, 3.642, 3.278, 2.895, 2.569, 1.998, 1.874, 1.756, 1.651, 
               1.55, 1.436, 1.368, 1.234, 1.144, 1.073, 0.973, 0.854, 0.761, 0.605, 
               0.467, 0.326, 0.007])
VI1 = np.array([0.517, 0.516, 0.514, 0.513, 0.512, 0.51, 0.506, 0.502, 0.495, 0.486, 
                0.476, 0.467, 0.453, 0.436, 0.408, 0.371, 0.284, 0.263, 0.244, 0.222, 
                0.205, 0.183, 0.167, 0.139, 0.124, 0.112, 0.096, 0.078, 0.065, 0.046, 
                0.032, 0.02, -0.004])

# --- Данные для N = 2460 (λ ≈ 5856.6 Å) ---
N2, lam2 = 2460, get_lambda(2460)
V2 = np.array([7.455, 7.245, 7.061, 6.588, 6.09, 5.498, 5.048, 4.632, 4.116, 3.561, 
               3.071, 2.546, 2.156, 2.026, 1.927, 1.823, 1.682, 1.563, 1.488, 1.395, 
               1.258, 1.132, 0.999, 0.674, 0.381, 0.007])
VI2 = np.array([0.475, 0.472, 0.47, 0.461, 0.45, 0.436, 0.423, 0.413, 0.387, 0.34, 
                0.294, 0.231, 0.182, 0.168, 0.158, 0.145, 0.129, 0.118, 0.106, 0.099, 
                0.084, 0.071, 0.059, 0.033, 0.014, -0.004])

# Сортируем данные по возрастанию V для корректной работы сплайна
idx1 = np.argsort(V1)
V1_s, VI1_s = V1[idx1], VI1[idx1]

idx2 = np.argsort(V2)
V2_s, VI2_s = V2[idx2], VI2[idx2]

# Создаем гладкие кривые с помощью кубической сплайн-интерполяции (k=3)
V1_smooth = np.linspace(V1_s.min(), V1_s.max(), 300)
spl1 = make_interp_spline(V1_s, VI1_s, k=3)
VI1_smooth = spl1(V1_smooth)

V2_smooth = np.linspace(V2_s.min(), V2_s.max(), 300)
spl2 = make_interp_spline(V2_s, VI2_s, k=3)
VI2_smooth = spl2(V2_smooth)

# Построение графика
plt.figure(figsize=(10, 6))

# Рисуем гладкие линии
plt.plot(V1_smooth, VI1_smooth, '-', color='blue', linewidth=2, label=f'N = {N1} (λ = {lam1:.1f} Å)')
plt.plot(V2_smooth, VI2_smooth, '-', color='red', linewidth=2, label=f'N = {N2} (λ = {lam2:.1f} Å)')

# Поверх линий рисуем исходные экспериментальные точки
plt.plot(V1, VI1, 'o', color='blue', markersize=5, fillstyle='none') # полые точки для наглядности
plt.plot(V2, VI2, 's', color='red', markersize=5, fillstyle='none')

# Оформление
plt.xlabel('Напряжение V, мВ', fontsize=12)
plt.ylabel('V(I), мВ (пропорционален фототоку)', fontsize=12)
# plt.title('Вольт-амперные характеристики фотоэлемента', fontsize=14, fontweight='bold')
plt.grid(True, which='major', linestyle='-', alpha=0.7)
plt.grid(True, which='minor', linestyle='--', alpha=0.4)
plt.legend(fontsize=11, loc='upper left')

# Настройка пределов осей для красивого отображения
plt.xlim(-0.5, 8.0)
plt.ylim(-0.05, 0.55)

plt.tight_layout()
plt.show()