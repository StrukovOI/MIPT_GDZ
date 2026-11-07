import os
import numpy as np
import matplotlib.pyplot as plt
from scipy import stats
from scipy.optimize import fsolve

# ==========================================
# 0. Принудительная смена рабочей папки
# ==========================================
target_dir = r"C:\Users\olezh\OneDrive\Рабочий стол\Лабы\Электроника\5 семестр\АЭП"
os.chdir(target_dir)
print(f"✅ Рабочая папка: {os.getcwd()}\n")

# ==========================================
# 1. Настройки и константы
# ==========================================
R_izm = 21700.0      # Измерительный резистор, Ом
phi = 4.7            # Работа выхода углерода, эВ
R_m = 1e-3           # Расстояние катод-анод, м (1 мм)
k_geom = 0.5         # Коэффициент формы (1/2 для параболического центра)

def fmt(val, decimals=2):
    """Форматирует число с запятой вместо точки (для LaTeX)"""
    return f"{val:.{decimals}f}".replace('.', ',')

def parse_tektronix(filepath):
    """Парсит CSV файл осциллографа Tektronix TDS2000 series"""
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
# 2. Поиск и группировка файлов
# ==========================================
all_files = os.listdir('.')
ch1_files = [f for f in all_files if 'CH1' in f.upper() and f.upper().endswith('.CSV')]
ch3_files = [f for f in all_files if 'CH3' in f.upper() and f.upper().endswith('.CSV')]

if not ch1_files or not ch3_files:
    print("❌ ОШИБКА: Файлы CH1 или CH3 не найдены!")
    print(f"CH1: {ch1_files}")
    print(f"CH3: {ch3_files}")
    exit()

def get_prefix(filename):
    name = filename.upper().replace('.CSV', '')
    return name.replace('CH1', '').replace('CH3', '')

measurements = {}
for f in ch1_files:
    prefix = get_prefix(f)
    measurements.setdefault(prefix, {})['CH1'] = f
for f in ch3_files:
    prefix = get_prefix(f)
    measurements.setdefault(prefix, {})['CH3'] = f

# ==========================================
# 3. Обработка данных и построение графиков переходных процессов
# ==========================================
results = []  # <-- ВАЖНО: инициализация ДО цикла
n_meas = len(measurements)

cols = 2 if n_meas > 1 else 1
rows = (n_meas + 1) // 2
plt.figure(figsize=(6 * cols, 5 * rows))

plot_idx = 1
for prefix, files in sorted(measurements.items()):
    if 'CH1' not in files or 'CH3' not in files:
        continue
        
    time, u_ch1 = parse_tektronix(files['CH1'])
    _, u_ch3 = parse_tektronix(files['CH3'])
    
    min_len = min(len(time), len(u_ch3))
    time = time[:min_len]
    u_ch1 = u_ch1[:min_len]
    u_ch3 = u_ch3[:min_len]
    
    i_ua = (u_ch3 / R_izm) * 1e6
    u_kv = u_ch1 / 1000.0
    
    steady_start = int(min_len * 0.8)
    u_steady_kv = np.mean(u_kv[steady_start:])
    i_steady_ua = np.mean(i_ua[steady_start:])
    
    results.append({
        'prefix': prefix,
        'U_kV': u_steady_kv,
        'I_uA': i_steady_ua
    })
    
    if plot_idx <= 4:
        plt.subplot(rows, cols, plot_idx)
        plt.plot(time, i_ua, color='blue', linewidth=1.5, label='Ток (мкА)')
        plt.xlabel("Время, с", fontsize=10)
        plt.ylabel("Ток, мкА", color='blue', fontsize=10)
        plt.grid(True, alpha=0.3)
        
        plt.twinx()
        plt.plot(time, u_kv, color='red', linewidth=1.5, linestyle='--', label='Напр. (кВ)')
        plt.ylabel("Напряжение, кВ", color='red', fontsize=10)
        plt.title(f"Измерение {prefix}", fontsize=11)
        plt.legend(loc='upper left', fontsize=9)
        plot_idx += 1

