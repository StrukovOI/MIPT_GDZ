import numpy as np
import matplotlib.pyplot as plt
from scipy.interpolate import PchipInterpolator

# Данные для начальной кривой намагничивания
H = np.array([0, 85.22998568, 156.5335031, 217.8099634, 247.8911348,
              311.39583, 371.5581728, 528.6487347, 875.6963234,
              1394.87506, 2862.724813, 8119.688047])
dB = np.array([0, 0.034608096, 0.073542204, 0.190344527, 0.095172264,
               0.194670539, 0.116802324, 0.263886731, 0.307146851,
               0.259560719, 0.341754947, 0.307146851])

# Вычисляем абсолютные значения B
B = np.cumsum(dB)

# Задаем погрешности
H_err = 20  # Погрешность H, А/м
B_err = 0.05  # Погрешность B, Тл

# Создаем монотонную интерполяцию (PCHIP)
pchip = PchipInterpolator(H, B)
H_smooth = np.linspace(H.min(), H.max(), 500)
B_smooth = pchip(H_smooth)

# Для области за пределами данных используем постоянное значение (насыщение)
H_extended = np.linspace(H.max(), H.max() * 1.5, 100)
B_extended = np.full_like(H_extended, B[-1])

# Объединяем данные для полного графика
H_full = np.concatenate([H_smooth, H_extended])
B_full = np.concatenate([B_smooth, B_extended])

# Создаем график
plt.figure(figsize=(12, 8))

# Построение сглаженной кривой
plt.plot(H_full, B_full, color='royalblue', linewidth=2, 
         label='Сглаженная начальная кривая')

# Построение погрешностей для исходных точек
plt.errorbar(H, B, xerr=H_err, yerr=B_err, fmt='o', color='crimson', 
             capsize=5, capthick=1, elinewidth=2, markersize=6,
             label='Экспериментальные точки с погрешностями')

# Вертикальная линия, показывающая границу измерений
plt.axvline(x=H.max(), color='gray', linestyle='--', alpha=0.7, 
            label='Граница измерений')

# Настройка графика
plt.xlabel('H, А/м', fontsize=14)
plt.ylabel('B, Тл', fontsize=14)
plt.title('Начальная кривая намагничивания ферромагнетика', fontsize=16)
plt.legend(fontsize=12, loc='lower right')
plt.grid(True, linestyle='--', alpha=0.7)

# Добавляем подписи к критическим точкам
plt.annotate('B_s', xy=(H[-1], B[-1]), xytext=(10, 10), 
             textcoords='offset points', fontsize=14,
             arrowprops=dict(arrowstyle='->', color='black'))

# Устанавливаем диапазоны осей
plt.xlim(-100, H.max() * 1.6)
plt.ylim(-0.1, B.max() * 1.1)

# Показать график
plt.tight_layout()
plt.show()