import matplotlib.pyplot as plt
import pandas as pd

# Загрузка данных с правильным разделителем
data = pd.read_csv(
    r'C:\Users\olezh\OneDrive\Рабочий стол\Лабы\Электроника\Вакуум\data.csv',
    sep=';',           # разделитель столбцов: точка с запятой
    decimal=',',       # десятичный разделитель: запятая
    header=None,       # нет заголовков столбцов
    names=['time', 'pressure']  # задаем имена столбцов
)

# Используем столбцы с правильными именами
time = data['time']
pressure = data['pressure']

print("Первые 5 строк данных:")
print(data.head())
print(f"\nВсего точек: {len(data)}")
print(f"Диапазон времени: {time.min()} - {time.max()}")
print(f"Диапазон давления: {pressure.min()} - {pressure.max()}")

# Построение графика
plt.figure(figsize=(12, 5))
plt.plot(time, pressure, color = 'blue', linewidth=1)
# plt.title('Зависимость давления от времени')
plt.xlabel('Время, с')
plt.ylabel('Давление, Торр')
plt.grid(True)
plt.tight_layout()
plt.show()