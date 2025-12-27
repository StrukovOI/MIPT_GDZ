import numpy as np
import matplotlib.pyplot as plt
from scipy.interpolate import Akima1DInterpolator

# Данные петли гистерезиса
# H_hyst = np.array([-7621.359223, -2363.281872, -895.0421773, -375.9191469, -29.31720516,
#                    127.9961802, 188.158523, 252.1088652, 282.1900366, 343.4664969,
#                    414.2129556, 500, 500, 585.7870444, 656.5335031, 717.8099634,
#                    747.8354289, 811.39583, 871.5581728, 1028.648735, 1375.139265,
#                    1894.318001, 3361.610696, 8619.688047, 7621.359223, 2363.281872,
#                    895.0421773, 375.9191469, 29.31720516, -127.9961802, -188.158523,
#                    -252.1088652, -282.1900366, -343.4664969, -414.2129556, -500, -500,
#                    -585.7870444, -656.5335031, -717.8099634, -747.8354289, -811.39583,
#                    -871.5581728, -1028.648735, -1375.139265, -1894.318001, -3361.610696,
#                    -8619.688047])

# B_hyst = np.array([-0.994982757, -0.752726086, -0.514795427, -0.367711019, -0.259560719,
#                    -0.198996551, -0.168714468, -0.142758396, -0.121128336, -0.095172264,
#                    -0.06489018, 0, 0, 0.012978036, 0.025956072, 0.038934108, 0.047586132,
#                    0.06489018, 0.077868216, 0.138432384, 0.276864767, 0.445579235,
#                    0.713791978, 0.969026685, 0.977678709, 0.744074062, 0.506143403,
#                    0.354732983, 0.246582683, 0.203322563, 0.168714468, 0.142758396,
#                    0.116802324, 0.090846252, 0.056238156, 0, 0, -0.015573643, -0.025956072,
#                    -0.041529715, -0.062294573, -0.08305943, -0.098633073, -0.160927646,
#                    -0.29589922, -0.467209295, -0.737152443, -1.001904376])

H_hyst = np.array([-145.0, -141.936177, -139.4095177, -137.2210727, -136.1487347,
                   -133.8787204, -131.7300653, -126.119688, -113.7450263, -95.20292854,
                   -42.79961802, 144.9888588, 145.0485714, 141.9847484, 139.4580892,
                   137.2696442, 136.1953166, 133.9113758, 131.7627207, 126.1443855,
                   113.7657448, 95.22563652, 42.78850458, -144.9999723])

B_hyst = np.array([-1.85, -1.801981267, -1.753962534, -1.705943801, -1.673931312,
                   -1.609906335, -1.561887602, -1.337800181, -0.825600361, -0.201356832,
                   0.791030318, 1.735398735, 1.831426, 1.591332335, 1.479288624,
                   1.383251158, 1.303219936, 1.20718247, 1.09513876, 0.871051339,
                   0.47089523, -0.073317078, -0.953660518, -1.850010201])

# Данные начальной кривой намагничивания (обновленные)
# H_initial = np.array([0, 85.22998568, 156.5335031, 217.8099634, 247.8911348, 341.39583,
#                       401.5581728, 588.6487347, 875.6963234, 1394.87506, 2862.724813, 8119.688047])

# B_initial = np.array([0, 0.013843238, 0.04326012, 0.119397931, 0.157466836, 0.235335052,
#                       0.282055982, 0.337610674, 0.410469415, 0.514293702, 0.750995681, 0.973854421])

H_initial = np.array([0.0, 1.52196403, 2.795241127, 3.889463632, 4.426627407,
                      5.560639822, 6.634967372, 9.440155976, 15.63743435,
                      24.90848321, 51.12008595, 144.9944294])

B_initial = np.array([0.0, 0.019663691, 0.061449034, 0.169599334, 0.223674483,
                      0.334282744, 0.400647701, 0.550583344, 0.7250986,
                      0.902576282, 1.266755229, 1.837080318])

# Задаем абсолютные погрешности (можно изменить эти значения)
H_error_abs = 1.5  # Абсолютная погрешность H в А/м
B_error_abs = 0.05  # Абсолютная погрешность B в Тл