plt.tight_layout()
plt.savefig('transient_plots.png', dpi=300, bbox_inches='tight')
print("✅ График переходных процессов сохранён как 'transient_plots.png'")
plt.close()

if not results:
    print("❌ Не удалось извлечь данные из файлов. Проверьте формат CSV.")
    exit()

# ==========================================
# 4. Расчёт Фаулера-Нордгейма и радиуса r
# ==========================================
u_kv_arr = np.array([res['U_kV'] for res in results])
i_ua_arr = np.array([res['I_uA'] for res in results])

# Координаты ФН
x_fn = 1.0 / u_kv_arr
y_fn = np.log(i_ua_arr / (u_kv_arr**2))

# Масштабируем x для улучшения обусловленности
x_fn_scaled = x_fn * 1000.0

slope_scaled, intercept, r_value, p_value, std_err_scaled = stats.linregress(x_fn_scaled, y_fn)
slope = slope_scaled * 1000.0  # Возвращаем к исходному масштабу

# Расчёт форм-фактора beta (в 10^6 м^-1)
beta_table = -6.83 * (phi**1.5) / slope
beta_m = beta_table * 1e6

# Численное решение уравнения beta = 1 / (k * r * ln(R/r))
def equation_r(r_m):
    return beta_m - 1.0 / (k_geom * r_m * np.log(R_m / r_m))

r_m_solved = fsolve(equation_r, 50e-9)[0]
r_nm = r_m_solved * 1e9

# ==========================================
# 5. Вывод результатов
# ==========================================
print("\n" + "="*70)
print("РЕЗУЛЬТАТЫ РАСЧЁТА (готовы для вставки в отчёт)")
print("="*70)
print(f"Наклон прямой ФН (tan α):  {fmt(slope, 2)} кВ")
print(f"Коэффициент детерминации:  {fmt(r_value**2, 4)}")
print("-" * 70)
print(f"Форм-фактор β:             {fmt(beta_table, 2)} · 10⁶ м⁻¹")
print(f"Характерный радиус r:      {fmt(r_nm, 1)} нм")
print("="*70)

print("\nТАБЛИЦА УСТАНОВИВШИХСЯ ЗНАЧЕНИЙ ДЛЯ LATEX:")
print("\\begin{tabular}{|c|c|c|}")
print("\\hline")
print("Измерение & $U$, кВ & $I$, мкА \\\\")
print("\\hline")
for res in results:
    print(f"{res['prefix']} & {fmt(res['U_kV'], 3)} & {fmt(res['I_uA'], 2)} \\\\")
print("\\hline")
print("\\end{tabular}")

# ==========================================
# 6. График Фаулера-Нордгейма
# ==========================================
plt.figure(figsize=(8, 6))
plt.scatter(x_fn, y_fn, color='red', s=60, zorder=5, label='Экспериментальные точки')

x_fit = np.linspace(min(x_fn)*0.98, max(x_fn)*1.02, 100)
y_fit = slope * x_fit + intercept
plt.plot(x_fit, y_fit, color='blue', linewidth=2, 
         label=f'Аппроксимация\n$y = {fmt(slope, 2)}x + ({fmt(intercept, 2)})$')

# plt.title('Вольт-амперная характеристика в координатах Фаулера–Нордгейма', fontsize=12, fontweight='bold')
plt.xlabel(r'$1/U$, кВ$^{-1}$', fontsize=12)
plt.ylabel(r'$\ln(I/U^2)$', fontsize=12)
plt.grid(True, linestyle='--', alpha=0.7)
plt.legend(fontsize=11, loc='best')
plt.tight_layout()

plt.savefig('fn_plot.png', dpi=300, bbox_inches='tight')
plt.savefig('fn_plot.pdf', bbox_inches='tight')
print("\n✅ График Фаулера-Нордгейма сохранён как 'fn_plot.png' и 'fn_plot.pdf'")
plt.show()