import numpy as np
import matplotlib.pyplot as plt
from scipy import stats

# ==========================================
# 1. Парсинг CSV файлов (тот же, что раньше)
# ==========================================
def parse_tektronix(filepath):
    time_data, volt_data = [], []
    with open(filepath, 'r', encoding='utf-8', errors='ignore') as f:
        for line in f:
            if line.startswith(','):
                parts = line.strip().split(',')
                try:
                    t = float(parts[3].strip().replace(',', '.'))
                    v = float(parts[4].strip().replace(',', '.'))
                    time_data.append(t)
                    volt_data.append(v)
                except (ValueError, IndexError):
                    continue
    return np.array(time_data), np.array(volt_data)

# ==========================================
# 2. Загрузка данных для всех 4 катодов
# ==========================================
import os
target_dir = r"C:\Users\olezh\OneDrive\Рабочий стол\Лабы\Электроника\5 семестр\АЭП"
os.chdir(target_dir)

R_izm = 21700.0  # Ом

cathodes = ['F0001', 'F0002', 'F0003', 'F0004']
data = {}

for cath in cathodes:
    ch1_file = f"{cath}CH1.CSV"
    ch3_file = f"{cath}CH3.CSV"
    
    if os.path.exists(ch1_file) and os.path.exists(ch3_file):
        time, u_ch1 = parse_tektronix(ch1_file)
        _, u_ch3 = parse_tektronix(ch3_file)
        
        min_len = min(len(time), len(u_ch3))
        time = time[:min_len]
        u_ch1 = u_ch1[:min_len]
        u_ch3 = u_ch3[:min_len]
        
        # Ток в мкА, напряжение в кВ
        i_ua = (u_ch3 / R_izm) * 1e6
        u_kv = u_ch1 / 1000.0
        
        data[cath] = {'time': time, 'U_kV': u_kv, 'I_uA': i_ua}
        print(f"✅ Загружен {cath}: {min_len} точек")

# ==========================================
# 3. Построение графиков Ф-Н для каждого катода
# ==========================================
fig, axes = plt.subplots(2, 2, figsize=(14, 10))
axes = axes.flatten()

for idx, cath in enumerate(cathodes):
    if cath not in data:
        continue
    
    U_kV = data[cath]['U_kV']
    I_uA = data[cath]['I_uA']
    
    # Берём только точки, где U > 0.5 кВ и I > 1 мкА (чтобы избежать шума и деления на ноль)
    mask = (U_kV > 0.5) & (I_uA > 1.0)
    U_filt = U_kV[mask]
    I_filt = I_uA[mask]
    
    # Координаты Ф-Н: x = 1/U (кВ^-1), y = ln(I/U²)
    # I в мкА, U в кВ -> ln(I_мкА / U_кВ²)
    x_FN = 1.0 / U_filt
    y_FN = np.log(I_filt / (U_filt**2))
    
    # Линейная регрессия
    slope, intercept, r_value, p_value, std_err = stats.linregress(x_FN, y_FN)
    
    ax = axes[idx]
    ax.scatter(x_FN, y_FN, s=10, alpha=0.3, color='blue', label='Точки переходного процесса')
    
    # Линия аппроксимации
    x_fit = np.linspace(x_FN.min(), x_FN.max(), 100)
    y_fit = slope * x_fit + intercept
    ax.plot(x_fit, y_fit, 'r-', linewidth=2, label=f'Линейная аппроксимация')
    
    ax.set_xlabel(r'$1/U$, кВ$^{-1}$', fontsize=11)
    ax.set_ylabel(r'$\ln(I/U^2)$', fontsize=11)
    ax.set_title(f'Катод {cath} в координатах Фаулера–Нордгейма', fontsize=12, fontweight='bold')
    ax.legend(fontsize=9)
    ax.grid(True, alpha=0.3)

plt.tight_layout()
plt.savefig('transient_FN.png', dpi=300, bbox_inches='tight')
plt.savefig('transient_FN.pdf', bbox_inches='tight')
print("\n✅ Графики Ф-Н из переходных процессов сохранены как 'transient_FN.png/pdf'")
plt.show()

# ==========================================
# 4. Вывод результатов для каждого катода
# ==========================================
print("\n" + "="*70)
print("РЕЗУЛЬТАТЫ АППРОКСИМАЦИИ Ф-Н ДЛЯ КАЖДОГО КАТОДА")
print("="*70)

phi = 4.7  # эВ

for cath in cathodes:
    if cath not in data:
        continue
    
    U_kV = data[cath]['U_kV']
    I_uA = data[cath]['I_uA']
    
    mask = (U_kV > 0.5) & (I_uA > 1.0)
    U_filt = U_kV[mask]
    I_filt = I_uA[mask]
    
    x_FN = 1.0 / U_filt
    y_FN = np.log(I_filt / (U_filt**2))
    
    slope, intercept, r_value, p_value, std_err = stats.linregress(x_FN, y_FN)
    
    # Форм-фактор: beta = -6.83 * phi^(3/2) / slope (slope в кВ)
    beta = -6.83 * (phi**1.5) / slope
    
    print(f"\n{cath}:")
    print(f"  Наклон: {slope:.2f} кВ")
    print(f"  R²: {r_value**2:.4f}")
    print(f"  β = {beta:.2f} · 10⁶ м⁻¹")