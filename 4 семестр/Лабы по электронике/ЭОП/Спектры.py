import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
from scipy.interpolate import CubicSpline, interp1d

# ========== НАСТРОЙКИ ==========
# Пути к файлам (замените на свои)
file_spectrum = "C:/Users/olezh/OneDrive/Рабочий стол/Лабы/Электроника/4 семестр/ЭОП/Спектры/ФС1.csv"
file_calibration = "C:/Users/olezh/OneDrive/Рабочий стол/Лабы/Электроника/4 семестр/ЭОП/Спектры/Калибровка.csv"

# Параметры для обоих файлов (одинаковые)
sep = ';'          # разделитель столбцов
decimal = ','      # десятичный разделитель
header = None      # нет строки заголовка
# =================================

def load_csv(file_path, sep, decimal, header):
    """
    Загружает CSV-файл без заголовка, с заданными разделителями.
    Возвращает отсортированные по первому столбцу массивы x и y.
    """
    try:
        # Читаем без заголовка, имена столбцов зададим позже
        df = pd.read_csv(file_path, sep=sep, decimal=decimal, header=header)
    except Exception as e:
        print(f"Ошибка загрузки {file_path}: {e}")
        return None, None

    # Если файл пустой или что-то не так
    if df.empty:
        print(f"Файл {file_path} пуст.")
        return None, None

    # Принудительно преобразуем столбцы в числа (заменяем запятые на точки, если нужно)
    # Но pandas с параметром decimal уже должен сделать это корректно.
    # Однако на всякий случай:
    for col in df.columns:
        df[col] = pd.to_numeric(df[col].astype(str).str.replace(',', '.'), errors='coerce')

    # Удаляем строки с NaN
    df = df.dropna()

    if df.empty:
        print(f"В файле {file_path} нет числовых данных.")
        return None, None

    # Сортируем по первому столбцу (длина волны)
    df = df.sort_values(by=df.columns[0])

    x = df.iloc[:, 0].values
    y = df.iloc[:, 1].values

    return x, y

# Загружаем спектр
x_spec, y_spec = load_csv(file_spectrum, sep, decimal, header)
# Загружаем калибровку
x_cal, y_cal = load_csv(file_calibration, sep, decimal, header)

if x_spec is None or x_cal is None:
    print("Не удалось загрузить один из файлов. Программа завершена.")
    exit()

print(f"Спектр: {len(x_spec)} точек, диапазон {x_spec.min():.2f} - {x_spec.max():.2f} нм")
print(f"Калибровка: {len(x_cal)} точек, диапазон {x_cal.min():.2f} - {x_cal.max():.2f} нм")

# Интерполируем калибровочную кривую на длины волн спектра
# (используем линейную интерполяцию, экстраполяцию за границы разрешим)
cal_interp = interp1d(x_cal, y_cal, kind='linear',
                      fill_value='extrapolate', bounds_error=False)
y_cal_on_spec = cal_interp(x_spec)

# Корректируем спектр (умножаем интенсивность на коэффициент)
y_corrected = y_spec * y_cal_on_spec

# Построение графиков
plt.figure(figsize=(12, 6))

# Исходный спектр (гладкая кривая)
# cs_spec = CubicSpline(x_spec, y_spec)
x_smooth = np.linspace(x_spec.min(), x_spec.max(), 1000)
# y_smooth_spec = cs_spec(x_smooth)
# plt.plot(x_smooth, y_smooth_spec, 'b-', linewidth=1.5, label='Исходный спектр')

# Скорректированный спектр (гладкая кривая)
cs_corr = CubicSpline(x_spec, y_corrected)
y_smooth_corr = cs_corr(x_smooth)
plt.plot(x_smooth, y_smooth_corr, 'b-', linewidth=1.5)

plt.xlabel(r"$\lambda$, нм", fontsize=12)
plt.ylabel("Интенсивность", fontsize=12)
plt.grid(True, linestyle=':', alpha=0.5)
# plt.legend()
plt.tight_layout()
plt.show()