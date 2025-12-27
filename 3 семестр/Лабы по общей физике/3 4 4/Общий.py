import numpy as np
import matplotlib.pyplot as plt

# === 1. Данные для восходящей ветви (уменьшение H) ===
# Данные упорядочены от H=0 до H=max (обратный порядок исходных данных)
H_asc = np.array([0, 85.78704441, 156.5335031, 217.8099634, 247.8911348,
                  311.841477, 372.0038198, 529.3172052, 875.9191469,
                  1395.042177, 2863.281872, 8121.359223])

dB_asc = np.array([0.06489018, 0.030282084, 0.025956072, 0.02163006, 0.025956072,
                   0.030282084, 0.060564168, 0.1081503, 0.147084408, 0.237930659, 0.242256671, 0])

B_asc = np.cumsum(dB_asc)  # Абсолютные значения B для восходящей ветви
B_sat = B_asc[-1]  # Насыщение ≈ 0.995 Тл

# === 2. Данные для нисходящей ветви (возрастание H) ===
H_desc = np.array([0, 85.78704441, 156.5335031, 217.8099634, 247.8354289,
                   311.39583, 371.5581728, 528.6487347, 875.1392647,
                   1394.318001, 2861.610696, 8119.688047])

dB_desc = np.array([0, -0.012978036, -0.012978036, -0.012978036, -0.008652024,
                    -0.017304048, -0.012978036, -0.060564168, -0.138432384,
                    -0.168714468, -0.268212743, -0.255234707])

# Ключевой момент: нисходящая ветвь начинается с уровня насыщения
B_desc = np.cumsum(dB_desc) + B_sat

# === 3. Начальная кривая намагничивания ===
H_initial = np.array([0.000, 85.230, 156.534, 217.810, 247.891, 311.396, 
                      371.558, 528.649, 875.696, 1394.875, 2862.725, 8119.688])

dB_initial = np.array([0.0000, 0.017304048, 0.036771102, 0.095172264, 0.047586132, 0.09733527, 
                      0.058401162, 0.131943366, 0.153573426, 0.12978036, 0.170877474, 0.153573426])

# Для начальной кривой ΔB - это приращения (суммируем)
B_initial = np.cumsum(dB_initial)

# === 4. Построение графика ===
plt.figure(figsize=(12, 8))

# === Ключевые изменения: раздельная раскраска ветвей петли ===
# Восходящая ветвь (возрастающая) - СИНИЙ цвет
plt.plot(H_asc, B_asc, 'b-', linewidth=2.5, label='Восходящая ветвь (возрастающая)')
plt.scatter(H_asc, B_asc, c='blue', s=40, zorder=5, edgecolor='black')

# Нисходящая ветвь - ЗЕЛЁНЫЙ цвет
plt.plot(-H_desc[1:], B_desc[1:], 'g-', linewidth=2.5, label='Нисходящая ветвь')
plt.scatter(-H_desc, B_desc, c='green', s=40, zorder=5, edgecolor='black')

# Начальная кривая - КРАСНЫЙ цвет (без изменений)
plt.plot(H_initial, B_initial, 'r-', linewidth=2.5, label='Начальная кривая')
plt.scatter(H_initial, B_initial, c='red', s=40, zorder=5, edgecolor='black')

# Оси и оформление
plt.axhline(0, color='k', linewidth=1.0, alpha=0.7)  # Ось H по центру
plt.axvline(0, color='gray', linestyle='--', alpha=0.3)

# Настройка пределов
max_H = max(np.max(H_asc), np.max(H_desc)) * 1.1
max_B = max(np.max(B_asc), np.max(B_desc), np.max(B_initial)) * 1.1
plt.xlim(-max_H, max_H)
plt.ylim(-max_B * 0.1, max_B * 1.05)

# Подписи и заголовок
plt.xlabel('Напряженность магнитного поля $H$, А/м', fontsize=12)
plt.ylabel('Магнитная индукция $B$, Тл', fontsize=12)
plt.title('Кривая гистерезиса и начальная кривая намагничивания', fontsize=14)
plt.legend(loc='lower right', fontsize=11)
plt.grid(linestyle='--', alpha=0.6)

# Отметка насыщения
plt.axhline(B_sat, color='purple', linestyle=':', alpha=0.7)
plt.annotate(f'Насыщение $B_s$ = {B_sat:.3f} Тл', 
             xy=(max_H*0.7, B_sat*0.95),
             color='purple', fontsize=10)

# Стрелки направления для наглядности
plt.annotate('', xy=(6000, 0.5), xytext=(7000, 0.5),
             arrowprops=dict(arrowstyle='->', color='blue', lw=1.5))
plt.annotate('', xy=(-6000, 0.5), xytext=(-7000, 0.5),
             arrowprops=dict(arrowstyle='->', color='green', lw=1.5))

# Коэрцитивная сила
Hc_index = np.argmin(np.abs(B_desc))
Hc = H_desc[Hc_index]
plt.scatter([-Hc], [0], s=120, color='darkgreen', zorder=10, edgecolor='black')
plt.text(-Hc-500, 0.05, f'$H_c$ = {-Hc:.1f} А/м', fontsize=12, color='darkgreen')

plt.tight_layout()
plt.show()