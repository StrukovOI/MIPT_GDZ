import pandas as pd
import numpy as np
from scipy.interpolate import interp1d

# ========== НАСТРОЙКИ ==========
# Пути к файлам (замените на свои)
spectrum_file = "C:/Users/olezh/OneDrive/Рабочий стол/Лабы/Электроника/4 семестр/ЭОП/Спектры/ФС1.csv"
calibration_file = "C:/Users/olezh/OneDrive/Рабочий стол/Лабы/Электроника/4 семестр/ЭОП/Спектры/Калибровка.csv"

# Параметры формата (для обоих файлов одинаковые)
sep = ';'          # разделитель столбцов
decimal = ','      # десятичный разделитель
header = None      # заголовков нет

# Граница отсечки (все длины волн больше этого значения исключаются)
cutoff = 900  # нм
# =================================

def load_data(file_path):
    """Загружает CSV без заголовка, возвращает отсортированные x и y."""
    df = pd.read_csv(file_path, sep=sep, decimal=decimal, header=header)
    # Принудительное преобразование в числа (на случай, если pandas не справился)
    for col in df.columns:
        df[col] = pd.to_numeric(df[col].astype(str).str.replace(',', '.'), errors='coerce')
    df = df.dropna()                     # удаляем строки с NaN
    df = df.sort_values(by=df.columns[0]) # сортируем по первому столбцу (длина волны)
    return df.iloc[:, 0].values, df.iloc[:, 1].values

# Загрузка файлов
x_spec, y_spec = load_data(spectrum_file)
x_cal, y_cal = load_data(calibration_file)

# Интерполяция калибровочной кривой на длины волн спектра
cal_interp = interp1d(x_cal, y_cal, kind='linear',
                      fill_value='extrapolate', bounds_error=False)
y_cal_on_spec = cal_interp(x_spec)

# Коррекция спектра
y_corrected = y_spec * y_cal_on_spec

# Отсечка по длине волны
mask = x_spec <= cutoff
if np.sum(mask) < 2:
    print(f"Ошибка: после отсечки осталось менее 2 точек (интегрирование невозможно).")
else:
    x_integ = x_spec[mask]
    y_integ = y_corrected[mask]
    integral = np.trapz(y_integ, x_integ)
    print(f"Интеграл скорректированного спектра (λ ≤ {cutoff} нм) = {integral:.6f} (в условных единицах)")