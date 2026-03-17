import matplotlib.pyplot as plt

# Данные
wavelength = [582, 620, 552, 457, 455]      # нм
current = [2.014890863, 2.377468403, 3.501097335, 2.805762855, 2.939565699]  # мкА

# Построение точечного графика
plt.scatter(wavelength, current, color='blue', marker='o')

# Подписи осей
plt.xlabel(r'$\lambda$, нм')
plt.ylabel(r'$\Phi$, мкА')
# plt.title('Зависимость Ф от длины волны')

# Сетка для удобства (опционально)
plt.grid(True, linestyle=':', alpha=0.6)

# Показать график
plt.show()