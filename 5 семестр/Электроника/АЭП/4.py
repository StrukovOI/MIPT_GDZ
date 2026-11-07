import os
import numpy as np
import matplotlib.pyplot as plt

# ==========================================
# 0. Принудительная смена рабочей папки
# ==========================================
target_dir = r"C:\Users\olezh\OneDrive\Рабочий стол\Лабы\Электроника\5 семестр\АЭП"
os.chdir(target_dir)
print(f"✅ Рабочая папка: {os.getcwd()}\n")

# ==========================================
# 1. Настройки и константы
# ==========================================
R_izm = 21700.0  # Измерительный резистор, Ом

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

print(f"📊 Найдено пар измерений: {len(measurements)}")

# ==========================================
# 3. Построение 4 графиков на одном изображении
# ==========================================
fig, axes = plt.subplots(2, 2, figsize=(14, 10))
axes = axes.flatten()  # Преобразуем 2D массив в 1D для удобства

plot_idx = 0
for prefix, files in sorted(measurements.items()):
    if 'CH1' not in files or 'CH3' not in files:
        continue
    if plot_idx >= 4:  # Максимум 4 графика
        break
        
    time, u_ch1 = parse_tektronix(files['CH1'])
    _, u_ch3 = parse_tektronix(files['CH3'])
    
    min_len = min(len(time), len(u_ch3))
    time = time[:min_len]
    u_ch1 = u_ch1[:min_len]
    u_ch3 = u_ch3[:min_len]
    
    # Расчёт тока в мкА и напряжения в кВ
    i_ua = (u_ch3 / R_izm) * 1e6
    u_kv = u_ch1 / 1000.0
    
    ax = axes[plot_idx]
    
    # График тока (синяя линия, левая ось Y)
    ax.plot(time, i_ua, color='blue', linewidth=1.5, label='Ток, мкА')
    ax.set_xlabel('Время, с', fontsize=10)
    ax.set_ylabel('Ток, мкА', color='blue', fontsize=10)
    ax.tick_params(axis='y', labelcolor='blue')
    ax.grid(True, alpha=0.3)
    ax.set_title(f'Катод {prefix}', fontsize=12, fontweight='bold')
    
    # График напряжения (красная пунктирная линия, правая ось Y)
    ax2 = ax.twinx()
    ax2.plot(time, u_kv, color='red', linewidth=1.5, linestyle='--', label='Напряжение, кВ')
    ax2.set_ylabel('Напряжение, кВ', color='red', fontsize=10)
    ax2.tick_params(axis='y', labelcolor='red')
    
    # Легенда
    lines1, labels1 = ax.get_legend_handles_labels()
    lines2, labels2 = ax2.get_legend_handles_labels()
    ax.legend(lines1 + lines2, labels1 + labels2, loc='upper left', fontsize=9)
    
    plot_idx += 1

# Если графиков меньше 4, скрываем пустые субплоты
for idx in range(plot_idx, 4):
    axes[idx].axis('off')

plt.tight_layout()
plt.savefig('transient_plots.png', dpi=300, bbox_inches='tight')
print("✅ График сохранён как 'transient_plots.png'")
plt.show()