# Создаем массивы погрешностей
H_error_hyst = np.full_like(H_hyst, H_error_abs)
B_error_hyst = np.full_like(B_hyst, B_error_abs)
H_error_initial = np.full_like(H_initial, H_error_abs)
B_error_initial = np.full_like(B_initial, B_error_abs)

# Разделение данных петли гистерезиса на две ветви
H1, B1 = H_hyst[:12], B_hyst[:12]  # Первая половина данных (нисходящая ветвь)
H2, B2 = H_hyst[12:], B_hyst[12:]  # Вторая половина данных (восходящая ветвь)

# Удаление дубликатов
def remove_duplicates(H, B, H_err, B_err):
    unique_H, indices = np.unique(H, return_index=True)
    return unique_H, B[indices], H_err[indices], B_err[indices]

H1_clean, B1_clean, H1_err_clean, B1_err_clean = remove_duplicates(H1, B1, H_error_hyst[:12], B_error_hyst[:12])
H2_clean, B2_clean, H2_err_clean, B2_err_clean = remove_duplicates(H2, B2, H_error_hyst[12:], B_error_hyst[12:])

# Сортировка по H для каждой ветви
sort_idx1 = np.argsort(H1_clean)
H1_sorted, B1_sorted = H1_clean[sort_idx1], B1_clean[sort_idx1]
H1_err_sorted, B1_err_sorted = H1_err_clean[sort_idx1], B1_err_clean[sort_idx1]

sort_idx2 = np.argsort(H2_clean)
H2_sorted, B2_sorted = H2_clean[sort_idx2], B2_clean[sort_idx2]
H2_err_sorted, B2_err_sorted = H2_err_clean[sort_idx2], B2_err_clean[sort_idx2]

# Интерполяция с использованием Akima для петли гистерезиса
akima1 = Akima1DInterpolator(H1_sorted, B1_sorted)
akima2 = Akima1DInterpolator(H2_sorted, B2_sorted)

# Генерация плавных кривых для петли гистерезиса
H_smooth1 = np.linspace(H1_sorted.min(), H1_sorted.max(), 1000)
B_smooth1 = akima1(H_smooth1)

H_smooth2 = np.linspace(H2_sorted.min(), H2_sorted.max(), 1000)
B_smooth2 = akima2(H_smooth2)

# Интерполяция для начальной кривой намагничивания
akima_initial = Akima1DInterpolator(H_initial, B_initial)
H_smooth_initial = np.linspace(H_initial.min(), H_initial.max(), 1000)
B_smooth_initial = akima_initial(H_smooth_initial)

# Построение графика
plt.figure(figsize=(14, 10))

# Петля гистерезиса
plt.errorbar(H1_sorted, B1_sorted, xerr=H1_err_sorted, yerr=B1_err_sorted, 
             fmt='o', color='blue', ecolor='black', 
             elinewidth=1, capsize=3, alpha=0.7, markersize=4)
plt.errorbar(H2_sorted, B2_sorted, xerr=H2_err_sorted, yerr=B2_err_sorted, 
             fmt='o', color='red', ecolor='black', 
             elinewidth=1, capsize=3, alpha=0.7, markersize=4)
plt.plot(H_smooth1, B_smooth1, 'b-', linewidth=2, label='Восходящая ветвь')
plt.plot(H_smooth2, B_smooth2, 'r-', linewidth=2, label='Нисходящая ветвь')

# Начальная кривая намагничивания
plt.errorbar(H_initial, B_initial, xerr=H_error_initial, yerr=B_error_initial, 
             fmt='s', color='green', ecolor='black', 
             elinewidth=1, capsize=3, alpha=0.7, markersize=4)
plt.plot(H_smooth_initial, B_smooth_initial, 'g-', linewidth=2, label='Начальная кривая намагничивания')

plt.xlabel('H, А/м', fontsize=12)
plt.ylabel('B, Тл', fontsize=12)
# plt.title('Петля гистерезиса и начальная кривая намагничивания', fontsize=14)
plt.legend()
plt.grid(True, linestyle='--', alpha=0.7)
plt.tight_layout()
plt.show()

# Вывод информации о погрешностях
# print(f"Использованные погрешности:")
# print(f"  Для H: ±{H_error_abs} А/м")
# print(f"  Для B: ±{B_error_abs} Тл")