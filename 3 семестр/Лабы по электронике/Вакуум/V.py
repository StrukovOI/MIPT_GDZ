import numpy as np
import matplotlib.pyplot as plt

def linear_regression_tab_comma():
    """
    Программа для определения коэффициентов линейной регрессии
    для данных с разделителем табуляция и десятичными запятыми
    """
    print("=" * 60)
    print("ПРОГРАММА ДЛЯ ОПРЕДЕЛЕНИЯ КОЭФФИЦИЕНТОВ ЛИНЕЙНОЙ РЕГРЕССИИ")
    print("Формат данных: x[TAB]y (десятичный разделитель - запятая)")
    print("Модель: y = A + B·x")
    print("=" * 60)
    
    # Ввод данных
    print("\nВВОД ДАННЫХ")
    print("Введите данные в формате: x[TAB]y")
    print("Пример: 108,61[TAB]-11,61828598")
    print("Для завершения ввода введите пустую строку")
    print("-" * 40)
    
    x_data = []
    y_data = []
    
    while True:
        try:
            line = input().strip()
            if not line:
                break
                
            # Заменяем запятые на точки и разделяем по табуляции или пробелам
            line_clean = line.replace(',', '.')
            parts = line_clean.split()
            
            if len(parts) >= 2:
                x = float(parts[0])
                y = float(parts[1])
                x_data.append(x)
                y_data.append(y)
                print(f"Добавлена точка: x={x}, y={y}")
            else:
                print("Ошибка: введите два числа через табуляцию или пробел")
                
        except ValueError as e:
            print(f"Ошибка преобразования: {e}")
            print("Проверьте формат данных")
        except KeyboardInterrupt:
            print("\nВвод прерван")
            break
    
    if len(x_data) < 2:
        print("Недостаточно данных для расчёта (нужно минимум 2 точки)")
        return
    
    # Преобразуем в numpy массивы
    x = np.array(x_data)
    y = np.array(y_data)
    
    print(f"\nВВЕДЕНЫ ДАННЫЕ:")
    print(f"Количество точек: {len(x)}")
    print(f"x: от {x.min():.4f} до {x.max():.4f}")
    print(f"y: от {y.min():.4f} до {y.max():.4f}")
    
    # Расчёт коэффициентов методом наименьших квадратов
    print("\n" + "=" * 60)
    print("РАСЧЁТ КОЭФФИЦИЕНТОВ")
    print("=" * 60)
    
    # Суммы для расчёта
    n = len(x)
    S_x = np.sum(x)
    S_y = np.sum(y)
    S_xx = np.sum(x**2)
    S_xy = np.sum(x * y)
    S_yy = np.sum(y**2)
    
    print(f"n = {n}")
    print(f"Σx = {S_x:.6f}")
    print(f"Σy = {S_y:.6f}")
    print(f"Σx² = {S_xx:.6f}")
    print(f"Σxy = {S_xy:.6f}")
    
    # Коэффициенты прямой y = A + Bx
    denominator = n * S_xx - S_x**2
    B = (n * S_xy - S_x * S_y) / denominator
    A = (S_y - B * S_x) / n
    
    print(f"\nЗНАЧЕНИЯ КОЭФФИЦИЕНТОВ:")
    print(f"B (наклон) = {B:.8f}")
    print(f"A (intercept) = {A:.8f}")
    print(f"Уравнение: y = {A:.6f} + {B:.6f}·x")
    
    # Статистика качества аппроксимации
    print("\n" + "-" * 40)
    print("СТАТИСТИКА КАЧЕСТВА АППРОКСИМАЦИИ")
    print("-" * 40)
    
    # Предсказанные значения
    y_pred = A + B * x
    
    # Остатки
    residuals = y - y_pred
    
    # Коэффициент детерминации R²
    y_mean = np.mean(y)
    SS_tot = np.sum((y - y_mean)**2)
    SS_res = np.sum(residuals**2)
    R_squared = 1 - SS_res / SS_tot
    
    # Стандартная ошибка
    std_error = np.sqrt(SS_res / (n - 2))
    
    print(f"Коэффициент детерминации R² = {R_squared:.6f}")
    print(f"Стандартная ошибка оценки = {std_error:.6f}")
    
    # Построение графиков
    print("\n" + "=" * 60)
    print("ПОСТРОЕНИЕ ГРАФИКОВ")
    print("=" * 60)
    
    plt.figure(figsize=(12, 5))
    
    # График 1: Данные и линия регрессии
    plt.subplot(1, 2, 1)
    plt.plot(x, y, 'bo', markersize=4, label='Экспериментальные данные')
    
    # Линия регрессии
    x_fit = np.linspace(min(x), max(x), 100)
    y_fit = A + B * x_fit
    plt.plot(x_fit, y_fit, 'r-', linewidth=2, 
             label=f'y = {A:.4f} + {B:.4f}·x\nR² = {R_squared:.4f}')
    
    plt.xlabel('x')
    plt.ylabel('y')
    plt.title('Линейная регрессия')
    plt.legend()
    plt.grid(True, alpha=0.3)
    
    # График 2: Остатки
    plt.subplot(1, 2, 2)
    plt.plot(x, residuals, 'ro', markersize=4)
    plt.axhline(y=0, color='k', linestyle='-', alpha=0.3)
    plt.xlabel('x')
    plt.ylabel('Остатки (y - y_pred)')
    plt.title('График остатков')
    plt.grid(True, alpha=0.3)
    
    plt.tight_layout()
    plt.show()
    
    # Вывод результатов в формате для LaTeX
    print("\n" + "=" * 60)
    print("РЕЗУЛЬТАТЫ ДЛЯ LaTeX")
    print("=" * 60)
    
    print(f"""
\\subsection*{{Результаты линейной регрессии}}

Уравнение регрессии:
\\[
y = {A:.6f} + {B:.6f} \\cdot x
\\]

Статистические показатели:
\\begin{{itemize}}
    \\item Коэффициент детерминации: $R^2 = {R_squared:.6f}$
    \\item Стандартная ошибка оценки: $\\sigma = {std_error:.6f}$
    \\item Количество точек: $n = {n}$
\\end{{itemize}}

\\textbf{{Коэффициент наклона:}} $B = {B:.8f}$
""")
    
    return A, B, R_squared

