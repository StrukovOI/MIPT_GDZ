import matplotlib.pyplot as plt
import numpy as np
from scipy.interpolate import CubicSpline

# Данные
data = """
26,165	5,609
26,164	5,269
26,156	4,818
26,12	4,556
26,08	3,937
26,04	3,516
26,01	3,201
25,93	2,636
25,9	2,492
25,87	2,256
25,83	2,037
25,81	1,849
25,78	1,615
25,76	1,442
25,75	1,267
25,82	0,924
25,95	0,76
26,18	0,644
26,33	0,574
26,18	0,406
25,98	0,351
"""

# Преобразование данных в числа (замена запятых на точки)
lines = data.strip().split('\n')
U = [float(line.split()[0].replace(',', '.')) for line in lines]
I = [float(line.split()[1].replace(',', '.')) for line in lines]

# Параметрическая интерполяция - используем индекс точки как параметр
t = np.arange(len(U))  # параметр - порядковый номер точки

# Создаем кубические сплайны для U(t) и I(t)
cs_U = CubicSpline(t, U)
cs_I = CubicSpline(t, I)

# Генерация точек для плавной кривой
t_smooth = np.linspace(0, len(U)-1, 500)
U_smooth = cs_U(t_smooth)
I_smooth = cs_I(t_smooth)

# Погрешности
delta_U = 0.01  # В
delta_I = 0.005  # мА

# Построение графика
plt.figure(figsize=(10, 6))
plt.plot(U_smooth, I_smooth, 'b-', label='Сглаженная кривая', linewidth=2)
plt.errorbar(U, I, xerr=delta_U, yerr=delta_I, fmt='ro', markersize=6, 
             capsize=3, capthick=1, label='Экспериментальные точки')
plt.xlabel('U, В')
plt.ylabel('Ток I, мА')
plt.title('Вольт-амперная характеристика разряда')
# plt.legend()
plt.grid(True, linestyle='--', alpha=0.7)
plt.tight_layout()
plt.show()