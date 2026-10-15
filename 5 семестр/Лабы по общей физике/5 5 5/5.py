import numpy as np
import matplotlib.pyplot as plt

# Данные: (Источник, E_эксп, E_гамма_источника для расчета теоретического края)
data = [
    ("60Co", 0.897, 1.173),   
    ("137Cs", 0.475, 0.662),  
    ("22Na", 0.279, 0.511),   
    ("152Eu", 0.168, 0.344)   
]

m_e_c2 = 0.511 # Энергия покоя электрона, МэВ

sources = []
E_exp_list = []
E_theo_list = []

print("Источник | E_эксп (МэВ) | E_гамма (МэВ) | E_теор (МэВ)")
print("-" * 55)

for source, E_exp, E_gamma in data:
    # Расчет теоретической энергии края Комптона по формуле из методички
    E_theo = E_gamma * (2 * E_gamma) / (2 * E_gamma + m_e_c2)
    sources.append(source)
    E_exp_list.append(E_exp)
    E_theo_list.append(E_theo)
    print(f"{source:8} | {E_exp:9.3f} | {E_gamma:11.3f} | {E_theo:9.3f}")

# Построение графика
plt.figure(figsize=(8, 8))

# Точки экспериментальных данных
plt.scatter(E_theo_list, E_exp_list, color='blue', s=100, zorder=5, label='Экспериментальные данные')

# Подписи к точкам
for i, txt in enumerate(sources):
    plt.annotate(txt, (E_theo_list[i], E_exp_list[i]), textcoords="offset points", 
                 xytext=(10, 5), fontsize=11, fontweight='bold')

# Линия идеального совпадения y = x
min_val = min(min(E_theo_list), min(E_exp_list)) * 0.8
max_val = max(max(E_theo_list), max(E_exp_list)) * 1.1
plt.plot([min_val, max_val], [min_val, max_val], 'r--', linewidth=2, 
         label='Идеальное совпадение ($E_{эксп} = E_{теор}$)')

plt.xlabel('Расчетная энергия края Комптона $E_{\\text{теор}}$, МэВ', fontsize=13)
plt.ylabel('Экспериментальная энергия края Комптона $E_{\\text{эксп}}$, МэВ', fontsize=13)
# plt.title('Сравнение экспериментальных и расчетных энергий края Комптона', fontsize=14)
plt.legend(fontsize=11, loc='upper left')
plt.grid(True, alpha=0.4)
plt.tight_layout()

plt.savefig('compton_edge_user_data.png', dpi=300)
print("\nГрафик сохранен как 'compton_edge_user_data.png'")
plt.show()