import numpy as np
import matplotlib.pyplot as plt

# Энергия покоя электрона, МэВ
mc2 = 0.511

# Теоретическая функция для пика обратного рассеяния (формула 2 из методички)
def E_obs_theo(E_gamma):
    return E_gamma / (1 + 2 * E_gamma / mc2)

# Экспериментальные данные (E_гамма_теор, E_обр_эксп из вашей таблицы)
# 1. 22Na (обратное рассеяние от аннигиляционной линии 0.511 МэВ)
# 2. 137Cs (обратное рассеяние от линии 0.662 МэВ)
# 3. 60Co (обратное рассеяние от линии 1.173 МэВ)
E_gamma_points = np.array([0.511, 0.662, 1.173])
E_obs_exp = np.array([0.178, 0.198, 0.229]) # Ваши рассчитанные значения из таблицы

# Расчет теоретических значений для этих точек
E_obs_theo_points = E_obs_theo(E_gamma_points)

# Генерация плавной теоретической кривой для графика
E_gamma_curve = np.linspace(0.1, 2.0, 100)
E_obs_curve = E_obs_theo(E_gamma_curve)

# Построение графика
plt.figure(figsize=(9, 7))

# Теоретическая кривая
plt.plot(E_gamma_curve, E_obs_curve, 'r-', linewidth=2, label='Теоретическая зависимость')

# Экспериментальные точки
plt.scatter(E_gamma_points, E_obs_exp, color='blue', s=100, zorder=5, label='Экспериментальные данные')

# Подписи к точкам
labels = ["$^{22}$Na (0,511 МэВ)", "$^{137}$Cs (0,662 МэВ)", "$^{60}$Co (1,173 МэВ)"]
for i, txt in enumerate(labels):
    plt.annotate(txt, (E_gamma_points[i], E_obs_exp[i]), textcoords="offset points", 
                 xytext=(10, 5), fontsize=10, fontweight='bold')

plt.xlabel('Энергия фотопика $E_\gamma$, МэВ', fontsize=13)
plt.ylabel('Энергия пика обратного рассеяния $E_{обр}$, МэВ', fontsize=13)
# plt.title('Зависимость энергии пика обратного рассеяния от энергии фотопика', fontsize=14)
plt.legend(fontsize=11, loc='upper left')
plt.grid(True, alpha=0.4)
plt.xlim(0, 2.0)
plt.ylim(0, 0.35)
plt.tight_layout()

plt.savefig('backscatter_peak_graph.png', dpi=300)
print("График сохранён как 'backscatter_peak_graph.png'")

# Вывод таблицы для отчета
print("\n=== ДАННЫЕ ДЛЯ ТАБЛИЦЫ В ОТЧЁТЕ ===")
print("Источник | E_γ (МэВ) | E_обр_эксп (МэВ) | E_обр_теор (МэВ)")
print("-" * 55)
sources = ["22Na", "137Cs", "60Co"]
for i in range(len(sources)):
    print(f"{sources[i]:8} | {E_gamma_points[i]:7.3f} | {E_obs_exp[i]:14.3f} | {E_obs_theo_points[i]:14.3f}")

plt.show()