def quick_slope_tab_comma():
    """
    Упрощённая версия только для расчёта наклона
    для данных с табуляцией и десятичными запятыми
    """
    print("\nБЫСТРЫЙ РАСЧЁТ НАКЛОНА")
    print("Введите данные в формате: x[TAB]y")
    print("(десятичный разделитель - запятая)")
    print("Пустая строка - конец ввода:")
    print("-" * 40)
    
    x_data = []
    y_data = []
    
    while True:
        line = input().strip()
        if not line:
            break
        try:
            # Заменяем запятые на точки и разделяем
            line_clean = line.replace(',', '.')
            parts = line_clean.split()
            if len(parts) >= 2:
                x = float(parts[0])
                y = float(parts[1])
                x_data.append(x)
                y_data.append(y)
            else:
                print("Пропущена строка (неверный формат)")
        except:
            print("Пропущена строка (ошибка преобразования)")
    
    if len(x_data) < 2:
        print("Недостаточно данных")
        return
    
    x = np.array(x_data)
    y = np.array(y_data)
    
    # Простой расчёт наклона
    n = len(x)
    B = (n * np.sum(x*y) - np.sum(x) * np.sum(y)) / (n * np.sum(x**2) - np.sum(x)**2)
    A = (np.sum(y) - B * np.sum(x)) / n
    
    # R²
    y_pred = A + B * x
    R_squared = 1 - np.sum((y - y_pred)**2) / np.sum((y - np.mean(y))**2)
    
    print(f"\nРЕЗУЛЬТАТ:")
    print(f"Наклон B = {B:.8f}")
    print(f"Intercept A = {A:.8f}")
    print(f"Уравнение: y = {A:.6f} + {B:.6f}·x")
    print(f"R² = {R_squared:.6f}")
    
    return A, B, R_squared

# Основная программа
if __name__ == "__main__":
    print("Выберите режим:")
    print("1 - Полный анализ с графиками")
    print("2 - Только расчёт коэффициентов")
    
    choice = input("Ваш выбор [1]: ").strip()
    
    if choice == "2":
        A, B, R2 = quick_slope_tab_comma()
    else:
        A, B, R2 = linear_regression_tab_comma()
    
    if A is not None:
        print(f"\n" + "="*60)
        print(f"ИТОГОВЫЙ КОЭФФИЦИЕНТ НАКЛОНА: B = {B:.8f}")
        print("="*60)