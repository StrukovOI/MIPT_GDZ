import os
import glob
import numpy as np
import matplotlib.pyplot as plt

def read_iv_data(filename):
    """
    Читает файл с данными ВАХ.
    Возвращает два массива: Bias (напряжение) и Current (ток).
    Если данные не найдены, возвращает (None, None).
    """
    bias = []
    current = []
    
    with open(filename, 'r', encoding='utf-8') as f:
        lines = f.readlines()

    # Ищем строку, содержащую заголовок таблицы данных
    start_idx = None
    for i, line in enumerate(lines):
        if 'Bias' in line and 'Current' in line and 'Resistance' in line:
            start_idx = i + 1
            break

    if start_idx is None:
        print(f"Предупреждение: в файле {filename} не найден заголовок данных.")
        return None, None

    # Читаем все последующие строки до конца файла
    for line in lines[start_idx:]:
        parts = line.strip().split()
        if len(parts) == 3:  # ожидаем ровно три числа
            try:
                b = float(parts[0])
                c = float(parts[1])
                bias.append(b)
                current.append(c)
            except ValueError:
                # Строка содержит нечисловые данные – пропускаем
                continue
        # Строки другой длины (пустые и пр.) игнорируем

    return np.array(bias), np.array(current)


def main():
    # Шаблон для поиска файлов (можно изменить)
    file_pattern = r"C:\Users\olezh\OneDrive\Рабочий стол\Лабы\Электроника\4 семестр\Диод Шоттки\14969.data"  # все текстовые файлы в текущей папке
    files = glob.glob(file_pattern)

    if not files:
        print("Файлы не найдены. Проверьте шаблон или поместите файлы в текущую директорию.")
        return

    data = {}
    for f in files:
        bias, current = read_iv_data(f)
        if bias is not None:
            # Используем имя файла (без расширения) как метку
            label = os.path.splitext(os.path.basename(f))[0]
            data[label] = (bias, current)
            print(f"Загружено {len(bias)} точек из файла {f}")

    if not data:
        print("Не удалось загрузить данные ни из одного файла.")
        return

    # Построение графиков
    plt.figure(figsize=(10, 10))

    # Линейный график
    # plt.subplot(1, 2, 1)
    for label, (b, c) in data.items():
        plt.plot(b, c, label=label, linewidth=1)
    plt.xlabel('Напряжение (В)')
    plt.ylabel('Ток (А)')
    plt.title('ВАХ (линейный масштаб)')
    plt.grid(True)
    plt.legend()

    # График с симметричной логарифмической шкалой по току
    # plt.subplot(1, 2, 2)
    # for label, (b, c) in data.items():
    #     plt.plot(b, c, label=label, linewidth=1)
    # plt.xlabel('Напряжение (В)')
    # plt.ylabel('Ток (А)')
    # plt.title('ВАХ (symlog по оси Y)')
    # plt.yscale('symlog')  # удобно для данных, меняющих знак
    # plt.grid(True)
    # plt.legend()

    plt.tight_layout()
    plt.show()

    # При необходимости можно сохранить график в файл
    # plt.savefig('iv_curves.png', dpi=300)


if __name__ == "__main__":
    main()