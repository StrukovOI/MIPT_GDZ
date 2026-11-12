import numpy as np
import matplotlib.pyplot as plt
from matplotlib.widgets import Slider

# Настройка шрифтов
plt.rcParams['font.family'] = 'serif'
plt.rcParams['font.serif'] = ['Times New Roman', 'DejaVu Serif']
plt.rcParams['axes.unicode_minus'] = False

def get_lambda(N):
    return 1.5734e-3 * N**2 - 5.8206 * N + 10653.67

c = 2.99792458e18  # скорость света, Å/с
e = 1.602176634e-19 # элементарный заряд, Кл

# Все 5 наборов данных (как вы предоставили)
data = {
    2200: {
        'V': [2.329, 2.111, 1.965, 1.854, 1.744, 1.647, 1.552, 1.405, 1.248, 1.108, 0.966, 0.807, 0.621, 0.435],
        'I': [0.129, 0.11, 0.1, 0.092, 0.084, 0.078, 0.072, 0.061, 0.052, 0.044, 0.038, 0.03, 0.021, 0.013]
    },
    2300: {
        'V': [2.373, 2.127, 1.973, 1.851, 1.75, 1.648, 1.526, 1.404, 1.251, 1.104, 0.959, 0.802, 0.62, 0.416],
        'I': [0.166, 0.139, 0.126, 0.113, 0.104, 0.095, 0.086, 0.075, 0.064, 0.055, 0.046, 0.036, 0.026, 0.017]
    },
    2460: {
        'V': [2.156, 2.026, 1.927, 1.823, 1.682, 1.563, 1.488, 1.395, 1.258, 1.132, 0.999, 0.674],
        'I': [0.188, 0.174, 0.164, 0.151, 0.135, 0.124, 0.113, 0.105, 0.09, 0.077, 0.065, 0.039]
    },
    2550: {
        'V': [2.374, 2.128, 1.972, 1.855, 1.743, 1.608, 1.409, 1.207, 1.014, 0.811, 0.604, 0.407],
        'I': [0.269, 0.23, 0.205, 0.189, 0.171, 0.151, 0.122, 0.097, 0.075, 0.055, 0.037, 0.022]
    },
    2830: {
        'V': [1.998, 1.874, 1.756, 1.651, 1.55, 1.436, 1.368, 1.234, 1.144, 1.073, 0.973, 0.854, 0.761, 0.605, 0.467, 0.326],
        'I': [0.284, 0.263, 0.244, 0.222, 0.205, 0.183, 0.167, 0.139, 0.124, 0.112, 0.096, 0.078, 0.065, 0.046, 0.032, 0.02]
    }
}

# Создаем фигуру и оставляем место снизу для слайдеров
fig, ax = plt.subplots(figsize=(10, 8))
plt.subplots_adjust(bottom=0.35)

colors = {2200: 'blue', 2300: 'green', 2460: 'orange', 2550: 'red', 2830: 'purple'}
lines = {}
fit_lines = {}
sliders_I = {}
sliders_V = {}
n_fit = 4 # Количество точек для линейной аппроксимации (наименьшие токи)

# Начальная отрисовка
for N, vals in data.items():
    V = np.array(vals['V'])
    I = np.array(vals['I'])
    
    # Сортируем по V для корректной работы
    sort_idx = np.argsort(V)
    V = V[sort_idx]
    I = I[sort_idx]
    
    # Рисуем точки (пока без сдвигов)
    line, = ax.plot(V, np.sqrt(np.maximum(I, 0)), 'o', color=colors[N], label=f'N={N}', markersize=4)
    lines[N] = line
    
    # Линия аппроксимации
    fit_line, = ax.plot([], [], '--', color=colors[N], alpha=0.7)
    fit_lines[N] = fit_line

ax.set_xlabel('Напряжение $V$, В', fontsize=12)
ax.set_ylabel('$\sqrt{V(I)}$, $\sqrt{\text{мВ}}$', fontsize=12)
ax.set_title('Интерактивная настройка зависимостей $\sqrt{I}=f(V)$', fontsize=13, fontweight='bold')
ax.grid(True, linestyle='--', alpha=0.6)
ax.legend(loc='upper left', fontsize=9)

# Текстовое поле для вывода h
text_h = ax.text(0.98, 0.95, '', transform=ax.transAxes, fontsize=11, 
                 verticalalignment='top', horizontalalignment='right',
                 bbox=dict(boxstyle='round', facecolor='white', alpha=0.8))

# Функция обновления при движении слайдеров
def update(val):
    V0_list = []
    nu_list = []
    
    for N, vals in data.items():
        V = np.array(vals['V'])
        I = np.array(vals['I'])
        sort_idx = np.argsort(V)
        V = V[sort_idx]
        I = I[sort_idx]
        
        # Применяем сдвиги из слайдеров
        dV = sliders_V[N].val
        dI = sliders_I[N].val
        
        V_shifted = V + dV
        I_shifted = np.maximum(I + dI, 0) # Чтобы не было корней из отрицательных чисел
        
        # Обновляем точки на графике
        lines[N].set_data(V_shifted, np.sqrt(I_shifted))
        
        # Берем n_fit точек с наименьшими значениями V_shifted для аппроксимации
        # Сортируем уже сдвинутые данные по V_shifted
        sort_idx_shifted = np.argsort(V_shifted)
        V_fit = V_shifted[sort_idx_shifted][:n_fit]
        I_fit = I_shifted[sort_idx_shifted][:n_fit]
        
        # Линейная аппроксимация sqrt(I) = k*V + b
        k, b = np.polyfit(V_fit, np.sqrt(I_fit), 1)
        V0 = -b / k
        
        # Обновляем линию аппроксимации
        x_line = np.linspace(min(V_fit)-0.2, max(V_fit)+0.5, 100)
        fit_lines[N].set_data(x_line, k*x_line + b)
        
        V0_list.append(V0)
        nu_list.append(c / get_lambda(N))
    
    # Расчет постоянной Планка по всем 5 точкам
    nu_arr = np.array(nu_list)
    v0_arr = np.array(V0_list)
    
    # Сортируем по частоте для корректной регрессии
    sort_nu = np.argsort(nu_arr)
    m, c0 = np.polyfit(nu_arr[sort_nu], v0_arr[sort_nu], 1)
    
    h_calc = e * m  # Классический расчет (знак зависит от наклона, который вы регулируете!)
    
    # Обновляем текст
    text_h.set_text(f'h = {h_calc:.3e} Дж·с\n({h_calc*1e27:.3e} эрг·с)\nНаклон: {m:.3e}')
    
    fig.canvas.draw_idle()

# Создание слайдеров
slider_start_y = 0.25
for i, N in enumerate([2200, 2300, 2460, 2550, 2830]):
    # Слайдер для сдвига тока (dI)
    ax_I = plt.axes([0.25, slider_start_y - i*0.04, 0.2, 0.02])
    s_I = Slider(ax_I, f'N={N} $\Delta I$', -0.02, 0.02, valinit=0.0, valstep=0.001, color=colors[N])
    s_I.on_changed(update)
    sliders_I[N] = s_I
    
    # Слайдер для сдвига напряжения (dV) - самый важный для выравнивания V0
    ax_V = plt.axes([0.55, slider_start_y - i*0.04, 0.2, 0.02])
    s_V = Slider(ax_V, f'N={N} $\Delta V$', -0.5, 0.5, valinit=0.0, valstep=0.01, color=colors[N])
    s_V.on_changed(update)
    sliders_V[N] = s_V

# Первичный вызов для расчета начального h
update(None)

plt.show()